# INTE264[1|2] | Blockchain Technology Fundamentals 
# Created by: Zyle Estacion (s4064846)
# RMIT University

import hashlib
import string
import time
import random

# Block Structure
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
    
# Chain integrity and hashing
# Source: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
class Blockchain(object):
    """
    Manages the chain by storing transactions and contains helper methods to add new blocks.
    """
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
    def new_block(self, nonce, previous_hash=None):
        """
        Creates a new block and adds it to the chain. When it is instantiated (created for the first time - a genesis block is created).

        Args:
            nonce (int): Arbitrary number used to indicate proof-of-work difficulty.
            previous_hash (string): Hash of the previous block. None for genesis block.

        Returns:
            block (obj): 
        """
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

    def new_transaction(self, sender, receiver, amount):
        """
        Creates a new transaction which will be hashed, and placed into the next mined Block

        Args:
            sender (str): Sender of the transaction.
            receiver (str): Reciever of the transaction.
            amount (hash): Sender of the transaction

        Returns:
            self.last_block['id'] + 1: The ID of the next mined block which will hold the transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        return self.last_block['id'] + 1


    # TODO: Maybe modify this so it takes current transaction data + previous block hash
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash for a block. @staticmethod = can be used outside of the 'Blockchain' class.

        Args:
            block (dict): Block
        
        Returns: 
            hash (str): Hash value
        """
        pass

    @property
    def last_block(self):
        """
        Returns the last block in the chain. @property = turns a method into an attribute so we can modify its values later on.

        Returns:
            block (dict): Last block
        """
    pass
