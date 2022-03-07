from brownie import LotCoin
from web3 import Web3

from scripts.helpful_scripts import get_account


def deploy_lot_coin():
    account = get_account()
    raphael_address = "0x9211cd5a0940FA9F71bcbcF1d45b0EC20Cb62A38"
    mike_address = "0x00fE76cbadEe293339360655bb477c29dba01078"
    benson_address = "0x0d02DdadeFef2580378B1a006B13c368A658123A"
    initial_supply = Web3.toWei(21_000_000, "ether")
    lot_coin = LotCoin.deploy(
        raphael_address, mike_address, benson_address, initial_supply, {"from": account}
    )
    return lot_coin


def main():
    deploy_lot_coin()
