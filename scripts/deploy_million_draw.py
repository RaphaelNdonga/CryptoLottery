from scripts.helpful_scripts import get_account, POLYGON_NETWORKS
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
        {"from": account},
    )
    return million_draw


def main():
    deploy_million_draw()
