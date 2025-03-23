import bdkpython as bdk
from mnemonic import Mnemonic as MnemonicLib
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

# Step 1: Generate a mnemonic
try:
    print("Generating mnemonic seed...")

    #step 2: convert mnemonic to seed
    # generate mnemonic from mnemoniclib
    mnemoniclib = MnemonicLib("english")
    mnemo_phrase = mnemoniclib.generate(strength=128)
    print(mnemo_phrase)
    seed_bytes = mnemoniclib.to_seed(mnemo_phrase, passphrase="")
    print("MnemonicLib converted to seed successfully.")
    print(seed_bytes)

except Exception as e:
    print(f"Error converting mnemonic to seed: {e}")
    exit(1)
    
# Step 3
try:
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN_TESTNET)
    account_key = bip44_mst.Purpose().Coin().Account(0)
    print("Extended private key derived successfully.")

except Exception as e:
    print(f"Error deriving extended private key: {e}")
    exit(1)

# Step 4: Create descriptors
try:
    # Get the extended private key (xprv) from the Bip44 account key
    xprv = account_key.PrivateKey().ToExtended()

    # Create descriptors using the xprv
    descriptor = bdk.Descriptor(
        f"wpkh({xprv}/0/*)", 
        bdk.Network.TESTNET
    )
    change_descriptor = bdk.Descriptor(
        f"wpkh({xprv}/1/*)",  
        bdk.Network.TESTNET
    )
    print("Descriptors created successfully.")
except Exception as e:
    print(f"Error creating descriptors: {e}")
    exit(1)

# Step 5: Initialize wallet
try:
    wallet = bdk.Wallet(
        descriptor,
        change_descriptor,
        bdk.Network.TESTNET,
        bdk.MemoryDatabase()
    )
    print("Wallet initialized successfully.")
except Exception as e:
    print(f"Error initializing wallet: {e}")
    exit(1)

# Step 6: Generate and display addresses
print("\nGenerated Addresses:")
try:
    for i in range(3):
        address = wallet.get_address(bdk.AddressIndex.NEW).address
        print(f"Address {i+1}: {address}")
except Exception as e:
    print(f"Error generating addresses: {e}")
    exit(1)

    # Step 7: Synchronize wallet with testnet
try:
    blockchain = bdk.ElectrumBlockchain(config={"url": "ssl://electrum.blockstream.info:60002"})
    print("\nSynchronizing with testnet...")
    wallet.sync(blockchain)
    balance = wallet.get_balance()
    print(f"Balance: {balance.total} satoshis ({balance.total / 100_000_000:.8f} BTC)")
except Exception as e:
    print(f"Error synchronizing wallet: {e}")
    exit(1)

# Step 8: Verify funding status
if balance.total > 0:
    print("Funding confirmed—wallet is active.")
else:
    print("No funds detected—continue funding.")