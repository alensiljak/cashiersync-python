'''
    Models used in the app.
'''
#from json import JSONEncoder
import json
from decimal import Decimal


class RegisterRow:
    '''
    Represents the register transaction. 
    Also used for IB report comparison.
    '''
    def __init__(self):
        self.date: str = None
        self.payee: str = None
        self.account: str = None
        self.amount: Decimal = None
        self.currency: str = None

    def __repr__(self):
        return { 'date':self.date, 'payee':self.payee,
            'amount':self.amount, 'currency':self.currency }

    def __str__(self):
        return (f"Transaction(date='{self.date}', payee='{self.payee}'," + 
            f", amount={self.amount}, currency='{self.currency}')")

class Distribution:
    '''
    Represents the register transaction. 
    Also used for IB report comparison.
    '''
    def __init__(self):
        self.date: str = None
        self.symbol: str = None
        self.type: str = None
        self.amount: Decimal = None
        self.currency: str = None

    def __repr__(self):
        return { 'date':self.date, 'symbol':self.symbol, 'type':self.type,
            'amount':self.amount, 'currency':self.currency }

    def __str__(self):
        return (f"Transaction(date='{self.date}', symbol='{self.symbol}'," + 
            f"type='{self.type}', amount={self.amount}, currency='{self.currency}')")

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class TransactionEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Transaction):
            return object.__dict__
        elif isinstance(object, Decimal):
            return str(object)
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)