// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TxOriginFixture {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function drain(address payable target) external {
        require(tx.origin == owner, "not owner");
        target.transfer(address(this).balance);
    }
}
