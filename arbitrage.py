from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from flashbots import FlashbotsProvider, FlashbotsBundle
from config import config  # Import config dictionary

# Extract config values
rpc_url = config["rpc_endpoints"][0]["url"]
chain_id = config["rpc_endpoints"][0]["chain_id"]
eth_private_key = config["private_key"]
flashbots_url = config["flashbots_relay_url"]
max_priority_fee = Web3.to_wei(config["max_priority_fee"], "gwei")
max_fee = Web3.to_wei(config["max_fee"], "gwei")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Load account
eth_account: LocalAccount = Account.from_key(eth_private_key)

# Attach Flashbots Provider
flashbots = FlashbotsProvider(w3, eth_account)

# Example Transaction (Replace with Arbitrage Logic)
tx = {
    "to": "0x0000000000000000000000000000000000000000",  # Replace with target address
    "value": Web3.to_wei(0.1, "ether"),
    "gas": 25000,
    "maxPriorityFeePerGas": max_priority_fee,
    "maxFeePerGas": max_fee,
    "nonce": w3.eth.get_transaction_count(eth_account.address),
    "chainId": chain_id
}

def send_flashbots_transaction(tx):
    """ Sends transaction through Flashbots """
    bundle = FlashbotsBundle([
        {"signer": eth_account, "transaction": tx}
    ])

    try:
        response = flashbots.send_bundle(bundle)
        response.wait()
        print("Transaction sent via Flashbots!")
    except Exception as e:
        print(f"Flashbots transaction failed: {e}")

send_flashbots_transaction(tx)
