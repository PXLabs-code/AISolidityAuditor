// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PublicInitializerFixture {
    address public owner;
    bool public initialized;

    function initialize(address newOwner) public {
        require(!initialized, "initialized");
        owner = newOwner;
        initialized = true;
    }
}
