# q2-test_cases.py
# Test cases for your blockchain implementation

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
print("\n=== INITIAL INTEGRITY CHECK ===")
print(f"Genesis hash valid: {blockchain.verify_hash(genesis)}")
print(f"Block 2 hash valid: {blockchain.verify_hash(block2)}")

# Simulate an attacker modifying the block
print("\n🛠️ ===Simulating an attacker modifying the block ===")
original_amount = block2.transactions[0]['amount']
original_hash = block2.current_hash
print(f"Original transaction amount: {original_amount}")
print(f"Original hash: {original_hash}")
block2.transactions[0]['amount'] = 999  # Tamper
print(f"Modified transaction amount: {block2.transactions[0]['amount']}")
print(f"Hash valid after tampering: {blockchain.verify_hash(block2)}")

# Post modification steps
print("\n=== POST MODIFICATION STEPS ===")
# Restore original data
block2.transactions[0]['amount'] = original_amount
print(f"After restoring original data - Hash valid: {blockchain.verify_hash(block2)}")

# Tamper again and recalculate hash
block2.transactions[0]['amount'] = 777
print(f"After tampering - Hash valid: {blockchain.verify_hash(block2)}")
block2.current_hash = blockchain.hash(block2)
print(f"After recalculating hash - Hash valid: {blockchain.verify_hash(block2)}")
print(f"New hash: {block2.current_hash}")

# Final verification
print("\n=== FINAL VERIFICATION ===")
print(f"Genesis hash valid: {blockchain.verify_hash(genesis)}")
print(f"Block 2 hash valid: {blockchain.verify_hash(block2)}")

print("\n=== FULL CHAIN VERIFICATION ===")
verify_chain_integrity(blockchain)
