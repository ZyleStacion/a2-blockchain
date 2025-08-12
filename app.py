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
    def __init__(self, id, timestamp, transactions, previous_hash, nonce, hash):
        self.id = id
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash

    # Asked ChatGPT to make this look like a block
    def __str__(self):
        lines = [
            f"│ Block ID    : {self.id}",
            f"│ Timestamp   : {self.timestamp}",
            f"│ Data        : {self.data}",
            f"│ Nonce       : {self.nonce}",
            f"│ Hash        : {self.hash}",
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
    def __init___(self):
        self.chain = []
        self.current_transactions = []
    
    def new_block(self):
        # Creates a new block and adds it to the chain
        pass

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction which will be placed into the next mined Block

        Args:

        """
        pass

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
