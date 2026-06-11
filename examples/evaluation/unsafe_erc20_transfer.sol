// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20Like {
    function transfer(address recipient, uint256 amount) external returns (bool);
}

contract UnsafeErc20TransferFixture {
    function payout(IERC20Like token, address recipient, uint256 amount) external {
        token.transfer(recipient, amount);
    }
}
