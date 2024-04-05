"""
Raccoglitore di funzioni e classi che servono per la gestione degli smart contract
"""
from web3.auto import w3
from web3 import Account


def create_wallet():
    account = Account.create()
    return account.address, account._privateKey.hex()


def compile_smart_contract() -> str:
    """
    Controlla se il file è compilato oppure no
    se compilato ritorna il path
    se non compilato lo compila e ritorna il path
    """
    pass


def deploy_on_besu(compiled_smart_contract_path: str) -> bool:
    pass
