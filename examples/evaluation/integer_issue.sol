// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract IntegerIssueFixture {
    mapping(address => uint256) public balances;

    function addBalance(uint256 amount) external {
        balances[msg.sender] += amount;
    }
}
