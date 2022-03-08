from scripts.helpful_scripts import get_account, get_lot_coin, get_million_draw
import time
from brownie import network


def main():
    network.priority_fee("30 gwei")
    million_draw_contract = get_million_draw()
    million_draw_contract.getRandomness({"from": get_account()})
    time.sleep(200)
    million_draw_contract.getWinner({"from": get_account()})
    print(f"The winner is {million_draw_contract.winner()}")
    million_draw_contract.fundWinner(get_lot_coin(), {"from": get_account()})
