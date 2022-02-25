from brownie import Contract, accounts,config,network,LotCoin,MillionDraw,LinkToken
from web3 import Web3

LOCAL_BLOCKCHAIN=["development","mainnet-fork"]

def get_account(index=None,id=None):
    account = None
    if index:
        account = accounts[index]
    if id:
        account = accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN:
        account = accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])
    return account

def get_lot_coin():
    contract_address = config["networks"][network.show_active()]["lot_coin"]
    lot_coin = Contract.from_abi(LotCoin._name,contract_address,LotCoin.abi)
    return lot_coin

def get_million_draw():
    contract_address = config["networks"][network.show_active()]["million_draw"]
    million_draw = Contract.from_abi(MillionDraw._name,contract_address,MillionDraw.abi)
    return million_draw

def get_link():
    contract_address = config["networks"][network.show_active()]["link"]
    link = Contract.from_abi(LinkToken._name,contract_address,LinkToken.abi)
    return link

def fund_with_lot(contract_address,account=None,lot_coin=None,entryFee=Web3.toWei(1000,"ether")):
    account =  account if account else get_account()
    lot_coin = lot_coin if lot_coin else get_lot_coin()
    tx = lot_coin.transfer(contract_address,entryFee,{"from":account})
    tx.wait(1)
    print(f"contract {contract_address} funded {entryFee} with lot")
    return tx

def fund_with_link(contract_address,account=None,link=None,link_fee=Web3.toWei(0.0001,"ether")):
    account = account if account else get_account()
    link = link if link else get_link()
    tx = link.transfer(contract_address,link_fee,{"from":account})
    tx.wait(1)
    print(f"contract {contract_address} funded {link_fee} with link")
    return tx

def join_draw(million_draw_address,account=None):
    account = account if account else get_account()
    tx = million_draw_address.joinDraw({"from":account})
    tx.wait(1)
    num_participants = million_draw_address.getParticipantsNum()
    for i in range(num_participants):
        print(f"participant {i+1} {million_draw_address.participants(i)}")
    return tx