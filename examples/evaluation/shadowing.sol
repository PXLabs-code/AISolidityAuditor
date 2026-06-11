// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ShadowingFixture {
    uint256 public value;

    function set(uint256 value) external {
        value = value + 1;
    }
}
