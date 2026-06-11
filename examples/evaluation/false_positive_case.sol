// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FalsePositiveCaseFixture {
    mapping(address => uint256) public balances;

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        balances[msg.sender] = 0;
        (bool ok,) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
    }
}
