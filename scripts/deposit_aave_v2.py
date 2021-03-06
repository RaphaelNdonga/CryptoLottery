from brownie import network, config, interface
from web3 import Web3
from scripts.helpful_scripts import get_account, POLYGON_NETWORKS


def main():
    if network.show_active() in POLYGON_NETWORKS:
        network.priority_fee("30 gwei")
    deposit(Web3.toWei(0.01, "ether"))


def deposit(amount):
    account = get_account()
    provider_address = config["networks"][network.show_active()][
        "lending_pool_addresses_provider"
    ]
    pool_address_provider = interface.ILendingPoolAddressesProvider(provider_address)
    pool_address = pool_address_provider.getLendingPool()
    print(f"pool address obtained: {pool_address}")
    pool = interface.ILendingPool(pool_address)
    wrapped = None
    wrapped = interface.IWrapped(config["networks"][network.show_active()]["wrapped"])
    tx = wrapped.deposit({"from": account, "value": amount})
    tx.wait(1)
    wrapped_address = config["networks"][network.show_active()]["wrapped"]
    wrapped_token = interface.IERC20(wrapped_address)
    print("Approving transfer of wrapped token by pool")
    approve_txn = wrapped_token.approve(pool_address, amount, {"from": account})
    approve_txn.wait(1)
    print("wrapped approved successfully")
    print("Depositing funds into aave")

    supply_txn = pool.deposit(
        wrapped_address, amount, account.address, 0, {"from": account}
    )
    supply_txn.wait(1)
    account_data = pool.getUserAccountData(account.address)
    print(f"account is: {account.address} ")
    print(f"account data! {account_data}")
