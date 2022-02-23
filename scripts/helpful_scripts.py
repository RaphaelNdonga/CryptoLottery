from brownie import accounts,config,network

LOCAL_BLOCKCHAIN=["development","mainnet-fork"]

def get_account():
    account = None
    if network.show_active() in LOCAL_BLOCKCHAIN:
        account = accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])
    return account