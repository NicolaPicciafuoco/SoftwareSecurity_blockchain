import json

from web3 import Web3

# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
import time


class ContractInteractions:

    node_address = "http://rpcnode:8545"
    w3 = Web3(Web3.HTTPProvider(node_address))
    chain_id = 1337
    ChainLog = None

    def load_contract(self):

        # Loads the already-compiled contract

        with open("./contract/compiled_code.json", "r") as file:
            compiled_sol = json.load(file)
        abi = json.loads(compiled_sol["contracts"]["ChainLog.sol"]["ChainLog"]["metadata"])["output"]["abi"]
        self.ChainLog = self.w3.eth.contract(abi=abi)
        with open("./contract/contract_address.txt", "r") as file:
            contract_address = file.read()
        self.ChainLog = self.w3.eth.contract(address=contract_address, abi=abi)
        return self.ChainLog

    def __init__(self):
        load_dotenv()
        self.my_address = os.getenv("ADMIN_ADDRESS")
        self.private_key = os.getenv("ADMIN_PRIVATE_KEY")
        self.load_contract()

    def deploy(self):

        # Load the contract source code
        with open("./contract/ChainLog.sol", "r") as file:
            chain_log_file = file.read()

        # We add these two lines that we forgot from the video!
        print("Installing...")
        install_solc("0.8.0")

        # Solidity source code
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"ChainLog.sol": {"content": chain_log_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                        }
                    }
                },
            },
            solc_version="0.8.0",
        )

        with open("./contract/compiled_code.json", "w") as file:
            json.dump(compiled_sol, file)

        # get bytecode
        bytecode = compiled_sol["contracts"]["ChainLog.sol"]["ChainLog"]["evm"][
            "bytecode"
        ]["object"]

        # get abi
        abi = json.loads(
            compiled_sol["contracts"]["ChainLog.sol"]["ChainLog"]["metadata"]
        )["output"]["abi"]

        # Imposta il tempo massimo di attesa in secondi
        max_wait_time = 300
        start_time = time.time()

        # Loop fino a quando il nodo non si connette o fino a quando non superi il tempo massimo di attesa
        while not self.w3.is_connected():
            if time.time() - start_time > max_wait_time:
                print("Il nodo non si è connesso entro il tempo massimo di attesa.")
                break
            time.sleep(1)  # Attendi 1 secondo prima di riprovare la connessione
        print("Il nodo si è connesso")

        if self.chain_id == 4:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            print(self.w3.client_version)

        # Added print statement to ensure connection succeeded as per
        # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority

        # my_address = "0x6aABE487828603b6f0a3E1C7DAcF7F42bA42A9B2"
        # private_key = "8a63f5a3608d032ba652a323d62f333f71a895d253d6aa9f5defc16a43e4d7f1"

        # Create the contract in Python
        ChainLog = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        nonce = self.w3.eth.get_transaction_count(self.my_address, 'pending')

        # Submit the transaction that deploys the contract
        transaction = ChainLog.constructor().build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.my_address,
                "nonce": nonce,
            }
        )

        # Sign the transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        print("Deploying Contract!")
        # Send it!
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined, and get the transaction receipt

        print("Waiting for transaction to finish...")

        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
        with open("./contract/contract_address.txt", "w") as file:
            file.write(tx_receipt.contractAddress)

    # Function to interact with the contract

    def log_action(self, patient, medic, action_type, medic_key, encrypted_data):
        # Building, signing and sending the transaction

        nonce = self.w3.eth.get_transaction_count(medic)

        # Costruisci la transazione manualmente
        transaction = {
            'to': self.ChainLog.address,
            'from': medic,
            'nonce': nonce,
            'gasPrice': self.w3.eth.gas_price,
            'gas': 1000000,  # Definisci il limite di gas
            'data': self.ChainLog.encodeABI(fn_name="createAction", args=[patient, medic, action_type, encrypted_data]),
        }

        # Firma la transazione
        signed_transaction = self.w3.eth.account.sign_transaction(transaction, private_key=medic_key)

        # Invia la transazione firmata
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Attendere che la ricevuta della transazione sia disponibile
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)

        # Decodifica l'hash della transazione
        action_hash = tx_receipt.transactionHash.hex()

        if action_type == "Create":
            self.ChainLog.functions.createAction(patient, medic, action_hash, encrypted_data).call()

            return action_hash
        elif action_type == "Update":
            results = self.ChainLog.functions.updateAction(patient, medic, action_hash, encrypted_data).call()
            if  results == "Found":
                return action_hash
            else:
                return results
        elif action_type == "Delete":
            results = self.ChainLog.functions.deleteAction(patient, medic, action_hash, encrypted_data).call()
            if results == "Found":
                return action_hash
            else:
                return results
        elif action_type == "Read":
            results = self.ChainLog.functions.readAction(patient, medic, action_hash, encrypted_data).call()
            if results == "Found":
                return action_hash
            else:
                return results
        return False

    def get_action_log(self):
        # Returns the action log from the contract

        logs = self.ChainLog.functions.getLog().call()
        return logs

''' Commentato per ora
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
greeting_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
'''
