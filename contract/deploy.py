import json

from web3 import Web3

from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
# from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

# load_dotenv()     Non necessario dato che non usiamo Infuria

import time


with open("./contract/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.8.0")

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
    solc_version="0.8.0",
)

with open("./contract/compiled_code.json", "w") as file:
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
node_address = "http://rpcnode:8545"
chain_id = 1337

# Inizializza un oggetto Web3 con l'indirizzo IP del nodo Besu
w3 = Web3(Web3.HTTPProvider(node_address))

# Imposta il tempo massimo di attesa in secondi
max_wait_time = 100
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
print("primo contratto fatto")
# provo il secondo
#
# with open("./contract/provahash.sol", "r") as file:
#     provahash_file = file.read()
#
# # Compila il contratto Solidity
# compiled_sol = compile_standard(
#     {
#         "language": "Solidity",
#         "sources": {"provahash.sol": {"content": provahash_file}},
#         "settings": {
#             "outputSelection": {
#                 "*": {
#                     "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
#                 }
#             }
#         },
#     },
#     solc_version="0.6.0",
# )
#
# # Salva i contratti compilati in un file JSON
# with open("./contract/compiled_provahash.json", "w") as file:
#     json.dump(compiled_sol, file)
#
# # Ottieni il bytecode e l'ABI del contratto
# bytecode = compiled_sol["contracts"]["provahash.sol"]["HashContract"]["evm"]["bytecode"]["object"]
# abi = json.loads(compiled_sol["contracts"]["provahash.sol"]["HashContract"]["metadata"])["output"]["abi"]
#
# # Connessione al nodo Ethereum
#
# # Attendi che il nodo si connetta
#
# # Middleware per la Proof of Authority (PoA) se necessario
#
# # Indirizzo e chiave privata dell'account che effettua il deploy
#
#
# # Creazione del contratto in Python
# ProvahashContract = w3.eth.contract(abi=abi, bytecode=bytecode)
#
# # Ottieni il nonce più recente
# nonce = w3.eth.get_transaction_count(my_address)
#
# # Costruisci la transazione per il deploy del contratto
# transaction = ProvahashContract.constructor().build_transaction({
#     "chainId": chain_id,
#     "gasPrice": w3.eth.gas_price,
#     "from": my_address,
#     "nonce": nonce,
# })
#
# # Firma la transazione
# signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print("Deploying Contract!")
#
# # Invia la transazione
# tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#
# # Attendi che la transazione venga inclusa nel blocco e ottieni il receipt della transazione
# print("Waiting for transaction to finish...")
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
# print()
# # Lavoro con i contratti deployati
# provahash_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#
# # Esempio di utilizzo: recupera la stringa fissa dal contratto
# print(f"Fixed String: {provahash_contract.functions.getFixedString().call()}")
# print("ciao a tutti provahash")







# PROVO TRANSAZIONE


with open("./contract/TransactionContract.sol", "r") as file:
    TransactionContract_file = file.read()

# Compila il contratto Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"TransactionContract.sol": {"content": TransactionContract_file}},
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

# Salva i contratti compilati in un file JSON
with open("./contract/compiled_TransactionContract.json", "w") as file:
    json.dump(compiled_sol, file)

# Ottieni il bytecode e l'ABI del contratto
bytecode = compiled_sol["contracts"]["TransactionContract.sol"]["TransactionContract"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["TransactionContract.sol"]["TransactionContract"]["metadata"])["output"]["abi"]


# Creazione del contratto in Python
TransactionContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Ottieni il nonce più recente
nonce = w3.eth.get_transaction_count(my_address)

# Costruisci la transazione per il deploy del contratto
transaction = TransactionContract.constructor().build_transaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": nonce,
})

# Firma la transazione
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")

# Invia la transazione
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Attendi che la transazione venga inclusa nel blocco e ottieni il receipt della transazione
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
print("fattooooo il secondo")
# # Lavoro con i contratti deployati
# provahash_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#
# # Esempio di utilizzo: recupera la stringa fissa dal contratto
# print(f"Fixed String: {provahash_contract.functions.getFixedString().call()}")
# print("ciao a tutti provahash")