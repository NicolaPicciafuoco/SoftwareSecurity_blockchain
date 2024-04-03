// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity >=0.6.0 <0.9.0;

// import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
// import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract ChainLog {
    //constructor() ERC20("ChainLog", "MTK") ERC20Permit("ChainLog") {}

    enum ActionType{Create, Update}

    struct Action {
        uint primaryKey;
        address patient;
        address medic;
        ActionType latestAction;
        string hashedData;
    }

    Action[] private terapieLog;             // Array to store all the actions on terapie
    Action[] private prestazioniLog;         // Array to store all the actions on terapie

    // Stores a creation action on the chain

    function createAction(address patient, address medic, uint pk, string calldata hashedData, string calldata choice) public {
        if (keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("Terapia"))) {
            terapieLog.push(Action(pk, patient, medic, ActionType.Create, hashedData));
        } else if (keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("Prestazione"))) {
            prestazioniLog.push(Action(pk, patient, medic, ActionType.Create, hashedData));
        }
    }

    // Stores an update action on the chain
    // TODO: rethink the update action

    function updateAction(address patient, address medic, uint pk, string calldata hashedData, string calldata choice) public {
        if (keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("Terapia"))) {
            for (uint i = 0; i < terapieLog.length; i++) {
                if (terapieLog[i].primaryKey == pk) {
                    terapieLog[i].latestAction = ActionType.Update;
                    terapieLog[i].hashedData = hashedData;
                    return;
                }
            }

        } else if (keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("Prestazione"))) {
            for (uint i = 0; i < prestazioniLog.length; i++) {
                if (prestazioniLog[i].primaryKey == pk) {
                    prestazioniLog[i].latestAction = ActionType.Update;
                    prestazioniLog[i].hashedData = hashedData;
                    return;
                }
            }
        }
    }

    // Deletes a terapia or prestazione from the chain

    function deleteAction(address patient, address medic, uint pk, string calldata hashedData, string calldata choice) public {
        if (keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("Terapia"))) {
            for (uint i = 0; i < terapieLog.length; i++) {
                if (terapieLog[i].primaryKey == pk) {
                terapieLog[i].hashedData = ""; // Rimuovo l'hash
                return;
                }
            }
        } else if (keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("Prestazione"))) {
           for (uint i = 0; i < prestazioniLog.length; i++) {
                if (prestazioniLog[i].primaryKey == pk) {
                    delete prestazioniLog[i];
                    return;
                }
            }
        }
    }

    // Getter functions to retrieve the logs

    function getTerapieLog() public view returns (Action[] memory){
        return terapieLog;
    }

    function getPrestazioniLog() public view returns (Action[] memory){
        return prestazioniLog;
    }



    function getTerapiaByKey(uint pk) public view returns (Action[] memory) {
    Action[] memory matchingActions = new Action[](terapieLog.length);  // Inizializza l'array con la dimensione di terapieLog
    uint counter = 0;
    for (uint i = 0; i < terapieLog.length; i++) {
        if (terapieLog[i].primaryKey == pk) {
            matchingActions[counter] = terapieLog[i];  // Aggiungi l'azione corrispondente all'array
            counter++;
        }
    }
    // Ridimensiona l'array per rimuovere gli spazi vuoti non utilizzati
    assembly { mstore(matchingActions, counter) }
    return matchingActions;
}


     function getPrestazioneByKey(uint pk) public view returns (Action[] memory) {
    Action[] memory matchingActions = new Action[](prestazioniLog.length);  // Inizializza l'array con la dimensione di terapieLog
    uint counter = 0;
    for (uint i = 0; i < prestazioniLog.length; i++) {
        if (prestazioniLog[i].primaryKey == pk) {
            matchingActions[counter] = prestazioniLog[i];  // Aggiungi l'azione corrispondente all'array
            counter++;
        }
    }
    // Ridimensiona l'array per rimuovere gli spazi vuoti non utilizzati
    assembly { mstore(matchingActions, counter) }
    return matchingActions;
}

  /* I hate Solidity so much
    function getPrestazioneByKey(uint pk) public view returns (Action memory){
        for (uint i = 0; i < prestazioniLog.length; i++) {
            if (prestazioniLog[i].primaryKey == pk) {
                return prestazioniLog[i];
            }
        } return false;
    }

    */
}
