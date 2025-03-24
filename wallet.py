import bip39
import requests
import bdkpython as bdk
from mnemonic import Mnemonic
from bip32 import BIP32
# from bip39 import BIP39
from bitcoinlib.keys import HDKey

#How I generated the mnemonic phrase
mnemonic = Mnemonic("english")
mnemonic_phrase = mnemonic.generate(strength=128)  # Generate a new 12-word mnemonic
print(f"Mnemonic: {mnemonic_phrase}")

# Convert Mnemonic to Seed
seed = mnemonic.to_seed(mnemonic_phrase)  # Convert mnemonic to seed
# root_key = BIP32.from_seed(seed)
root_key = BIP32.from_seed(seed, network="test")


# # Generate Mnemonic phrase - 1
# mnemonic = Mnemonic("english")
# mnemonic_phrase = "hill neglect prison common modify tone shadow trophy hazard toy boil seat"  # Fixed Mnemonic which was already generated
# print(f"Mnemonic: {mnemonic_phrase}")

# # Convert Mnemonic to Seed - 1
# seed = mnemonic.to_seed(mnemonic_phrase)
# root_key = BIP32.from_seed(seed)


# BIP84 (SegWit) Address Derivation
# path_bip84 = "m/84'/1'/0'/0/{i}" #m/44'/1'/0'/0/0 - change address
# child_key_bip84 = HDKey(root_key.get_privkey_from_path(path_bip84), network='testnet')
# p2wpkh_address = child_key_bip84.address()
# print(f"Generated SegWit Address: {p2wpkh_address}")

# Generate three receiving addresses
# BIP84 (SegWit) Address Derivation
print("\nGenerated Addresses:")
for i in range(3):
    path_bip84 = f"m/84'/1'/0'/0/{i}"  # Replace {i} with the current index
    child_key_bip84 = HDKey(root_key.get_privkey_from_path(path_bip84), network='testnet')
    p2wpkh_address = child_key_bip84.address()
    print(f"Address {i + 1}: {p2wpkh_address}")
    

# BIP44 (P2PKH) Address Derivation
path_bip44 = "m/44'/1'/0'/0/0"
child_key_bip44 = HDKey(root_key.get_privkey_from_path(path_bip44), network='testnet')
p2pkh_address = child_key_bip44.address()
print(f"Generated P2PKH Address: {p2pkh_address}")

# Function to fetch balance
def get_balance(address):
    try:
        url = f"https://blockstream.info/testnet/api/address/{address}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print("Balance Information:", data.get("chain_stats", {}))
    except requests.exceptions.RequestException as e:
        print("Error fetching balance:", e)

# Function to fetch transaction history
def get_transaction_history(address):
    try:
        url = f"https://blockstream.info/testnet/api/address/{address}/txs"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        transactions = response.json()
        if not transactions:
            print("No transactions found.")
        else:
            print("Transaction History:")
            for i, tx in enumerate(transactions, 1):
                print(f"TX {i}: ID: {tx['txid']}, Confirmed: {tx['status']['confirmed']}")
    except requests.exceptions.RequestException as e:
        print("Error fetching transactions:", e)

# Fetch balance and transaction history
print("\nFetching balance for SegWit Address...")
get_balance(p2wpkh_address)

print("\nFetching transaction history for SegWit Address...")
get_transaction_history(p2wpkh_address)
