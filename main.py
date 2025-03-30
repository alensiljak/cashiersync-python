''' Application entry point '''

import logging
from cashiersync.executor import Executor
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
# from cashiersync.ledger_exec import LedgerExecutor

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

# CORS
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True,
    allow_methods=['*'], allow_headers=['*'])

ledger_exec = None


@app.get('/')
def ledger(request: Request):
    ''' Returns the ledger file '''
    # from fastapi.responses import FileResponse
    # from cashiersync.config import Config

    # params will contain all query parameters as a dictionary
    print(request.query_params)
    params = request.query_params._dict

    command = params.get('command', None)

    global ledger_exec
    if ledger_exec is None:
        ledger_exec = Executor(logger=logger)

    result = ledger_exec.run(command)

    return result

    #config = Config()
    # path = config.get_config_path()
    #return FileResponse(path)

@app.get('/about')
def about():
    ''' display some diagnostics '''
    import os
    cwd = os.getcwd()
    return f"cwd: {cwd}"

@app.get('/hello')
async def hello_img():
    ''' Returns an image, can be used with <img> element to check online status. '''

    import io
    import base64

    # Base64 encoded pixel
    pixelEncoded = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    pixel = base64.b64decode(pixelEncoded)
    buf = io.BytesIO(pixel)
    
    response = StreamingResponse(buf, media_type='image/png')
    
    return response

@app.get('/shutdown')
def shutdown():
    import os, signal

    # Shutdown Ledger
    global ledger_exec
    if ledger_exec is not None:
        logger.info("Shutting down Ledger...")
        ledger_exec.shutdown()
        ledger_exec = None

    os.kill(os.getpid(), signal.SIGTERM)

    return {"message": "Shutting down"}

###################################


def run_server():
    ''' Available to be called from outside, i.e. console scripts in setup. '''
    # Prod setup:
    # debug=False
    import uvicorn
    port = 3000 # to match the Rust version. Original: 5000.
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    # config = uvicorn.Config("main:app", host="0.0.0.0", port=port)
    # server = uvicorn.Server(config)
    # server.run()
    # Check if in DEV mode.
    # reload=True
    # log_level='debug'
    # log_level="info"

##################################################################################
if __name__ == '__main__':
    run_server()
