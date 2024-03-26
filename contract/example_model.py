"""
Esempio di script per la generazione di smart contract
SimpleCounter.sol deve risiedere nella directory dello script
"""
import random
import string
import time

from django.db import models
from web3 import Web3
from solcx import compile_source
import os
import json
# Solidity source code
DEFAULT_SOURCE_CODE_NAME: str = "SimpleCounter.sol"
DEFAULT_SOURCE_CODE: str = '''
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Counter {
    uint256 public count;

    constructor() {
        count = 0;
    }

    function increment() public {
        count++;
    }
}
'''


def get_time_plus_random_str() -> str:
    timestamp = int(time.time())
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"{timestamp}_{random_string}"


def generate_smart_contract_filename() -> str:
    return f"SmartContract_{get_time_plus_random_str()}.sol"


def __create_contract_file(
        contract_file_path: str | None = os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_SOURCE_CODE_NAME),
        contract_source_code: str | None = DEFAULT_SOURCE_CODE,
        contract_name: str | None = generate_smart_contract_filename()) -> str:

    if contract_file_path is None and contract_name is not None:
        contract_file_path = os.path.join(contract_file_path, contract_name)
    with open(contract_file_path, "w") as file:
        file.write(contract_source_code)
        file.flush()
    if not os.path.exists(os.path.join(contract_file_path, contract_name)):
        raise FileNotFoundError


def _get_or_create_contract_file(contract_file_path: str | None = os.path.dirname(os.path.abspath(__file__))):
    try:
        with open(contract_file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        with open(__create_contract_file(), "r") as file:
            return file.read()
    except Exception as e:
        print(e)


class MyModel(models.Model):
    count = models.PositiveIntegerField(default=0)

    @classmethod
    async def increment_counter(cls):
        web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Update with your Besu RPC endpoint
        web3.eth.default_account = web3.eth.accounts[0]  # Set default account to use for transactions

        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        contract_file_path = os.path.join(current_dir, DEFAULT_SOURCE_CODE_NAME)

        contract_source = _get_or_create_contract_file(contract_file_path)


        # Compile the contract
        compiled_sol = compile_source(contract_source)
        contract_interface = compiled_sol['<stdin>:Counter']

        # Deploy the contract
        contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        tx_hash = contract.constructor().transact()
        tx_receipt = await web3.eth.wait_for_transaction_receipt(tx_hash)

        # Contract instance
        contract_instance = web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_interface['abi']
        )

        try:
            # Increment the counter
            tx_hash = contract_instance.functions.increment().transact()

            # Wait for the transaction to be mined
            await web3.eth.wait_for_transaction_receipt(tx_hash)

            # Get the updated counter value
            counter_value = contract_instance.functions.count().call()

            # Update the Django model instance
            obj = cls.objects.first()
            obj.count = counter_value
            obj.save()

        except Exception as e:
            # Handle exceptions, e.g., log the error
            print("Error:", e)
