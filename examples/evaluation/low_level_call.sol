// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LowLevelCallFixture {
    function forward(address target, bytes calldata data) external {
        (bool ok,) = target.call(data);
        require(ok, "call failed");
    }
}
