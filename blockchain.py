# INTE264[1|2] | Blockchain Technology Fundamentals 
# Created by: Zyle Estacion (s4064846)
# RMIT University

import hashlib
import time
from block import Block

# Source: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
class Blockchain(object):
    """
    Manages the chain by storing transactions and contains helper methods to add new blocks.
    """
    def __init__(self):
        self.chain = []
        self.mempool = []
        # Define mining difficulty
        self.difficulty = 4
    
    def new_block(self, nonce=None, previous_hash=None, mine=True):
        """
        Creates a new block and adds it to the chain. When it is instantiated (created for the first time - a genesis block is created).

        Args:
            nonce (int): Arbitrary number used to indicate proof-of-work difficulty.
            previous_hash (string): Hash of the previous block. None for genesis block.
            mine (bool): Whether to mine the block or use the provided nonce

        Returns:
            block: The created block
        """

        if not self.verify_chain():
            raise Exception("Invalid block, it cannot be added to the chain.")
        
        # Take up to 5 transactions from the mempool
        transaction_for_block = self.mempool[:5]

        block = Block(
            id = len(self.chain) + 1,
            timestamp = time.time(),
            transactions= transaction_for_block,
            previous_hash=previous_hash,
            # Only fill the nonce if its not a genesis block
            nonce= nonce if nonce is not None else 0,
            current_hash=""
        )
        
        if mine:
            # Mine the block using PoW
            block = self.mine_block(block)
        else:
            block.current_hash = self.hash(block)

        # Add it to the chain
        self.chain.append(block)

        # Remove processed transactions from the mempool
        self.mempool = self.mempool[5:]

        return block
    
    def mine_block(self, block):
        """
        Proof of work mining algorithm to find a valid hash
        
        Args:
            block: The block to mine
        
        Returns:
            block: The mined block with a valid nonce and hash
        """
        target = "0" * self.difficulty
        attempts = 0
        start_time = time.time()

        print(f"⛏️ Mining block {block.id} with difficulty {self.difficulty}...")
    
        while True:
            # Calculate hash with current nonce
            block.current_hash = self.hash(block)
            attempts += 1
            
            # Check if hash meets the target requirement
            if block.current_hash.startswith(target):
                end_time = time.time()
                print(f"✅ Found valid hash! Nonce: {block.nonce}, Time: {end_time - start_time:.2f}s")
                return block
            
            # Increment nonce and try again
            block.nonce += 1
            
            if attempts % 50000 == 0:
                print(f"   Attempt {attempts}: {block.current_hash}")

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
    
    def display_chain(self):
        """
        Print the entire blockchain
        """
        if len(self.chain) == 0:
            print("\nBlockchain is empty")
        else:
            for block in self.chain:
                print(block)