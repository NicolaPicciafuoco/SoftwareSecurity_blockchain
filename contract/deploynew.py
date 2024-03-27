# import json
# import time
# from web3 import Web3
# from solcx import compile_standard, install_solc
# from web3.middleware import geth_poa_middleware
#
#
# def deploy_contract(utente_wallet_address, utente_private_key, prescrittore_wallet_address, prescrittore_private_key):
#     # Load and compile the Solidity contract
#     with open("./contract/prestazione.sol", "r") as file:
#         prestazione_file = file.read()
#     print("Installing...")
#     install_solc("0.8.0")
#
#     compiled_sol = compile_standard(
#         {
#             "language": "Solidity",
#             "sources": {"prestazione.sol": {"content": prestazione_file}},
#             "settings": {
#                 "outputSelection": {
#                     "*": {
#                         "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
#                     }
#                 }
#             },
#         },
#         solc_version="0.8.0",
#     )
#     with open("./contract/compiled_prestazione.json", "w") as file:
#         json.dump(compiled_sol, file)
#     # Extract bytecode and ABI
#     # Estrai bytecode e ABI
#     bytecode = compiled_sol["contracts"]["prestazione.sol"]["TransferString"]["evm"]["bytecode"]["object"]
#     abi = json.loads(compiled_sol["contracts"]["prestazione.sol"]["TransferString"]["metadata"])["output"]["abi"]
#
#     # Connect to the Ethereum node
#     node_address = "http://rpcnode:8545"  # Replace with your node address
#     chain_id = 1337  # Replace with your chain ID
#
#     w3 = Web3(Web3.HTTPProvider(node_address))
#
#     # Wait for connection
#     max_wait_time = 100
#     start_time = time.time()
#
#     while not w3.is_connected():
#         if time.time() - start_time > max_wait_time:
#             print("Connection to the node timed out.")
#             break
#         time.sleep(1)
#
#     print("Connected to the node.")
#
#     if chain_id == 4:  # Check if it's a PoA network
#         w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#         print(w3.clientVersion)
#
#     # Deploy the contract for utente
#     nonce_utente = w3.eth.get_transaction_count(utente_wallet_address)
#     Prestazione_utente = w3.eth.contract(abi=abi, bytecode=bytecode)
#     transaction_utente = Prestazione_utente.constructor(prescrittore_wallet_address, utente_wallet_address,"Hello, World!").build_transaction(
#         {
#             "chainId": chain_id,
#             "gasPrice": w3.eth.gas_price,
#             "from": utente_wallet_address,
#             "nonce": nonce_utente,
#         })
#     signed_txn_utente = w3.eth.account.sign_transaction(transaction_utente, private_key=utente_private_key)
#     print("Deploying Contract for utente...")
#     tx_hash_utente = w3.eth.send_raw_transaction(signed_txn_utente.rawTransaction)
#     tx_receipt_utente = w3.eth.wait_for_transaction_receipt(tx_hash_utente)
#     contract_address_utente = tx_receipt_utente.contractAddress
#
#     # Deploy the contract for prescrittore
#     nonce_prescrittore = w3.eth.get_transaction_count(prescrittore_wallet_address)
#     Prestazione_prescrittore = w3.eth.contract(abi=abi, bytecode=bytecode)
#     transaction_prescrittore = Prestazione_prescrittore.constructor().build_transaction({
#         "chainId": chain_id,
#         "gasPrice": w3.eth.gas_price,
#         "from": prescrittore_wallet_address,
#         "nonce": nonce_prescrittore,
#     })
#     signed_txn_prescrittore = w3.eth.account.sign_transaction(transaction_prescrittore,
#                                                               private_key=prescrittore_private_key)
#     print("Deploying Contract for prescrittore...")
#     tx_hash_prescrittore = w3.eth.send_raw_transaction(signed_txn_prescrittore.rawTransaction)
#     tx_receipt_prescrittore = w3.eth.wait_for_transaction_receipt(tx_hash_prescrittore)
#     contract_address_prescrittore = tx_receipt_prescrittore.contractAddress
#
#     print(f"Contract deployed for utente to address: {contract_address_utente}")
#     print(f"Contract deployed for prescrittore to address: {contract_address_prescrittore}")
#
# # Utilizzare questa funzione passando l'indirizzo del portafoglio e la chiave privata
# # ad esempio:
# # deploy_contract("0x6aABE487828603b6f0a3E1C7DAcF7F42bA42A9B2", "8a63f5a3608d032ba652a323d62f333f71a895d253d6aa9f5defc16a43e4d7f1", "0xPrescrittoreAddress", "8a63f5a3608d032ba652a323d62f333f71a895d253d6aa9f5defc16a43e4d7f1")
