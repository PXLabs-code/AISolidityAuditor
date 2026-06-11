// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CleanContractFixture {
    address public owner;
    uint256 public value;

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setValue(uint256 newValue) external onlyOwner {
        value = newValue;
    }
}
