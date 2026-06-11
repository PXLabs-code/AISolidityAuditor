// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

contract IntegerIssueFixture {
    mapping(address => uint256) public balances;

    function addBalance(uint256 amount) external {
        balances[msg.sender] += amount;
    }
}
