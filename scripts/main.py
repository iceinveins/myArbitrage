from brownie import config, network, Arbitrage
from scripts.helper import get_account, toWei, fromWei, LOCAL_BLOCKCHAIN_ENVIRONMENTS, approve_erc20
from scripts.get_weth import get_weth


weth_token = config["networks"][network.show_active()]["weth_token"]
dai_token = config["networks"][network.show_active()]["dai_token"]

uni_router_address = config["networks"][network.show_active()]["uniswap_router"]
uni_factory_address = config["networks"][network.show_active()]["uniswap_factory"]
sushi_router_address = config["networks"][network.show_active()]["sushiswap_router"]

def main():
    account = get_account()

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        get_weth(account, 10)
    
    arbitrage = Arbitrage.deploy(
        uni_router_address,
        uni_factory_address,
        sushi_router_address,
        weth_token,
        dai_token,
        {"from": account}
    )
    print("-----Arbitrage deployed! -----")

    # amount = toWei(5)
    # approve_erc20(amount, arbitrage.address, weth_token, account)
    # deposit_tx = arbitrage.deposit(amount, {"from": account})
    # deposit_tx.wait(1)

    # print("-----Amount deposited: ", fromWei(arbitrage.funds()), "-----")

    # arbitrage_tx = arbitrage.makeArbitrage({"from": account})
    # arbitrage_tx.wait(1)
    
    # print("New amount: ", fromWei(arbitrage.funds()))
    
    print(" UniSwap Price ", arbitrage._getUniPrice(weth_token, dai_token))
    print(" SushiSwap Price ", arbitrage._getSushiPrice(weth_token, dai_token, 1))
    