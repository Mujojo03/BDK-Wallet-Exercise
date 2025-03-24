import bip39
import requests
import bdkpython as bdk
from mnemonic import Mnemonic
from bip32 import BIP32
# from bip39 import BIP39
from bitcoinlib.keys import HDKey

# #How I generated the mnemonic phrase
# mnemonic = Mnemonic("english")
# mnemonic_phrase = mnemonic.generate(strength=128)  # Generate a new 12-word mnemonic
# print(f"Mnemonic: {mnemonic_phrase}")

# # Convert Mnemonic to Seed
# seed = mnemonic.to_seed(mnemonic_phrase)  # Convert mnemonic to seed
# # root_key = BIP32.from_seed(seed)
# root_key = BIP32.from_seed(seed, network="test")


# An already Generated Mnemonic phrase
mnemonic = Mnemonic("english")
mnemonic_phrase = "dose wealth kiss target antique grab frown finish grocery inmate effort two"  # Fixed Mnemonic which was already generated
print(f"Mnemonic: {mnemonic_phrase}")

# Convert Mnemonic to Seed - 1
seed = mnemonic.to_seed(mnemonic_phrase)
root_key = BIP32.from_seed(seed, network="test")

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

# Function to fetch balance using JSON
def get_balance(address):
    try:
        url = f"https://blockstream.info/testnet/api/address/{address}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

         # Extract and print balance information
        chain_stats = data.get("chain_stats", {})
        funded_txo_sum = chain_stats.get("funded_txo_sum", 0)  # Total received
        spent_txo_sum = chain_stats.get("spent_txo_sum", 0)  # Total spent
        balance = funded_txo_sum - spent_txo_sum  # Calculate current balance

        print(f"Balance for {address}: {balance} satoshis ({balance / 100_000_000:.8f} BTC)")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance for {address}: {e}")

# Fetch balance and transaction history for all SegWit addresses
print("\nFetching balance and transaction history for SegWit Addresses:")
for i in range(3):  # Loop through the 3 generated addresses
    # Derive the path for each address
    path_bip84 = f"m/84'/1'/0'/0/{i}"
    child_key_bip84 = HDKey(root_key.get_privkey_from_path(path_bip84), network='testnet')
    p2wpkh_address = child_key_bip84.address()
    
    # Print the address
    print(f"\nFetching balance for Address {i + 1}: {p2wpkh_address}")
    
    # Fetch and print the balance for the address
    get_balance(p2wpkh_address)
    
    # Fetch and print the transaction history for the address
    print(f"\nFetching transaction history for Address {i + 1}: {p2wpkh_address}")
    get_transaction_history(p2wpkh_address)
