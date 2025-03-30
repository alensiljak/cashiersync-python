# cashier-sync

Cashier Sync is a (server-side) component that allows syncing [Cashier](https://cashier-svelte.netlify.app/), ([source](https://github.com/alensiljak/cashier-blazor)) to a local instance of ledger.

It is written in Python and is available for installation via pip (PyPi).

Cashier Sync simply provides an API end point, by default on port 5000, to which Cashier is supposed to connect to read the account balances. It never writes to your file and only uses the `ledger` binary to read the information.

## Setup and Use

Install `cashiersync` Python package. The recommended way is via `uv`:
```sh
uv tool install cashiersync
```
Run `cashiersync` in a console from a location in which you can also run ledger-cli, because Cashier Sync will simply run `ledger` to get the required data.

You can create your setup by adding a `.ledgerrc` file, pointing to the desired book and prices, or in any way you prefer.

### Tunnel

Optional: set up a tunnel to your machine so that it is available over the internet.
`ssh -R 80:localhost:5000 serveo.net`
or 
`ssh -R cashier:80:localhost:5000 serveo.net`

However, since Python runs in Termux, it might be more convenient to run the server component locally (cashier-sync and ledger).

## Run

### FastAPI and Uvicorn

`uvicorn cashiersync.main:app`

### Production

The `cashiersync` executable console script is registered by the setup. This will run the web app.
This may require the `wheel` package.

The configuration file can be created if the default options are to be modified.

### Running on Mobile Devices

The server can also run on Android in Termux. All that is needed in such case is to get the ledger book onto the device, possibly using git. 

## Development

Run uvicorn.

### Deployment

See distribute.sh script for the steps.
