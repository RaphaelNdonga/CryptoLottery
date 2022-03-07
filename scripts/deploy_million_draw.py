from scripts.helpful_scripts import get_account
from brownie import MillionDraw, config, network
from web3 import Web3


def deploy_million_draw():
    account = get_account()
    million_draw = MillionDraw.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link"],
        config["networks"][network.show_active()]["key_hash"],
        Web3.toWei(0.1, "ether"),
        {"from": account},
    )
    return million_draw


def main():
    deploy_million_draw()
