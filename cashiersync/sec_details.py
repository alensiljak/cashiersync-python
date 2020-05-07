'''
Security details calculation
'''

class SecurityDetails:
    '''
    The idea is to calculate the security details: 
    - average price (this will come with --average-lot-prices)
    - yield in the last 12 months
        - get the distributions "^income and :symbol$" in the last 12 months
        - divide by the current value
    '''
    def __init__(self, symbol):
        super().__init__()

        self.symbol = symbol
    
    def calculate(self):
        from .ledger_exec import LedgerExecutor

        result = {}
        ledger = LedgerExecutor()

        # lots
        ledger_cmd = f'b ^Assets and :{self.symbol}$ --lots --no-total --depth 2'
        lots = ledger.run(ledger_cmd).split('\n')
        result['lots'] = lots

        # average price

        # yield in the last 12 months
        from datetime import date, timedelta
        yield_start_date = date.today() - timedelta(weeks=52)
        yield_from = yield_start_date.strftime("%Y-%m-%d")
        # the accound ends with the symbol name
        ledger_cmd = f'b ^Income and :{self.symbol}$ -b {yield_from} --flat --no-total'
        # split separate lines
        rows = ledger.run(ledger_cmd).strip().split('\n')
        for i, item in enumerate(rows):
            rows[i] = rows[i].strip()
        result['income'] = rows

        return result

    def get_yield(self):
        '''
        Calculate the yield in the last 12 months.
        This, of course is affected by the recent purchases!
        '''
        # get the income in the last 12 months
        # get the current value
