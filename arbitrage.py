from web3 import Web3
from eth_account import Account
from flashbots import flashbots

from config import config

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(config["rpc_endpoints"][0]["url"]))

# Load account
account = Account.from_key(config["private_key"])

# Attach Flashbots
flashbots(w3, account)

def send_flashbots_transaction(tx):
    """
    Sends a private transaction via Flashbots.
    """
    bundle = [
        {
            "signer": account,
            "transaction": tx
        }
    ]
    try:
        response = w3.flashbots.send_bundle(bundle, target_block_number=w3.eth.block_number + 1)
        response.wait()
        print("Transaction sent via Flashbots:", response.receipts())
    except Exception as e:
        print("Flashbots transaction failed:", e)

# Example transaction (Replace this with actual arbitrage logic)
tx = {
    "to": "0x0000000000000000000000000000000000000000",  # Replace with arbitrage contract
    "value": w3.to_wei(0.1, "ether"),
    "gas": 25000,
    "gasPrice": w3.to_wei(2, "gwei"),
    "nonce": w3.eth.get_transaction_count(account.address),
    "chainId": config["rpc_endpoints"][0]["chain_id"]
}

send_flashbots_transaction(tx)
