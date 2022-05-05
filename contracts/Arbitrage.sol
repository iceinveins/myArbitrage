// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../interfaces/IERC20.sol";
import "../interfaces/ISwapRouter.sol";
import "../interfaces/IUniswapV3Factory.sol";
import "../interfaces/IUniswapV3Pool.sol";
import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router01.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

// refactor to add reetrancyguard
contract Arbitrage is Ownable{
    using SafeMath for uint256;

    address public uniswapRouterAddress;
    address public uniswapFactoryAddress;
    address public sushiswapRouterAddress;
    address public wethAddress;
    address public daiAddress;

    uint256 public funds;  // wei
    uint24 public constant poolFee = 3000;

    constructor(
        address _uniswapRouterAddress,
        address _uniswapFactoryAddress,
        address _sushiswapRouterAddress,
        address _weth,
        address _dai
    ) {
        uniswapRouterAddress = _uniswapRouterAddress;
        uniswapFactoryAddress = _uniswapFactoryAddress;
        sushiswapRouterAddress = _sushiswapRouterAddress;
        wethAddress = _weth;
        daiAddress = _dai;
    }

    function deposit(uint256 amount) external onlyOwner {
        require(amount > 0, "Deposit amount must be greater than 0");
        IERC20(wethAddress).transferFrom(msg.sender, address(this), amount);
        funds += amount;
    }

    function withdraw(uint256 amount) external onlyOwner {
        require(amount <= funds, "Not enough amount deposited");
        IERC20(wethAddress).transferFrom(address(this), msg.sender, amount);
        funds -= amount;
    }
    function getDeadline() public view returns (uint256){
        return block.timestamp+60;
    }

    // function _swapByUniV3(
    //     uint256 amountIn,
    //     address sell_token,
    //     address buy_token
    // ) internal returns (uint256) {
    //     IERC20(sell_token).approve(_uniswapRouterAddress, amountIn);

    //     ISwapRouter.ExactInputSingleParams memory params =
    //         ISwapRouter.ExactInputSingleParams({
    //             tokenIn: sell_token,
    //             tokenOut: buy_token,
    //             fee: poolfee,
    //             recipient: address(this),
    //             deadline: getDeadline(),
    //             amountIn: amountIn,
    //             amountOutMinimum: 0,
    //             sqrtPriceLimitX96: 0
    //     });

    //     uint256 amountOut = ISwapRouter(_uniswapRouterAddress).exactInputSingle(params);
    //     return amountOut;
    // }

    function _getUniPrice(
        address sell_token,
        address buy_token
    ) public view returns (uint256) {  // todo: internal
        IUniswapV3Pool pool = IUniswapV3Pool(IUniswapV3Factory(uniswapFactoryAddress)
            .getPool(sell_token, buy_token, poolFee));
        (uint160 sqrtPriceX96,,,,,,) =  pool.slot0();
        return uint(sqrtPriceX96).mul(uint(sqrtPriceX96)) >> (96 * 2);
    }

    function _getSushiPrice(
        address sell_token,
        address buy_token,
        uint256 amount
    ) public view returns (uint256) { // todo: internal
        address[] memory pairs = new address[](2);
        pairs[0] = sell_token;
        pairs[1] = buy_token;
        uint256 price = IUniswapV2Router01(sushiswapRouterAddress).getAmountsOut(
            amount,
            pairs
        )[1];
        return price;
    }
}
