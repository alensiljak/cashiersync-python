from json import encoder
from flask import Flask, request
from flask_cors import CORS  # , cross_origin
import json
from .ledger_exec import LedgerExecutor

app = Flask(__name__)
CORS(app)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/accounts")
def accounts():
    params = "accounts"
    ledger = LedgerExecutor(app.logger)
    result = ledger.run(params)

    return result


@app.route("/balance")
def balance():
    params = "b --flat --no-total"
    ledger = LedgerExecutor(app.logger)
    result = ledger.run(params)

    return result


@app.route("/currentValues")
def currentValues():
    root = request.args.get('root')
    currency = request.args.get('currency')
    params = f"b ^{root} -X {currency} --flat --no-total"

    ledger = LedgerExecutor(app.logger)
    result = ledger.run(params)

    # return f"current values for {root} in {currency}: {result}"
    return result


@app.route("/lots")
def lots():
    from .lots_parser import LotParser

    symbol = request.args.get('symbol')

    parser = LotParser(app.logger)
    result = parser.get_lots(symbol)

    return json.dumps(result)


@app.route('/payees')
def payees():
    ''' Send Payees as a simple list '''
    params = f"payees"
    ledger = LedgerExecutor(app.logger)
    result = ledger.run(params)
    return result


@app.route('/search', methods=['POST'])
def search_tx():
    ''' Search Transactions - Register '''
    from cashiersync.ledger_output_parser import LedgerOutputParser
    from cashiersync.model import TransactionEncoder

    query = request.get_json()
    app.logger.debug(query)

    dateFrom = query['dateFrom']
    dateTo = query['dateTo']
    payee = query['payee']
    freeText = query['freeText']

    params = f"r "
    if dateFrom:
        params += f'-b {dateFrom}'
    if dateTo is not None:
        params += f'-e {dateTo}'
    if payee:
        params += f'@"{payee}"'
    if freeText:
        params += f'{freeText}'

    ledger = LedgerExecutor(app.logger)
    result = ledger.run(params)

    lines = result.split('\n')
    parser = LedgerOutputParser()
    lines = parser.clean_up_register_output(lines)

    txs = parser.get_rows_from_register(lines)
    # return result
    #encoded = TransactionEncoder().encode(txs)
    encoded = json.dumps(txs, cls=TransactionEncoder)
    # return json.dumps(txs)
    return encoded


@app.route('/securitydetails')
def security_details():
    ''' Displays the security details (analysis) '''
    from .sec_details import SecurityDetails

    symbol = request.args.get('symbol')
    currency = request.args.get('currency')

    x = SecurityDetails(app.logger, symbol, currency)
    result = x.calculate()

    return json.dumps(result)


@app.route('/transactions')
def transactions():
    ''' Fetch the transactions in account for the giver period '''
    from .transactions import LedgerTransactions

    account = request.args.get('account')
    dateFrom = request.args.get('dateFrom')
    dateTo = request.args.get('dateTo')

    assert account is not None
    assert dateFrom is not None
    assert dateTo is not None

    tx = LedgerTransactions()
    txs = tx.get_transactions(account, dateFrom, dateTo)

    return json.dumps(txs)


@app.route('/xact', methods=['POST'])
def xact():
    query = request.get_json()
    params = 'xact '

    if 'date' in query:
        date_param = query['date']
        params += date_param + ' '
    if 'payee' in query:
        params += f'@"{query["payee"]}" '
    if 'freeText' in query:
        free_text = query['freeText']
        params += free_text

    #params = f'xact {date_param} {free_text}'

    ledger = LedgerExecutor(app.logger)
    try:
        result = ledger.run(params)
    except Exception as error:
        result = str(error)

    return result


@app.route('/about')
def about():
    ''' display some diagnostics '''
    import os
    cwd = os.getcwd()
    return f"cwd: {cwd}"

# Operations


@app.route('/shutdown')
def shutdown():
    # app.do_teardown_appcontext()

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

###################################


def run_server():
    """ Available to be called from outside """
    # use_reloader=False port=23948
    app.run(host='0.0.0.0', threaded=True, use_reloader=False, debug=True)
    # host='127.0.0.1' host='0.0.0.0'
    # , debug=True
    # Prod setup:
    # debug=False


##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    run_server()
