"""
Double-Spend Prevention Test Cases
Demonstrates how the blockchain prevents the same digital asset from being spent more than once.
Created by: Zyle Estacion (s4064846)
RMIT University - INTE264 Assignment 2
"""

from blockchain import Blockchain
import time

def test_double_spend_prevention():
    """
    Comprehensive test to demonstrate double-spend prevention mechanisms.
    """
    print("🚨 DOUBLE-SPEND PREVENTION TEST SUITE")
    print("=" * 60)
    
    # Initialize blockchain
    blockchain = Blockchain()
    
    # Create genesis block
    print("\n1. Creating Genesis Block...")
    genesis = blockchain.new_block(mine=False, nonce=100)  # Use manual nonce for faster testing
    print(f"✅ Genesis block created: {genesis.id}")
    
    # Test Case 1: Basic Double Spend Attempt
    print("\n" + "="*50)
    print("TEST CASE 1: Basic Double Spend Attempt")
    print("="*50)
    
    # Alice receives initial funds
    print("\n📝 Step 1: Alice receives 100 coins from genesis...")
    tx1_result = blockchain.new_transaction(
        sender="genesis", 
        receiver="Alice", 
        amount=100,
        spent_transactions=[]
    )
    print(f"Transaction added: {tx1_result is not None}")
    
    # Mine the block to confirm the transaction
    print("\n⛏️ Mining block to confirm Alice's funds...")
    block2 = blockchain.new_block(mine=False, nonce=200, previous_hash=genesis.current_hash)
    print(f"Block 2 mined with {len(block2.transactions)} transaction(s)")
    
    # Get Alice's transaction ID for spending
    alice_tx_id = block2.transactions[0]['transaction_id']
    print(f"Alice's transaction ID: {alice_tx_id[:8]}...")
    
    # Alice attempts first spend
    print("\n💸 Step 2: Alice tries to spend 50 coins to Bob...")
    tx2_result = blockchain.new_transaction(
        sender="Alice",
        receiver="Bob", 
        amount=50,
        spent_transactions=[alice_tx_id]
    )
    print(f"First spend attempt: {'✅ Success' if tx2_result else '❌ Failed'}")
    
    # Alice attempts second spend with SAME transaction ID
    print("\n💸 Step 3: Alice tries to spend the SAME 100 coins to Charlie...")
    tx3_result = blockchain.new_transaction(
        sender="Alice",
        receiver="Charlie",
        amount=30,
        spent_transactions=[alice_tx_id]  # Same transaction ID!
    )
    print(f"Second spend attempt: {'✅ Success' if tx3_result else '❌ Failed'}")
    
    # Results
    print(f"\n📊 Test Result: {'✅ PASS - Double spend prevented!' if not tx3_result else '❌ FAIL - Double spend allowed!'}")
    
    # Test Case 2: Duplicate Transaction ID Prevention
    print("\n" + "="*50)
    print("TEST CASE 2: Duplicate Transaction ID Prevention")
    print("="*50)
    
    # Try to create a transaction with duplicate ID
    print("\n🔄 Attempting to create transaction with duplicate ID...")
    
    # Get existing transaction ID from mempool
    if blockchain.mempool:
        existing_tx_id = blockchain.mempool[0]['transaction_id']
        
        # Create a new transaction with the same ID (this should fail)
        duplicate_transaction = {
            'transaction_id': existing_tx_id,  # Same ID as existing transaction
            'sender': 'Eve',
            'receiver': 'Mallory',
            'amount': 25,
            'spent_transactions': [],
            'timestamp': time.time()
        }
        
        print(f"Existing transaction ID: {existing_tx_id[:8]}...")
        is_valid = blockchain.verify_transaction(duplicate_transaction)
        print(f"Duplicate ID verification: {'❌ Rejected' if not is_valid else '✅ Accepted'}")
        print(f"Test Result: {'✅ PASS - Duplicate ID prevented!' if not is_valid else '❌ FAIL - Duplicate ID allowed!'}")
    else:
        print("No transactions in mempool to test duplicate IDs")
    
    # Test Case 3: Multiple Spend Attempts in Mempool
    print("\n" + "="*50)
    print("TEST CASE 3: Multiple Spend Attempts in Mempool")
    print("="*50)
    
    print("\n📝 Creating multiple transactions that try to spend the same UTXO...")
    
    # Create a new transaction for testing
    blockchain.new_transaction(
        sender="genesis",
        receiver="David",
        amount=75,
        spent_transactions=[]
    )
    
    # Mine block to confirm David's funds
    block3 = blockchain.new_block(mine=False, nonce=300, previous_hash=block2.current_hash)
    david_tx_id = block3.transactions[0]['transaction_id']
    
    print(f"David received transaction ID: {david_tx_id[:8]}...")
    
    # David tries multiple spends
    spend1 = blockchain.new_transaction(
        sender="David",
        receiver="Emma",
        amount=25,
        spent_transactions=[david_tx_id]
    )
    
    spend2 = blockchain.new_transaction(
        sender="David", 
        receiver="Frank",
        amount=25,
        spent_transactions=[david_tx_id]  # Same UTXO!
    )
    
    print(f"First spend to Emma: {'✅ Success' if spend1 else '❌ Failed'}")
    print(f"Second spend to Frank: {'✅ Success' if spend2 else '❌ Failed'}")
    print(f"Test Result: {'✅ PASS - Mempool double spend prevented!' if not spend2 else '❌ FAIL - Mempool double spend allowed!'}")
    
    # Test Case 4: Chain Integrity After Attack
    print("\n" + "="*50)
    print("TEST CASE 4: Chain Integrity After Double Spend Attempts")
    print("="*50)
    
    print("\n🔍 Verifying blockchain integrity...")
    chain_valid = blockchain.verify_chain()
    
    print(f"\n📊 Current blockchain status:")
    print(f"   Blocks in chain: {len(blockchain.chain)}")
    print(f"   Transactions in mempool: {len(blockchain.mempool)}")
    print(f"   Chain validity: {'✅ Valid' if chain_valid else '❌ Invalid'}")
    
    # Display final mempool
    print(f"\n📝 Final mempool contents:")
    if blockchain.mempool:
        for i, tx in enumerate(blockchain.mempool):
            print(f"   {i+1}. {tx['sender']} → {tx['receiver']}: {tx['amount']} (ID: {tx['transaction_id'][:8]}...)")
    else:
        print("   Mempool is empty")
    
    return chain_valid and not tx3_result and not spend2

