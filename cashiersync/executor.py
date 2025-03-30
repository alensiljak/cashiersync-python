'''
Encapsulates subprocess for execution of external console commands
and programs.
'''

class Executor:
    def __init__(self, logger = None):
        super().__init__()
        self.logger = logger
        self.process = None

    def run(self, command) -> list[str]:
        ''' Run Ledger-cli command 
        Runs a process using pexpect. This works with ledger-cli.
        '''
        import pexpect
        from strip_ansi import strip_ansi

        self.process = pexpect.spawn('ledger', encoding='utf-8')
        # child.logfile_read = sys.stdout
        self.process.expect(']')

        self.process.sendline(command)
        self.process.expect(']')

        output = self.process.before

        # clean up new lines
        #output = output.split('\r\n')
        output = output.splitlines()
        
        # clean up ANSI codes
        output = [self.clean_ansi(line) for line in output]
        # output = [strip_ansi(line) for line in output]

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
