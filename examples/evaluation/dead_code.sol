// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DeadCodeFixture {
    function live() external pure returns (uint256) {
        return 1;
    }

    function unusedInternal() internal pure returns (uint256) {
        return 2;
    }
}
