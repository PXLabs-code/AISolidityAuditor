// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IncorrectEqualityFixture {
    receive() external payable {}

    function exactMatch(uint256 target) external view returns (bool) {
        return address(this).balance == target;
    }
}
