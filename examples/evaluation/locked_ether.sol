// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LockedEtherFixture {
    receive() external payable {}

    function balance() external view returns (uint256) {
        return address(this).balance;
    }
}
