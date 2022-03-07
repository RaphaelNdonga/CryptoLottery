from scripts.helpful_scripts import (
    get_million_draw,
    fund_with_lot,
    fund_with_link,
    join_draw,
)


def main():
    million_draw_contract = get_million_draw()
    fund_with_lot(contract_address=million_draw_contract)
    fund_with_link(contract_address=million_draw_contract)
    join_draw(million_draw_contract)
