// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UninitializedLocalFixture {
    function read() external pure returns (uint256) {
        uint256 value;
        return value;
    }
}
