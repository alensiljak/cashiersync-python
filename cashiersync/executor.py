'''
Encapsulates subprocess for execution of external console commands
and programs.
'''

class Executor:
    def __init__(self, logger = None):
        super().__init__()
        self.logger = logger
        self.process = None

    def run_subprocess(self, command, cwd: str = None):
        ''' Execute a command in the local terminal '''
        import subprocess

        #self.logger.debug(f'running in {cwd}')

        result = subprocess.run(command, shell=True, encoding="utf-8", capture_output=True,
            cwd=cwd)

        # if self.logger:
        #     self.logger.debug(result)

        if result.returncode != 0:
            output = result.stderr
            raise Exception('Ledger error', output)
        else:
            output = result.stdout

        #output = self.split_lines(output)

        return output

    def run(self, command):
        ''' Run Ledger-cli command '''
        import pexpect

        self.process = pexpect.spawn('ledger', encoding='utf-8')
        # child.logfile_read = sys.stdout
        self.process.expect(']')

        self.process.sendline(command)
        self.process.expect(']')

        output = self.process.before
        return output

    def shutdown(self):
        ''' Close the process '''
        if self.process:
            self.process.sendline('quit')
