from scripts.helpful_scripts import get_account, POLYGON_NETWORKS, get_lot_coin
from brownie import MillionDraw, config, network
from web3 import Web3


def deploy_million_draw():
    if network.show_active() in POLYGON_NETWORKS:
        network.priority_fee("30 gwei")
    account = get_account()
    million_draw = MillionDraw.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link"],
        config["networks"][network.show_active()]["key_hash"],
        Web3.toWei(config["networks"][network.show_active()]["link_fee"], "ether"),
        account,
        1,
        {"from": account},
    )
    one_million_lot = Web3.toWei(1_000, "ether")
    transfer_lot_coin(account, million_draw, one_million_lot)
    return million_draw


def transfer_lot_coin(sender, receiver, amount):
    lot_coin = get_lot_coin()
    lot_coin.transfer(receiver, amount, {"from": sender})


def main():
    deploy_million_draw()