def demonstrate_attack_scenario():
    """
    Demonstrates a realistic attack scenario and how the system prevents it.
    """
    print("\n🎭 REALISTIC ATTACK SCENARIO DEMONSTRATION")
    print("=" * 60)
    
    blockchain = Blockchain()
    
    print("\n📖 Scenario: Attacker tries to buy from two merchants simultaneously")
    print("   1. Attacker has 1 UTXO worth 100 coins")
    print("   2. Tries to buy $80 item from Merchant A")
    print("   3. Simultaneously tries to buy $70 item from Merchant B")
    print("   4. Both merchants accept before either transaction is mined")
    
    # Setup
    genesis = blockchain.new_block(mine=False, nonce=100)
    
    # Attacker receives funds
    blockchain.new_transaction("genesis", "Attacker", 100, [])
    funds_block = blockchain.new_block(mine=False, nonce=200, previous_hash=genesis.current_hash)
    attacker_utxo = funds_block.transactions[0]['transaction_id']
    
    print(f"\n💰 Attacker receives UTXO: {attacker_utxo[:8]}... (100 coins)")
    
    # Attack attempts
    print(f"\n💸 Attack Attempt 1: Buy from Merchant A (80 coins)")
    attack1 = blockchain.new_transaction(
        "Attacker", "Merchant_A", 80, [attacker_utxo]
    )
    
    print(f"💸 Attack Attempt 2: Buy from Merchant B (70 coins) using SAME UTXO")
    attack2 = blockchain.new_transaction(
        "Attacker", "Merchant_B", 70, [attacker_utxo]
    )
    
    print(f"\n🛡️ Defense Results:")
    print(f"   Merchant A transaction: {'✅ Accepted' if attack1 else '❌ Rejected'}")
    print(f"   Merchant B transaction: {'✅ Accepted' if attack2 else '❌ Rejected'}")
    
    if attack1 and not attack2:
        print(f"\n🎉 SUCCESS: Only one merchant transaction was accepted!")
        print(f"   Merchant A will receive payment when block is mined")
        print(f"   Merchant B was protected from the double-spend attack")
    elif not attack1 and not attack2:
        print(f"\n⚠️ Both transactions rejected (unexpected)")
    else:
        print(f"\n🚨 FAILURE: Double spend attack succeeded!")
    
    return attack1 and not attack2

if __name__ == "__main__":
    print("🔗 BLOCKCHAIN DOUBLE-SPEND PREVENTION TEST SUITE")
    print("INTE264 Assignment 2 - Zyle Estacion (s4064846)")
    print("=" * 60)
    
    # Run comprehensive tests
    test_result = test_double_spend_prevention()
    
    # Run attack scenario
    attack_result = demonstrate_attack_scenario()
    
    # Final summary
    print("\n" + "="*60)
    print("📊 FINAL TEST SUMMARY")
    print("="*60)
    print(f"Basic double-spend prevention: {'✅ PASS' if test_result else '❌ FAIL'}")
    print(f"Realistic attack scenario: {'✅ PASS' if attack_result else '❌ FAIL'}")
    
    overall_result = test_result and attack_result
    print(f"\nOverall security assessment: {'🛡️ SECURE' if overall_result else '🚨 VULNERABLE'}")
    
    if overall_result:
        print("\n🎉 All tests passed! Your blockchain successfully prevents double spending.")
    else:
        print("\n⚠️ Some tests failed. Review the double-spend prevention implementation.")
