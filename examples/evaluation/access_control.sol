// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControlFixture {
    address public owner;

    function setOwner(address newOwner) external {
        owner = newOwner;
    }
}
