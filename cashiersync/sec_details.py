'''
Security details calculation
'''
from .ledger_exec import LedgerExecutor


class SecurityDetails:
    '''
    The idea is to calculate the security details: 
    - average price (this will come with --average-lot-prices)
    - yield in the last 12 months
        - get the distributions "^income and :symbol$" in the last 12 months
        - divide by the current value
    '''
    def __init__(self, logger, symbol, currency):
        super().__init__()

        self.logger = logger
        self.symbol = symbol
        # The currency to use for all values
        self.currency = currency
    
    def calculate(self):
        result = {}
        ledger = LedgerExecutor(self.logger)

        # lots
        ledger_cmd = f'b ^Assets and :{self.symbol}$ --lots --no-total --depth 2'
        lots = ledger.run(ledger_cmd).split('\n')
        result['lots'] = lots

        # average price

        # yield in the last 12 months
        result['yield'] = self.get_yield()

        # income (demo)
        income = self.get_income()
        result['income'] = income


        return result

    def get_yield(self):
        '''
        Calculate the yield in the last 12 months.
        This, of course is affected by the recent purchases!
        '''
        from datetime import date, timedelta

        ledger = LedgerExecutor(self.logger)

        yield_start_date = date.today() - timedelta(weeks=52)
        yield_from = yield_start_date.strftime("%Y-%m-%d")
        
        # the accound ends with the symbol name
        ledger_cmd = f'b ^Income and :{self.symbol}$ -b {yield_from} --flat -X {self.currency}'
        next_line_is_total = False
        total = None
        # split separate lines and trim.
        rows = ledger.run(ledger_cmd).strip().split('\n')
        for i, item in enumerate(rows):
            rows[i] = rows[i].strip()
            # get total
            if next_line_is_total:
                total = rows[i]
                self.logger.debug(f'total: {total}')
            if '------' in rows[i]:
                next_line_is_total = True

        # get the income in the last 12 months
        # get the current value
        the_yield = 0

        return the_yield

    def get_income(self):
        from datetime import date, timedelta

        yield_start_date = date.today() - timedelta(weeks=52)
        yield_from = yield_start_date.strftime("%Y-%m-%d")
        
        ledger = LedgerExecutor(self.logger)
        # the accound ends with the symbol name
        ledger_cmd = f'b ^Income and :{self.symbol}$ -b {yield_from} --flat --no-total'
        # split separate lines
        rows = ledger.run(ledger_cmd).strip().split('\n')
        for i, item in enumerate(rows):
            rows[i] = rows[i].strip()

        return rows
