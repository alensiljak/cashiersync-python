'''
'''
from decimal import Decimal
from cashiersync.ledger_output_parser import LedgerOutputParser

parser = LedgerOutputParser()

def test_parsing_long_line():
    '''
    Test parsing the long line(s)
    '''
    line = "2020-01-01 SYMBOL1 distribution               In:Investme:Dividend:Broker1234:SYMBOL1           -77.81 USD           -77.81 USD"

    tx = parser.get_row_from_register_line(line, None)

    assert tx is not None
    assert tx.date == "2020-01-01"
    assert tx.payee == "SYMBOL1 distribution"
    assert tx.account == "In:Investme:Dividend:Broker1234:SYMBOL1"
    assert tx.amount == Decimal("-77.81")
    assert tx.currency == "USD"

def test_parsing_short_line():
    '''
    Parse the secondary posting lines (without a date and payee)
    '''
    line = "                                              Assets:Investments:Broker:Cash Acc                 83.65 EUR                    0"

    tx = parser.get_row_from_register_line(line, None)

    assert tx is not None
    assert tx.date == None
    assert tx.payee == None
    assert tx.account == "Assets:Investments:Broker:Cash Acc"
    assert tx.amount == Decimal("83.65")
    assert tx.currency == "EUR"
