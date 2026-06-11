// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MissingZeroConstructorFixture {
    address public owner;

    constructor(address initialOwner) {
        owner = initialOwner;
    }
}
