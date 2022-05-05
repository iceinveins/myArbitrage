from brownie import config, network, accounts, Contract, interface
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "mainnet-fork"]

def get_account(index=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if index is not None:
            return accounts[index]
        else:
            return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def toWei(amount):
    return Web3.toWei(amount, "ether")

def fromWei(amount):
    return Web3.fromWei(amount, "ether")

def approve_erc20(amount, spender, erc20_address, account):
    erc20 = interface.IERC20(erc20_address)
    approve_tx = erc20.approve(spender, amount, {"from": account})
    approve_tx.wait(1)
    print("----- ERC20 Approved! -----")