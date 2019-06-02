# cashier-sync

Cashier Sync is a server-side component that allows syncing Cashier to a local instance of ledger.

## Use

Run `cashiersync` from the folder which is setup for use with ledger. Having a configured .ledgerrc is useful, to point to the ledger files (book, prices, etc.) you want to use.
Ledger-cli must be in the path as it will be executed to sync the data.

The synchronization will create the journal file at the current path in the form 
`cashiersync-date.ledger`

## Run

`flask run` from cashiersync folder.
