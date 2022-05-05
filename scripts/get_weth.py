from mmap import ACCESS_COPY
from brownie import network, interface, config, web3
from scripts.helper import get_account
from web3 import Web3



def get_weth(account, amount):
    weth_address = config["networks"][network.show_active()]["weth_token"]

    weth = interface.IWeth(weth_address)

    deposit_tx = weth.deposit({"from": account, "value": Web3.toWei(amount, "ether")})
    deposit_tx.wait(1)

    print(f"Received {amount} WETH")

