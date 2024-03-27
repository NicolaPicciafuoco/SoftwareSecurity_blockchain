// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

// Definizione del contratto
contract TransactionContract {
    // Evento che viene emesso quando viene eseguita una transazione
    event TransactionExecuted(address indexed sender, address indexed recipient, uint256 amount, string message);

    // Funzione per eseguire una transazione da un wallet all'altro
    function executeTransaction(address _recipient, uint256 _amount, string memory _message) external {
        // Verifica che l'importo da trasferire sia maggiore di zero
        require(_amount > 0, "Amount must be greater than zero");

        // Effettua il trasferimento di fondi al destinatario
        payable(_recipient).transfer(_amount);

        // Emetti l'evento TransactionExecuted per indicare che la transazione è stata eseguita
        emit TransactionExecuted(msg.sender, _recipient, _amount, _message);
    }
}