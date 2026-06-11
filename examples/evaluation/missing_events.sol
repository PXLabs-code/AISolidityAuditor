// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MissingEventsFixture {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function setOwner(address newOwner) external {
        owner = newOwner;
    }
}
