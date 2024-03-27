// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TransferString {
    address public fromAccount;
    address public toAccount;
    string public transferMessage;

    constructor(address _fromAccount, address _toAccount, string memory _transferMessage) {
        fromAccount = _fromAccount;
        toAccount = _toAccount;
        transferMessage = _transferMessage;
    }

    function updateTransferMessage(string memory _newMessage) public {
        require(msg.sender == fromAccount, "Only the sender can update the transfer message");
        transferMessage = _newMessage;
    }

    function getTransferDetails() public view returns (string memory) {
        return transferMessage;
    }
}
