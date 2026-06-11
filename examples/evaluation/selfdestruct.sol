// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SelfdestructFixture {
    address payable public owner;

    constructor() {
        owner = payable(msg.sender);
    }

    function destroy(address payable recipient) external {
        owner = recipient;
        selfdestruct(owner);
    }
}
