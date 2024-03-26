// Definizione del contratto
pragma solidity ^0.6.0;

// Dichiarazione del contratto
contract HashContract {
    // Dichiarazione della stringa predefinita
    string public fixedString;

    // Evento di registro contenente la stringa predefinita
    event FixedStringSet(string fixedString);

    // Costruttore del contratto
    constructor() public {
        // Imposta la stringa predefinita
        fixedString = "Questo sarà il tuo hash";

        // Emetti l'evento di registro
        emit FixedStringSet(fixedString);
    }

    // Funzione per restituire la stringa predefinita
    function getFixedString() public view returns (string memory) {
        // Restituisci la stringa predefinita
        return fixedString;
    }
}
