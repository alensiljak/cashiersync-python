'''
Runs Ledger in a background process.
'''

import asyncio
from threading import Lock

class Executor:
    """
    Class Executor
    This class manages an interactive subprocess running the "ledger" command-line tool.
    It provides methods to send commands to the ledger process, read responses,
    and gracefully shutdown the process.
    Attributes:
        logger (Optional[logging.Logger]): Optional logger instance for debug and error logging.
        lock (threading.Lock): A lock to ensure that interactions with the ledger process are thread-safe.
        process (subprocess.Popen): The subprocess running the ledger command in interactive mode.
    Methods:
        __init__(logger=None):
            Initializes the Executor instance by setting up the logger, a threading lock,
            and starting the ledger process in interactive mode. Logs a debug message if a logger is provided.
        run(command: str) -> subprocess.CompletedProcess:
            Sends a command string to the ledger process via its standard input and reads the output until
            a prompt (assumed to end with ']') is encountered. Returns a subprocess.CompletedProcess-like object
            with the command, a return code of 0, the accumulated standard output, and an empty standard error string.
        shutdown():
            Shuts down the ledger process by sending a "quit" command if possible, terminating the process,
            and waiting for it to exit. Any exceptions during shutdown are logged as errors if a logger is provided.
    """
    def __init__(self, logger=None):
        self.logger = logger
        self.lock = Lock()
        self.process = None

    async def start(self):
        '''
        Starts the ledger process in interactive mode using asyncio.
        This method is asynchronous and should be awaited.
        '''
        self.process = await asyncio.create_subprocess_exec('ledger',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        if self.logger:
            self.logger.debug('Ledger process started.')


    def run(self, command: str) -> str:
        '''
        Sends a command to the ledger process and reads the output until a prompt is encountered.
        Args:
            command (str): The command to send to the ledger process.
        Returns:
            str: The output from the ledger process.
        Raises:
            RuntimeError: If the ledger process is not available (stdin or stdout is None).
        '''
        with self.lock:
            if self.process is None:
                raise RuntimeError("Ledger process not available.")

            # Send the command to ledger.
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
            output_lines = []
            # Read the output until a prompt is encountered.
            # Adjust the condition below to match the actual ledger prompt.
            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                output_lines.append(line)
                if line.strip().endswith(']'):
                    break
            output = ''.join(output_lines)
            # Create a result object similar to subprocess.CompletedProcess.
            # result = asyncio.subprocess.CompletedProcess(args=command, returncode=0, stdout=output, stderr="")
            result = output
            return result

    def shutdown(self):
        '''
        Shuts down the ledger process.
        '''
        if self.process:
            try:
                if self.process.stdin:
                    # Send a quit command if ledger supports it.
                    self.process.stdin.write("quit\n")
                    self.process.stdin.flush()
                self.process.terminate()
                # self.process.wait(timeout=10)
                self.process.wait()
            except OSError as e:
                if self.logger:
                    self.logger.error("Error during shutdown: %s", e)
