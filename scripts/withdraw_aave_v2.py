from brownie import network, config, interface
from web3 import Web3
from scripts.helpful_scripts import get_account


def main():
    withdraw(Web3.toWei(0.01, "ether"))


def withdraw(amount):
    account = get_account()
    provider_address = config["networks"][network.show_active()][
        "lending_pool_addresses_provider"
    ]
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        provider_address
    )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    wrapped_address = config["networks"][network.show_active()]["wrapped"]
    withdraw_txn = lending_pool.withdraw(
        wrapped_address, amount, account.address, {"from": account}
    )
    withdraw_txn.wait(1)
