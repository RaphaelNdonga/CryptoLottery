import time
from brownie import LotCoin,MillionDraw,network,config
from web3 import Web3

from scripts.helpful_scripts import fund_with_lot, get_account, get_lot_coin, get_million_draw, join_draw,fund_with_link


def deploy_lot_coin():
    account = get_account()
    raphael_address = "0x9211cd5a0940FA9F71bcbcF1d45b0EC20Cb62A38"
    mike_address = "0x00fE76cbadEe293339360655bb477c29dba01078"
    benson_address = "0x0d02DdadeFef2580378B1a006B13c368A658123A"
    initial_supply = Web3.toWei(21_000_000,"ether")
    lot_coin = LotCoin.deploy(raphael_address,mike_address,benson_address, initial_supply,{"from":account})
    return lot_coin

def deploy_million_draw():
    account = get_account()
    million_draw = MillionDraw.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link"],
        config["networks"][network.show_active()]["key_hash"],
        Web3.toWei(0.0001,"ether"),{"from":account})
    return million_draw

def transfer_lot_coin(sender,receiver,amount):
    lot_coin = get_lot_coin()
    lot_coin.transfer(receiver,amount,{"from":sender})

def main():
    # deploy_lot_coin()
    # million_draw_contract = deploy_million_draw()
    million_draw_contract = get_million_draw()
    fund_with_lot(contract_address=million_draw_contract.address)
    fund_with_link(contract_address=million_draw_contract.address)
    join_draw(million_draw_contract)
    million_draw_contract.getRandomness({"from":get_account()})
    time.sleep(200)
    million_draw_contract.getWinner({"from":get_account()})
    print(f"The winner is {million_draw_contract.winner()}")
    million_draw_contract.fundWinner(get_lot_coin(),{"from":get_account()})

    # sender = get_account()
    # mike_address = "0x00fE76cbadEe293339360655bb477c29dba01078"
    # amount = Web3.toWei(1000,"ether")
    # tx = transfer_lot_coin(sender.address,mike_address,amount)