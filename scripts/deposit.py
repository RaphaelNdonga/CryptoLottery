from brownie import network, config, interface
from web3 import Web3
from scripts.helpful_scripts import get_account, POLYGON_NETWORKS


def main():
    if network.show_active() in POLYGON_NETWORKS:
        network.priority_fee("30 gwei")
    deposit(1)


def deposit(amount):
    account = get_account()
    provider_address = config["networks"][network.show_active()][
        "pool_addresses_provider"
    ]
    pool_address_provider = interface.ILendingPoolAddressesProvider(provider_address)
    pool_address = pool_address_provider.getLendingPool()
    print(f"pool address obtained: {pool_address}")
    pool = interface.ILendingPool(pool_address)
    weth = interface.WethInterface(
        config["networks"][network.show_active()]["weth_token"]
    )
    tx = weth.deposit({"from": account, "value": amount})
    tx.wait(1)
    weth_address = config["networks"][network.show_active()]["weth_token"]
    weth_token = interface.IERC20(weth_address)
    print("Approving transfer of weth token by pool")
    approve_txn = weth_token.approve(pool_address, amount, {"from": account})
    approve_txn.wait(1)
    print("Weth approved successfully")
    print("Depositing funds into aave")

    supply_txn = pool.deposit(
        weth_address, amount, account.address, 0, {"from": account}
    )
    supply_txn.wait(1)
    account_data = pool.getUserAccountData(account.address)
    print(f"account is: {account.address} ")
    print(f"account data! {account_data}")
