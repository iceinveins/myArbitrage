from scripts.helper import get_account, toWei, fromWei, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.get_weth import get_weth
from brownie import accounts, network

def test_get_account():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pass
    else:
        get_account() == accounts[0]
        for num in range(0, 9):
            assert get_account(num) == accounts[num]

def test_get_weth():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pass
    else:    
        account = get_account()
        initBalance = account.balance()
        amount = 7
        get_weth(account, amount)
        assert fromWei(initBalance) - amount == fromWei(account.balance())