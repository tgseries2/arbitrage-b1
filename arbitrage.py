from web3 import Web3
from eth_account import Account
from flashbots.rpc import FlashbotsWeb3Provider
import json
import time

# Load config
from config import config

# Connect to Ethereum RPC
w3 = Web3(Web3.HTTPProvider(config["rpc_endpoints"][0]["url"]))

# Load private key
private_key = config["private_key"]
account = Account.from_key(private_key)

# Attach Flashbots provider
w3.middleware_onion.inject(FlashbotsWeb3Provider, layer=0, account=account)

def main():
    print(f"Connected to Ethereum: {w3.isConnected()}")
    print(f"Account: {account.address}")
    
    # Example function to check ETH balance
    balance = w3.eth.get_balance(account.address)
    print(f"ETH Balance: {w3.from_wei(balance, 'ether')} ETH")
    
    # Simulate an arbitrage logic (replace with actual strategy)
    while True:
        print("Scanning for arbitrage opportunities...")
        time.sleep(5)  # Simulate waiting for market conditions

if __name__ == "__main__":
    main()
