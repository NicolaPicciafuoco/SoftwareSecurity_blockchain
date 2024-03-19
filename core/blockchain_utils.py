from web3.auto import w3


def create_ethereum_wallet():
    account = w3.eth.account.create()
    return {
        'address': account.address,
        'private_key': account.privateKey.hex(),
    }