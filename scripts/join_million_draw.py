from scripts.helpful_scripts import (
    get_million_draw,
    fund_with_lot,
    join_draw,
    POLYGON_NETWORKS,
)

from brownie import network


def main():
    if network.show_active() in POLYGON_NETWORKS:
        network.priority_fee("30 gwei")
    million_draw_contract = get_million_draw()
    fund_with_lot(contract_address=million_draw_contract)
    join_draw(million_draw_contract)
