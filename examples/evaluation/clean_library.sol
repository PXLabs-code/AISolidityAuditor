// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

library CleanMathLibraryFixture {
    function min(uint256 left, uint256 right) internal pure returns (uint256) {
        return left < right ? left : right;
    }
}
