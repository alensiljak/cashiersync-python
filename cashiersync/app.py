from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/accounts")
def accounts():
    params = "accounts"
    result = ledger(params)
    
    return f"accounts: {result}"

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
    command = f"ledger {parameters}"
    #result = subprocess.run(command, capture_output=True, shell=True, encoding="utf-8")
    #return result.stdout
    result = subprocess.check_output(command, shell=True, encoding="utf-8")
    return result
