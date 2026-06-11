// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UnusedReturnFixture {
    function tokenCall(address token, bytes calldata data) external {
        token.call(data);
    }
}
