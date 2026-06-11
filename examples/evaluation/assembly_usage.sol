// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AssemblyUsageFixture {
    function caller() external view returns (address result) {
        assembly {
            result := caller()
        }
    }
}
