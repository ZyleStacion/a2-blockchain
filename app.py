# INTE264[1|2] | Blockchain Technology Fundamentals 
# Created by: Zyle Estacion (s4064846)
# RMIT University

import hashlib
import string
import time
import random

# Block object
class Block:
    def __init__(self, id, timestamp, data, previous_hash, nonce, hash):
        self.id = id
        self.timestamp = timestamp
        self.data = data
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
    
