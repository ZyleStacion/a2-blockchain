# INTE264[1|2] | Blockchain Technology Fundamentals 
# Created by: Zyle Estacion (s4064846)
# RMIT University

import hashlib
import time

# Q1. Block Structure
class Block:
    """
    Represent a single block in our chain.

    Attributes:
        id (int): Unique block ID.
        timestamp (str): Time of block creation.
        transactions (dict): A list of transactions containing transaction details.
        previous_hash (str): SHA-256 hash of the previous block in the chain.
        nonce (int): Arbitrary number used to track Proof-of-Work difficulty.
        hash (str): SHA-256 hash of the block contents.
    """
    def __init__(self, id, timestamp, transactions, previous_hash, nonce, current_hash):
        self.id = id
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.current_hash = current_hash

    # Asked ChatGPT to make this look like a block
    def __str__(self):
        lines = [
            f"│ Block ID    : {self.id}",
            f"│ Timestamp   : {self.timestamp}",
            f"│ Transactions: {self.transactions}",
            f"│ Nonce       : {self.nonce}",
            f"│ Hash        : {self.current_hash}",
            f"│ Prev. Hash  : {self.previous_hash}",
        ]
        width = max(len(line) for line in lines)
        top = "┌" + "─" * (width - 2) + "┐"
        bottom = "└" + "─" * (width - 2) + "┘"
        return "\n".join([top] + lines + [bottom])
    
# Q2. Chain integrity and hashing
# Source: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
class Blockchain(object):
    """
    Manages the chain by storing transactions and contains helper methods to add new blocks.
    """
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.mempool = []
    
    def new_block(self, nonce, previous_hash=None):
        """
        Creates a new block and adds it to the chain. When it is instantiated (created for the first time - a genesis block is created).

        Args:
            nonce (int): Arbitrary number used to indicate proof-of-work difficulty.
            previous_hash (string): Hash of the previous block. None for genesis block.

        Returns:
            block: The created block
        """

        if not self.verify_chain():
            raise Exception("Invalid block, it cannot be added to the chain.")

        block = Block(
            id = len(self.chain) + 1,
            timestamp = time.time(),
            transactions= self.current_transactions,
            previous_hash=previous_hash,
            nonce= nonce,
            current_hash=""
        )
        
        # Set the block's hash
        block.current_hash = self.hash(block)

        # Add it to the chain
        self.chain.append(block)

        # Clear current transactions
        self.current_transactions = []

        return block
    
    def edit_block(self):
        """
        Allows a published block to be edited (for demonstration purposes)

        Args:
            block: The second to last block in the chain.
        
        Returns:
            modified_block (Block): A new, modified version of the block.
        """

        # Get the second to last block
        block = self.chain[-2]

        # Modify the block
        print(f"Modifying Block ID: {block.id}")
        print(f"Hash: {block.current_hash}")
        
        attributes = ['id', 'timestamp', 'transactions', 'nonce']

        for attribute in attributes:
            current_val = getattr(block, attribute)
            print(f"\nCurrent {attribute}: {current_val}")

            # Edit the attribute
            new_value = input(f"Enter new {attribute} or press Enter to skip: ")

            # Match field data types
            if new_value:
                match attribute:
                    case 'id' | 'nonce':
                        setattr(block, attribute, int(new_value))
                    case 'timestamp':
                        setattr(block, attribute, float(new_value))
                    case 'transactions':
                        # Convert input to list
                        setattr(block, attribute, eval(new_value))
                    case _:
                        setattr(block, attribute, new_value)

        # Calculate new block hash based on modified data
        block.current_hash = self.hash(block)
        print(f"\nNew hash: {self.hash(block)}")
        
        return block

    def new_transaction(self, sender, receiver, amount):
        """
        Verifies and adds a new transaction to the mempool. Only valid transactions are added.

        Args:
            sender (str): Sender of the transaction.
            receiver (str): Receiver of the transaction.
            amount (int/float): Amount to transfer.

        Returns:
            int or None: The ID of the next mined block which will hold the transaction, or None if invalid.
        """
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        if self.verify_transaction(transaction):
            self.mempool.append(transaction)
            print("✅ Transaction added to mempool.")
            return self.last_block.id + 1 if self.last_block else 1
        else:
            print("❌ Transaction is invalid and was not added.")
            return None

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash for a block. @staticmethod = can be used outside of the 'Blockchain' class.

        Args:
            block: The current block, used to access its data and previous hash.
        
        Returns: 
            hash (str): Hash value in hex format.
        """

        # Prepare the string for hashing - using all the block data
        hashableString = f"{block.id}{block.timestamp}{block.transactions}{block.previous_hash}{block.nonce}"
        
        # Hash and return the string
        return hashlib.sha256(hashableString.encode()).hexdigest()

    def verify_hash(self, block):
        """
        Verify that the hash stored in the block matches the calculated hash.

        Args:
            block: The entire block containing the hash to be verified.

        Returns:
            bool: True if calculated hash matches expected result, False is not.
        """
        calculated_hash = self.hash(block)
        return calculated_hash == block.current_hash

    @property
    def last_block(self):
        """
        Returns the last block in the chain. @property = turns a method into an attribute so we can modify its values later on.

        Returns:
            block: The last block in the chain
        """
        if len(self.chain) == 0:
            return None
        else:
            return self.chain[-1]
    
    def verify_chain(self):
        """
        Validates the entire blockchain by checking that each block's hash and its reference to a previous_hash is correct.

        Returns:
            bool: True if the chain if valid. False if otherwise.
        """
        for i in range(len(self.chain)):
            current_block = self.chain[i]

            # Check the current block's hash is correct
            if not self.verify_hash(current_block):
                print(f"❌ Block {current_block.id} has an invalid hash!")
                return False

            # For non-genesis blocks, also check if the previous hash is correct
            if i > 0:
                previous_block = self.chain[i - 1]
                if current_block.previous_hash != previous_block.current_hash:
                    print(f"❌ Block {current_block.id} does not match previous block hash!")
                    return False
        
        # No errors were found
        print("✅ Blockchain is valid!")
        return True
    
    def verify_transaction(self, transaction):
        """
        Verifies that a transaction contains all fields before passing it to the mempool.

        Args:
            transaction (dict): A transaction to verify, contains sender, receiver and amount.
        
        Returns:
            bool: True if valid, False otherwise.
        """

        # Source: GitHub Copilot
        required_fields = ['sender', 'receiver', 'amount']
        for field in required_fields:
            if field not in transaction:
                print(f"❌ Transaction is missing field {field}")
                return False
        if not isinstance(transaction['amount'], (int, float)):
            print("❌ Transaction amount must be a number!")
            return False
        if transaction['amount'] <= 0:
            print("❌ Transaction amount must be positive!")
            return False
        if not transaction['sender'] or not transaction['receiver']:
            print("❌ Sender and receiver must not be empty!")
            return False
        return True

### TEST CASES
# Create blockchain
blockchain = Blockchain()

# Create genesis block
genesis = blockchain.new_block(nonce=100)
print(genesis)

# Add a transaction
blockchain.new_transaction("Alice", "Bob", 50)

# Create second block
block2 = blockchain.new_block(nonce=200, previous_hash=genesis.current_hash)
print(block2)

print("\n=== 🛫 INITIAL INTEGRITY CHECK ===")
# Validate the chain before a modification is made
blockchain.verify_chain()

print("\n🛠️  Simulating an attacker modifying the block...")
modifiedblock = blockchain.edit_block()

print("\n=== 🕵️  POST-MODIFICATION INTEGRITY CHECK ===")
# Validate chain after a modification has been made
blockchain.verify_chain()