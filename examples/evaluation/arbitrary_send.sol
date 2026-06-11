// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ArbitrarySendFixture {
    receive() external payable {}

    function sendAll(address payable recipient) external {
        recipient.transfer(address(this).balance);
    }
}
