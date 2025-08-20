# INTE264[1|2] | Blockchain Technology Fundamentals 
# Created by: Zyle Estacion (s4064846)
# RMIT University

from app import Blockchain
import time

# Chain integrity check function (move to top so it's defined before use)
def verify_chain_integrity(blockchain):
    for i in range(1, len(blockchain.chain)):
        current_block = blockchain.chain[i]
        previous_block = blockchain.chain[i-1]
        if current_block.previous_hash != previous_block.current_hash:
            print(f"❌ Chain broken at Block {current_block.id}")
            print(f"   Expected: {previous_block.current_hash}")
            print(f"   Found:    {current_block.previous_hash}")
            return False
    print("✅ Chain integrity intact")
    return True

# Create blockchain
blockchain = Blockchain()

# Create genesis block
print("\n=== GENESIS BLOCK ===")
genesis = blockchain.new_block(nonce=100)
print(genesis)

# Add a transaction
print("\n=== ADD TRANSACTION ===")
blockchain.new_transaction("Alice", "Bob", 50)

# Create second block
print("\n=== SECOND BLOCK ===")
block2 = blockchain.new_block(nonce=200, previous_hash=genesis.current_hash)
print(block2)

# Initial integrity check
print("\n=== 🛫 INITIAL INTEGRITY CHECK ===")
# Validate the chain before a modification is made
blockchain.verify_chain()

print("\n🛠️ Simulating an attacker modifying the block...")
modifiedblock = blockchain.edit_block()

# Post modification steps
print("\n=== FULL CHAIN VERIFICATION ===")
verify_chain_integrity(blockchain)
