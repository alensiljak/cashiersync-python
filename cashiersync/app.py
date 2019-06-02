from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    # test config
    return "Hello World!"

@app.route("/accounts")
def accounts():
    params = "accounts"
    result = ledger(params)
    
    return f"accounts: {result}"

@app.route("/balance")
def balance():
    params = "b --flat --no-total"
    result = ledger(params)
    
    return result

@app.route("/currentValues")
def currentValues():
    root = request.args.get('root')
    currency = request.args.get('currency')
    params = f"b ^{root} -X {currency}"
    result = ledger(params)
    return f"current values for {root} in {currency}: {result}"

def ledger(parameters):
    ''' Execute ledger command '''
    import subprocess
    from cashiersync.config import Configuration

    cfg = Configuration()

    command = f"ledger {parameters}"
    result = subprocess.run(command, shell=True, encoding="utf-8", capture_output=True,
        cwd=cfg.ledger_working_dir)

    if result.returncode != 0:
        output = result.stderr
    else:
        output = result.stdout
    
    return output
