from scripts.helpful_scripts import (
    get_million_draw,
    fund_with_lot,
    fund_with_link,
    join_draw,
)

from brownie import network


def main():
    network.priority_fee("30 gwei")
    million_draw_contract = get_million_draw()
    fund_with_lot(contract_address=million_draw_contract)
    fund_with_link(contract_address=million_draw_contract)
    join_draw(million_draw_contract)
