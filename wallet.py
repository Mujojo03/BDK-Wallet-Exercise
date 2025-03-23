import bdkpython as bdk
from mnemonic import Mnemonic as MnemonicLib
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

# Step 1: Generate and save mnemonic (only run this once)
try:
    print("Generating mnemonic seed...")
    # mnemonic = bdk.Mnemonic(bdk.WordCount.WORDS12)
    # mnemonic_phrase = str(mnemonic)

    #step 2: convert mnemonic to seed
    # generate mnemonic from mnemoniclib
    mnemoniclib = MnemonicLib("english")
    mnemo_phrase = mnemoniclib.generate(strength=128)
    print(mnemo_phrase)
    seed_bytes = mnemoniclib.to_seed(mnemo_phrase, passphrase="")
    print("MnemonicLib converted to seed successfully.")
    print(seed_bytes)

    # Save mnemonic to file
#     with open("mnemonic.txt", "w") as f:
#         f.write(mnemo_phrase)
#     print(f"\nGenerated Mnemonic: {mnemo_phrase}")
#     print("Mnemonic saved to mnemonic.txt - TO BE KEPT SECURE!")
# except Exception as e:
#     print(f"Error generating mnemonic: {e}")
#     exit(1)

# Step 2: Load mnemonic from file
# try:
#     with open("mnemonic.txt", "r") as f:
#         mnemonic_phrase = f.read().strip()
#     print("\nMnemonic loaded from mnemonic.txt")
# except FileNotFoundError:
#     print("Error: mnemonic.txt not found.")
#     exit(1)

# Step 3: Convert mnemonic to seed
# try:
#     mnemonic = bdk.Mnemonic.from_string(mnemonic_phrase)  # Convert mnemonic phrase to Mnemonic object
#     seed_bytes = mnemonic.to_seed("")  # Generate seed from mnemonic (empty passphrase)
#     print("Mnemonic converted to seed successfully.")
except Exception as e:
    print(f"Error converting mnemonic to seed: {e}")
    exit(1)
    

# Step 3
try:
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN_TESTNET)
    account_key = bip44_mst.Purpose().Coin().Account(0)
    print("Extended private key derived successfully.")

    # root_key = bdk.ExtendedPrivKey.from_seed(seed_bytes)
    # account_key = root_key.derive_path("m/84'/1'/0'")
    # print("Extended private key derived successfully.")

except Exception as e:
    print(f"Error deriving extended private key: {e}")
    exit(1)


# // Step 5: Create descriptors
# try:
#     descriptor = bdk.Descriptor(
#         f"wpkh({account_key.to_xprv()}/0/*)",  # Receiving addresses (m/84'/1'/0'/0/*)
#         bdk.Network.TESTNET
#     )
#     change_descriptor = bdk.Descriptor(
#         f"wpkh({account_key.to_xprv()}/1/*)",  # Change addresses (m/84'/1'/0'/1/*)
#         bdk.Network.TESTNET
#     )
#     print("Descriptors created successfully.")
# except Exception as e:
#     print(f"Error creating descriptors: {e}")
#     exit(1)

# Step 4: Create descriptors
try:
    # Get the extended private key (xprv) from the Bip44 account key
    xprv = account_key.PrivateKey().ToExtended()

    # Create descriptors using the xprv
    descriptor = bdk.Descriptor(
        f"wpkh({xprv}/0/*)",  # Receiving addresses (m/84'/1'/0'/0/*)
        bdk.Network.TESTNET
    )
    change_descriptor = bdk.Descriptor(
        f"wpkh({xprv}/1/*)",  # Change addresses (m/84'/1'/0'/1/*)
        bdk.Network.TESTNET
    )
    print("Descriptors created successfully.")
except Exception as e:
    print(f"Error creating descriptors: {e}")
    exit(1)


# Step 6: Initialize wallet
try:
    wallet = bdk.Wallet(
        descriptor,
        change_descriptor,
        bdk.Network.TESTNET,
       

    )
    print("Wallet initialized successfully.")
except Exception as e:
    print(f"Error initializing wallet: {e}")
    exit(1)


# Step 7: Generate and display addresses
print("\nGenerated Addresses:")
try:
    for i in range(3):
        address = wallet.get_address(bdk.AddressIndex.NEW).address
        print(f"Address {i+1}: {address}")
except Exception as e:
    print(f"Error generating addresses: {e}")
    exit(1)