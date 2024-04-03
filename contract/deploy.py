import json
import os
import time
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
# from web3.middleware import geth_poa_middleware



class ContractInteractions:

    node_address = "http://rpcnode:8545"
    w3 = Web3(Web3.HTTPProvider(node_address))
    chain_id = 1337
    ChainLog = None

    # Loads the already-compiled contract

    def load_contract(self):

        # Checks if the compiled code and the contract address files exist

        if os.path.exists("./contract/compiled_code.json"):
            with open("./contract/compiled_code.json", "r", encoding="utf-8") as file:
                compiled_sol = json.load(file)
            abi = json.loads(compiled_sol["contracts"]["ChainLog.sol"]["ChainLog"]["metadata"])["output"]["abi"]
            self.ChainLog = self.w3.eth.contract(abi=abi)
        if os.path.exists("./contract/contract_address.txt"):
            with open("./contract/contract_address.txt", "r", encoding="utf-8") as file:
                contract_address = file.read()
            self.ChainLog = self.w3.eth.contract(address=contract_address, abi=abi)

    def __init__(self):
        load_dotenv()
        self.my_address = os.getenv("ADMIN_ADDRESS")
        self.private_key = os.getenv("ADMIN_PRIVATE_KEY")
        self.load_contract()

    # Function that deploys the contract. Only ran once on startup

    def deploy(self):

        # Load the contract source code
        with open("./contract/ChainLog.sol", "r", encoding="utf-8") as file:
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

        with open("./contract/compiled_code.json", "w", encoding="utf-8") as file:
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

        # Non ci serve il PoA middleware
        #
        # if self.chain_id == 4:
        #     self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        #     print(self.w3.client_version)

        # Added print statement to ensure connection succeeded as per
        # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority

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
        with open("./contract/contract_address.txt", "w", encoding="utf-8") as file:
            file.write(tx_receipt.contractAddress)

    # Function to interact with the contract

    def log_action(self, pk, patient, medic, action_type, medic_key, hashed_data, choice):
        # Building, signing and sending the transaction

        nonce = self.w3.eth.get_transaction_count(medic)
        call_data = None

        if action_type == "Create":
            call_data = self.ChainLog.encodeABI(fn_name="createAction", args=[patient,
                                                                              medic,
                                                                              pk,
                                                                              hashed_data,
                                                                              choice])
        elif action_type == "Update":
            call_data = self.ChainLog.encodeABI(fn_name="updateAction", args=[patient,
                                                                              medic,
                                                                              pk,
                                                                              hashed_data,
                                                                              choice])
        elif action_type == "Delete":
            call_data = self.ChainLog.encodeABI(fn_name="deleteAction", args=[patient,
                                                                              medic,
                                                                              pk,
                                                                              hashed_data,
                                                                              choice])
        elif action_type == "Read":
            call_data = self.ChainLog.encodeABI(fn_name="readAction", args=[patient,
                                                                            medic,
                                                                            pk,
                                                                            hashed_data,
                                                                            choice])

        # Costruisci la transazione manualmente
        transaction = {
            'to': self.ChainLog.address,
            'from': medic,
            'nonce': nonce,
            'gasPrice': self.w3.eth.gas_price,
            'gas': 1000000,  # Definisci il limite di gas
            'data': call_data,
        }
        
        # Firma la transazione
        signed_transaction = self.w3.eth.account.sign_transaction(transaction, private_key=medic_key)

        # Invia la transazione firmata
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Attendere che la ricevuta della transazione sia disponibile
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_hash.hex()

    # Function to get the action log from the contract

    def get_action_log(self, choice):
        # Returns the action log from the contract
        logs = None
        if choice == "Terapia":
            logs = self.ChainLog.functions.getTerapieLog().call()
        elif choice == "Prestazione":
            logs = self.ChainLog.functions.getPrestazioniLog().call()
        return logs

    # def get_action_by_key(self, key, choice):
    #     # Returns the log by key
    #     action = None
    #     if choice == "Terapia":
    #         action = self.ChainLog.functions.getTerapiaByKey(key).call()
    #     elif choice == "Prestazione":
    #         action = self.ChainLog.functions.getPrestazioneByKey(key).call()
    #     return action

    # Function to get the desired action based on the given key
    def get_action_by_key(self, key, choice):
        # Returns the log by key
        actions = []
        if choice == "Terapia":
            actions = self.ChainLog.functions.getTerapiaByKey(key).call()
        elif choice == "Prestazione":
            actions = self.ChainLog.functions.getPrestazioneByKey(key).call()
        return actions
