'''
Encapsulates subprocess for execution of external console commands
and programs.
'''
import pexpect

class Executor:
    """Class for executing Ledger-cli commands and returning their output.
    This class provides functionality to run Ledger-cli commands using pexpect,
    handle the output, and clean up ANSI escape sequences from the results.
    Attributes:
        logger: Optional logger instance for debugging purposes
        process: pexpect spawn object representing the Ledger-cli process
    Methods:
        run(command): Executes a Ledger-cli command and returns cleaned output
        clean_ansi(text): Removes ANSI escape sequences from text
        shutdown(): Closes the Ledger-cli process
    Example:
        executor = Executor()
        result = executor.run('balance')
        executor.shutdown()
    """
    def __init__(self, logger = None):
        super().__init__()

        self.logger = logger
        # Run ledger-cli immediately.
        self.process = pexpect.spawn('ledger', encoding='utf-8')
        self.process.expect(']')
        logger.debug('Ledger process started.')

    def run(self, command) -> list[str]:
        ''' Run Ledger-cli command 
        Runs a process using pexpect. This works with ledger-cli.
        '''

        # child.logfile_read = sys.stdout
        # self.process = pexpect.spawn('ledger', encoding='utf-8')
        # self.process.expect(']')

        self.process.sendline(command)
        self.process.expect(']', timeout=15)
        # self.process.expect(pexpect.EOF, timeout=15)

        output = self.process.before

        # clean up new lines
        output = output.splitlines()
        
        # clean up ANSI codes
        output = [self.clean_ansi(line) for line in output]

        # Remove the first line (command).
        output = output[1:]

        # remove empty lines
        output = [line for line in output if line.strip() != '']

        return output

    def clean_ansi(self, text: str) -> str:
        ''' Remove ANSI escape codes '''
        import re
        # ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mK]')
        # ansi_escape = re.compile(r'(\x1B[@-_][0-?]*[ -/]*[@-~])')
        # ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]|[=>])')
        return ansi_escape.sub('', text)

    def shutdown(self):
        ''' Close the process '''
        if self.process:
            self.process.sendline('quit')
