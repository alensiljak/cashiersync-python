from flask import Flask, request
from flask_cors import CORS #, cross_origin
import json

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
    result = ledger(params)
    
    return f'accounts: {result}'

@app.route("/balance")
def balance():
    params = "b --flat --no-total"
    result = ledger(params)
    
    return result

@app.route("/currentValues")
def currentValues():
    root = request.args.get('root')
    currency = request.args.get('currency')
    params = f"b ^{root} -X {currency} --flat --no-total"
    result = ledger(params)
    
    #return f"current values for {root} in {currency}: {result}"
    return result

@app.route('/securitydetails')
def security_details():
    ''' incomplete
    The idea is to calculate the security details: 
    - average price (this will come with --average-lot-prices)
    - yield in the last 12 months
    '''
    symbol = request.args.get('symbol')
    result = {}

    # lots
    ledger_cmd = f'b ^Assets and :{symbol}$ --lots --no-total --depth 2'
    lots = ledger(ledger_cmd).split('\n')
    result['lots'] = lots

    # average price

    # yield in the last 12 months
    from datetime import date, timedelta
    yield_start_date = date.today() - timedelta(weeks=52)
    yield_from = yield_start_date.strftime("%Y-%m-%d")
    # the accound ends with the symbol name
    ledger_cmd = f'b ^Income and :{symbol}$ -b {yield_from} --flat --no-total'
    # split separate lines
    rows = ledger(ledger_cmd).strip().split('\n')
    for i, item in enumerate(rows):
        rows[i] = rows[i].strip()
    result['income'] = rows

    return json.dumps(result)

@app.route('/about')
def about():
    ''' display some diagnostics '''
    import os
    cwd = os.getcwd()
    return f"cwd: {cwd}"

###################################

def ledger(parameters):
    ''' Execute ledger command '''
    import subprocess
    from cashiersync.config import Configuration

    command = f"ledger {parameters}"
    result = subprocess.run(command, shell=True, encoding="utf-8", capture_output=True)
    #cfg = Configuration()
    # cwd=cfg.ledger_working_dir

    if result.returncode != 0:
        output = result.stderr
    else:
        output = result.stdout
    
    return output

def run_server():
    """ Available to be called from outside """
    # use_reloader=False port=23948
    app.run(host='0.0.0.0', threaded=True, use_reloader=False)
    # host='127.0.0.1' host='0.0.0.0'
    # , debug=True
    # Prod setup: 
    # debug=False


##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    run_server()