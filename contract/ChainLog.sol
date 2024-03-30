// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity >=0.6.0 <0.9.0;

// import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
// import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract ChainLog {
    //constructor() ERC20("ChainLog", "MTK") ERC20Permit("ChainLog") {}

    enum ActionType{Create, Read, Update, Delete}

    struct Action {
        address patient;
        address medic;
        ActionType actionType;
        string transactionHash;
        bytes encryptedData;
    }

    Action[] private log;  // Array to store all the actions

    // Dummy function to process a transaction

    function processTransaction() public returns (bool){
        return true;
    }

    // Stores a creation action on the chain

    function createAction(address patient, address medic, string calldata hash, bytes calldata encryptedData) public {
        Action memory newAction = Action(patient, medic, ActionType.Create, hash, encryptedData);
        log.push(newAction);
    }

    // Checks if a transaction is stored on the chain and adds a new action with the Delete type

    function deleteAction(address patient, address medic, string calldata hash, bytes calldata encryptedData) public
                            returns (string memory) {
        for (uint i = 0; i < log.length; i++) {
            if (keccak256(abi.encodePacked(log[i].transactionHash)) == keccak256(abi.encodePacked(hash))) {
                if (log[i].medic != medic) {
                    return "Unauthorized";
                } else {
                    Action memory newAction = Action(patient, medic, ActionType.Delete, hash, encryptedData);
                    log.push(newAction);
                    return "Found";
                }
            }
        } return "Not Found";
    }

    // Checks if a transaction is present in the logs and whether the requester is authorized to read it
    // or it has been deleted

    function readAction(address patient, address medic, string calldata hash, bytes calldata encryptedData) public
                            returns (string memory) {
        for (uint i = log.length; i > 0; i--) {
            if (keccak256(abi.encodePacked(log[i].transactionHash)) == keccak256(abi.encodePacked(hash))) {
                if (log[i].actionType == ActionType.Delete) {
                    return "Deleted";
                } else if (log[i].medic != medic && log[i].patient != patient) {
                    return "Unauthorized";
                } else {
                    Action memory newAction = Action(patient, medic, ActionType.Read, hash, encryptedData);
                    log.push(newAction);
                    return "Found";
                }
            }
        }
        return "Not Found";
    }

    // Checks if a transaction is present in the logs and whether the requester is authorized to update it
    // or it has been deleted

    function updateAction(address patient, address medic, string calldata hash, bytes calldata encryptedData) public
                                returns (string memory) {
        for (uint i = log.length; i > 0; i--) {
            if (keccak256(abi.encodePacked(log[i].transactionHash)) == keccak256(abi.encodePacked(hash))) {
                if (log[i].actionType == ActionType.Delete) {
                    return "Deleted";
                } else if (log[i].medic != medic) {
                    return "Unauthorized";
                } else {
                    Action memory newAction = Action(patient, medic, ActionType.Update, hash, encryptedData);
                    log.push(newAction);
                    return "Found";
                }
            }
        } return "Not Found";
    }

    // Getter function to retrieve the log

    function getLog() public view returns(Action[] memory){
        return log;
    }

}