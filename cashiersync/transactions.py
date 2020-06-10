'''
    Ledger Transactions
'''
from .ledger_exec import LedgerExecutor
from typing import List


class Transactions:
    def __init__(self):
        super().__init__()

    def get_transactions(self, account, dateFrom, dateTo) -> List[str]:
        ''' Fetch historical transactions and return an array '''
        ledger = LedgerExecutor(None)
        params = f'r "{account}" -b {dateFrom} -e {dateTo}'
        output = ledger.run(params)
        output = ledger.split_lines(output)

        return output
