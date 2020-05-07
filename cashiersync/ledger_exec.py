'''
The ledger executor.
Runs ledger-cli to fetch the data.
'''

class LedgerExecutor:
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    def run(self, parameters):
        ''' Execute ledger command '''
        import subprocess
        from cashiersync.config import Configuration

        command = f"ledger {parameters}"
        result = subprocess.run(command, shell=True, encoding="utf-8", capture_output=True)
        #cfg = Configuration()
        # cwd=cfg.ledger_working_dir

        if self.logger:
            self.logger.debug(result)

        if result.returncode != 0:
            output = result.stderr
        else:
            output = result.stdout
        
        return output
