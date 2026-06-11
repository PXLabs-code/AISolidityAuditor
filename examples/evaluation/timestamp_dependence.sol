// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TimestampDependenceFixture {
    function lucky() external view returns (bool) {
        return block.timestamp % 2 == 0;
    }
}
