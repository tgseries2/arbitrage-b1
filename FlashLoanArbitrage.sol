// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IUniswapV2Router {
    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);
}

contract FlashLoanArbitrage {
    address private owner;
    address private constant UNISWAP_ROUTER = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant SUSHISWAP_ROUTER = 0xd9e1CE17F2641f24aE83637ab66a2cca9C378B9F;

    constructor() {
        owner = msg.sender;
    }

    function executeArbitrage(address token, uint amount) external {
        require(msg.sender == owner, "Not owner");

        uint uniswapPrice = getPrice(UNISWAP_ROUTER, token, amount);
        uint sushiswapPrice = getPrice(SUSHISWAP_ROUTER, token, amount);

        if (uniswapPrice > sushiswapPrice) {
            swap(UNISWAP_ROUTER, SUSHISWAP_ROUTER, token, amount);
        } else if (sushiswapPrice > uniswapPrice) {
            swap(SUSHISWAP_ROUTER, UNISWAP_ROUTER, token, amount);
        }
    }

    function getPrice(address router, address token, uint amount) private view returns (uint) {
        IUniswapV2Router uniRouter = IUniswapV2Router(router);
        address;
        path[0] = token;
        path[1] = 0xC02aaa39b223FE8D0A0E5C4F27eAD9083C756Cc2; // WETH

        uint[] memory amounts = uniRouter.swapExactTokensForTokens(amount, 1, path, address(this), block.timestamp);
        return amounts[1];
    }

    function swap(address fromRouter, address toRouter, address token, uint amount) private {
        IERC20(token).approve(fromRouter, amount);
        uint receivedAmount = getPrice(fromRouter, token, amount);
        
        IERC20(token).approve(toRouter, receivedAmount);
        getPrice(toRouter, token, receivedAmount);
    }
}
