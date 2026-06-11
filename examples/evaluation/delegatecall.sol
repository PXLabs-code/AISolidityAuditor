// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DelegatecallFixture {
    function execute(address target, bytes calldata data) external {
        (bool ok,) = target.delegatecall(data);
        require(ok, "delegatecall failed");
    }
}
