import json

from web3 import Web3

# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
# from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

# load_dotenv()     Non necessario dato che non usiamo Infuria

import time
# time.sleep(20) # Sleep for 20 seconds, serve per aspettare a prendere il nodo




with open("./contract/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]
#
# # w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
# # chain_id = 4
# #
# # For connecting to ganache
# w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
# chain_id = 1337
#
# if chain_id == 4:
#     w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#     print(w3.clientVersion)
# w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
# chain_id = 4
#
# For connecting to Besu
# w3 = Web3(Web3.HTTPProvider("http://172.16.239.15:8545"))  # Sostituisci con l'indirizzo IP del nodo Besu
# chain_id = 1337
node_address = "http://172.16.239.15:8545"
chain_id = 1337

# Inizializza un oggetto Web3 con l'indirizzo IP del nodo Besu
w3 = Web3(Web3.HTTPProvider(node_address))

# Imposta il tempo massimo di attesa in secondi
max_wait_time = 300
start_time = time.time()

# Loop fino a quando il nodo non si connette o fino a quando non superi il tempo massimo di attesa
while not w3.is_connected():
    if time.time() - start_time > max_wait_time:
        print("Il nodo non si è connesso entro il tempo massimo di attesa.")
        break
    time.sleep(1)  # Attendi 1 secondo prima di riprovare la connessione
print("il nodo si è connesso")



if chain_id == 4:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(w3.clientVersion)
#Added print statement to ensure connection suceeded as per
#https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority

my_address = "0x6aABE487828603b6f0a3E1C7DAcF7F42bA42A9B2"
private_key = "8a63f5a3608d032ba652a323d62f333f71a895d253d6aa9f5defc16a43e4d7f1"

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
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
