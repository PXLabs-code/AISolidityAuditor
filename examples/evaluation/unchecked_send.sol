// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UncheckedSendFixture {
    receive() external payable {}

    function payout(address payable recipient) external {
        recipient.send(address(this).balance);
    }
}
