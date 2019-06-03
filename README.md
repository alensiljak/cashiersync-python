# cashier-sync

Cashier Sync is a server-side component that allows syncing Cashier to a local instance of ledger.

## Use

Run `cashiersync` from the folder which is setup for use with ledger. Having a configured .ledgerrc is useful, to point to the ledger files (book, prices, etc.) you want to use.
Ledger-cli must be in the path as it will be executed to sync the data.

The synchronization will create the journal file at the current path in the form 
`cashiersync-date.ledger`

## Run

`flask run` from cashiersync folder.

## Important

Interestingly, when the app is run through `cashiersync` entry point, the CORS is not initialized.
But when run with `flask run`, it is.

Use a similar script to start, instead of the entry points:

```
export FLASK_APP=cashiersync.app
flask run
```

## Running on Mobile Devices

The server can also run on Android in Termux. All that is needed in such case is to get the book onto the device, possibly using git. 
