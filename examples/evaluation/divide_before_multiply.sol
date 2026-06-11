// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DivideBeforeMultiplyFixture {
    function prorata(uint256 amount, uint256 numerator, uint256 denominator) external pure returns (uint256) {
        return amount / denominator * numerator;
    }
}
