# INTE264[1|2] | Blockchain Technology Fundamentals 
# Created by: Zyle Estacion (s4064846)
# RMIT University

import hashlib
import time

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