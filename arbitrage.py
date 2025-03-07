from web3 import Web3
import json
import requests
from config import CONFIG

# 🔗 Connect to Ethereum
web3 = Web3(Web3.HTTPProvider(CONFIG["RPC_ENDPOINT"]))
account = web3.eth.account.from_key(CONFIG["PRIVATE_KEY"])

# 📜 Load Smart Contract
with open("FlashLoanArbitrage.json") as f:
    contract_abi = json.load(f)
contract = web3.eth.contract(address=CONFIG["CONTRACT_ADDRESS"], abi=contract_abi)

# 🚀 Flashbots Relay URL
FLASHBOTS_URL = CONFIG["FLASHBOTS_RELAY"]

# 📌 Function to send private transactions via Flashbots
def send_flashbots_transaction(tx):
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_sendPrivateTransaction",
        "params": [{"tx": tx, "maxBlockNumber": web3.eth.block_number + 10}]
    }
    response = requests.post(FLASHBOTS_URL, json=payload, headers=headers)
    return response.json()

# 🔍 Check for Arbitrage Opportunity
def find_arbitrage():
    uniswap_price = get_price_uniswap()
    sushiswap_price = get_price_sushiswap()
    
    if uniswap_price > sushiswap_price * 1.01:
        print("Arbitrage Found! Executing Flash Loan")
        execute_flashloan()

# 🚀 Execute Flash Loan Arbitrage via Flashbots
def execute_flashloan():
    tx = contract.functions.executeArbitrage("0xC02aaa39b223FE8D0A0E5C4F27eAD9083C756Cc2", 1000).build_transaction({
        'from': CONFIG["WALLET_ADDRESS"],
        'gas': 3000000,
        'gasPrice': web3.to_wei('30', 'gwei'),
        'nonce': web3.eth.get_transaction_count(CONFIG["WALLET_ADDRESS"])
    })

    signed_tx = web3.eth.account.sign_transaction(tx, CONFIG["PRIVATE_KEY"])
    raw_tx = signed_tx.rawTransaction.hex()

    flashbots_response = send_flashbots_transaction(raw_tx)
    print("Flashbots Response:", flashbots_response)

# 🏃 Run Bot
while True:
    find_arbitrage()
