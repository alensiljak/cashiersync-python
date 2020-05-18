'''
Parse the output for lots and return the array of lots for a symbol
'''

class LotParser:
    def __init__(self, logger, symbol):
        super().__init__()

        self.logger = logger
    
    def get_lots(self, symbol):
        from .ledger_exec import LedgerExecutor

        params = f"b ^Assets and :{symbol}$ --lots"
    
        ledger = LedgerExecutor(self.logger)
        result = ledger.run(params)
        result = ledger.split_lines(result)

        result = self.extract_lots_from_ledger_output(result)
        
        return result

    def extract_lots_from_ledger_output(self, ledger_output):
        '''
        Get all the lots from total, unless there is only one account.
        '''
        
