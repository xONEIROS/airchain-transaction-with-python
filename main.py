import time
import sys
import random
from web3 import Web3
from eth_account import Account

def create_wallet_from_private_key(private_key_hex):
    try:
        account = Account.from_key(private_key_hex)
        return account
    except Exception as e:
        print(f"Error parsing private key: {e}")
        sys.exit(1)

def send_tx(web3, account, to_address, amount, chain_id):
    try:
        nonce = web3.eth.get_transaction_count(account.address)
        gas_price = web3.eth.gas_price
        gas_limit = 25000

        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': amount,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': chain_id
        }

        signed_tx = Account.sign_transaction(tx, account._private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Tx: {tx_hash.hex()}")
    except Exception as e:
        print(f"Failed to send transaction: {e}")

def convert_from_wei(value, unit):
    units = {
        'wei': 1,
        'kwei': 1e3,
        'mwei': 1e6,
        'gwei': 1e9,
        'microether': 1e12,
        'milliether': 1e15,
        'ether': 1e18
    }
    return value / units[unit]

def main():
    private_key_hex = input("Enter EVM Private Key: ").strip()
    url = input("Enter RPC URL: ").strip()
    
    wallet = create_wallet_from_private_key(private_key_hex)
    print(wallet.address)
    
    web3 = Web3(Web3.HTTPProvider(url))
    
    try:
        balance = web3.eth.get_balance(wallet.address)
        print("Balance:", convert_from_wei(balance, 'ether'))
    except Exception as e:
        print(f"Error getting balance: {e}")
        sys.exit(1)

    chain_id = 1234
    i = 0
    while True:
        i += 1
        send_tx(web3, wallet, wallet.address, web3.to_wei(i % 10 + 1, 'ether'), chain_id)
        sleep_time = random.uniform(5, 8)  
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
