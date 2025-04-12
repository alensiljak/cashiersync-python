"""Application entry point"""

import logging
import os
import signal
from contextlib import asynccontextmanager
import base64
import io

import uvicorn
from fastapi import FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from cashiersync.executor import Executor


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
    Manage the application's lifespan events.

    On startup:
        - Initializes a global Executor instance and stores it in the application's state.
    On shutdown:
        - Shuts down the Executor instance and cleans up resources.

    This setup ensures that the Executor is available throughout the app's lifecycle.
    """
    # Initialize ledger_exec once at startup
    fastapi_app.state.ledger_exec = Executor(logger=logger)
    await fastapi_app.state.ledger_exec.start()
    logger.info("Executor started.")
    # Make sure to yield control back to the FastAPI app
    yield
    # Properly shutdown the executor when the app is shutting down
    if hasattr(fastapi_app.state, "ledger_exec") and fastapi_app.state.ledger_exec:
        logger.info("Shutting down Executor...")
        fastapi_app.state.ledger_exec.shutdown()
        fastapi_app.state.ledger_exec = None


app = FastAPI(
    title="Cashier Server",
    description="Ledger CLI REST server for Cashier PWA.",
    lifespan=lifespan,
)

logger = logging.getLogger("uvicorn.error")
# logger = logging.getLogger("cashier_server")

# Enable CORS with any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_ledger(command: str) -> str:
    '''
    Executes a ledger command and returns the output.
    '''
    # args = command.split()
    try:
        # Run the ledger command and capture output
        # result = subprocess.run(["ledger", *args], capture_output=True, text=True)

        logger.debug("Ledger command: %s", command)
        # Use the singleton instance from app.state
        result = app.state.ledger_exec.run(command)

    except (RuntimeError, OSError) as e:
        logger.error("Failed to execute ledger command: %s", e)
        return str(e)

    if not result.returncode == 0:
        return result.stderr
    return result.stdout


@app.get("/", response_class=JSONResponse)
# def ledger(command: Optional[str] = None):
async def ledger(
    command: str = Query(None, description="The ledger command to execute"),
):
    """Returns the ledger file"""
    if command is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=["No Ledger command sent"]
        )

    ledger_output = run_ledger(command)

    # split output into separate lines
    rows = ledger_output.splitlines()
    return JSONResponse(status_code=status.HTTP_200_OK, content=rows)


@app.get("/about")
def about():
    """display some diagnostics"""
    cwd = os.getcwd()
    return f"cwd: {cwd}"


@app.get("/hello")
async def hello_img():
    """Returns an image, can be used with <img> element to check online status."""
    # Base64 encoded pixel
    pixel_encoded = b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    pixel = base64.b64decode(pixel_encoded)
    buf = io.BytesIO(pixel)

    response = StreamingResponse(buf, media_type="image/png")

    return response


@app.get("/shutdown")
def shutdown():
    """
    Gracefully shuts down the application and its components.
    This function performs the following shutdown sequence:
    1. Shuts down the Ledger component if it exists
    2. Terminates the current process using SIGTERM signal
    Returns:
        dict: A message indicating shutdown is in progress
    """
    os.kill(os.getpid(), signal.SIGTERM)

    return {"message": "Shutting down"}


###################################


def run_server():
    """Available to be called from outside, i.e. console scripts in setup."""
    # Prod setup:
    # debug=False
    port = 3000  # to match the Rust version. Original: 5000.
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, log_level="debug")
    # config = uvicorn.Config("main:app", host="0.0.0.0", port=port)
    # server = uvicorn.Server(config)
    # server.run()
    # Check if in DEV mode.


##################################################################################
if __name__ == "__main__":
    run_server()
