# INTE264[1|2] | Blockchain Technology Fundamentals 
# Created by: Zyle Estacion (s4064846)
# RMIT University

"""
CLI interface for interacting with the blockchain.
"""

from blockchain import Blockchain
import sys

class BlockchainCLI:
    def __init__(self):
        self.blockchain = Blockchain()
        
    def show_menu(self):
        print("\n" + "="*50)
        print("🔗 BLOCKCHAIN CLI - INTE264 Assignment 2")
        print("Created by: Zyle Estacion (s4064846)")
        print("="*50)
        print("1. Create Genesis Block")
        print("2. Add Transaction")
        print("3. Mine Block")
        print("4. Display Blockchain")
        print("5. Verify Chain")
        print("6. Edit Block (Demo)")
        print("7. Show Mempool")
        print("8. Exit")
        print("="*50)
        
    def create_genesis_block(self):
        if len(self.blockchain.chain) > 0:
            print("❌ Genesis block already exists!")
            return
            
        try:
            nonce = int(input("Enter nonce for genesis block: "))
            genesis = self.blockchain.new_block(nonce=nonce)
            print("\n🎉 Genesis block created!")
            print(genesis)
        except ValueError:
            print("❌ Please enter a valid number for nonce")
        except Exception as e:
            print(f"❌ Error creating genesis block: {e}")
    
    def add_transaction(self):
        try:
            sender = input("Enter sender: ").strip()
            receiver = input("Enter receiver: ").strip()
            amount = float(input("Enter amount: "))
            
            result = self.blockchain.new_transaction(sender, receiver, amount)
            if result:
                print(f"📝 Transaction will be included in block {result}")
        except ValueError:
            print("❌ Please enter a valid amount")
        except Exception as e:
            print(f"❌ Error adding transaction: {e}")
    
    def mine_block(self):
        if len(self.blockchain.chain) == 0:
            print("❌ Create genesis block first!")
            return
            
        if len(self.blockchain.mempool) == 0:
            print("❌ No transactions in mempool to mine!")
            return
            
        try:
            nonce = int(input("Enter nonce for new block: "))
            previous_hash = self.blockchain.last_block.current_hash
            
            new_block = self.blockchain.new_block(nonce=nonce, previous_hash=previous_hash)
            print("\n⛏️ Block mined successfully!")
            print(new_block)
        except ValueError:
            print("❌ Please enter a valid number for nonce")
        except Exception as e:
            print(f"❌ Error mining block: {e}")
    
    def display_blockchain(self):
        self.blockchain.display_chain()
    
    def verify_chain(self):
        print("\n🔍 Verifying blockchain integrity...")
        self.blockchain.verify_chain()
    
    def edit_block_demo(self):
        print("\n🛠️ Block Editing Demo (Security Test)")
        print("This will modify a block to demonstrate chain integrity detection")
        
        if len(self.blockchain.chain) < 2:
            print("❌ Need at least 2 blocks to demonstrate editing")
            return
            
        print("\nBefore modification:")
        self.blockchain.verify_chain()
        
        self.blockchain.edit_block()
        
        print("\nAfter modification:")
        self.blockchain.verify_chain()
    
    def show_mempool(self):
        if len(self.blockchain.mempool) == 0:
            print("📝 Mempool is empty")
        else:
            print(f"\n📝 MEMPOOL ({len(self.blockchain.mempool)} transactions)")
            print("-" * 30)
            for i, tx in enumerate(self.blockchain.mempool, 1):
                print(f"{i}. {tx['sender']} → {tx['receiver']}: {tx['amount']}")
    
    def run(self):
        while True:
            self.show_menu()
            try:
                choice = input("\nEnter your choice (1-8): ").strip()
                
                match choice:
                    case '1':
                        self.create_genesis_block()
                    case '2':
                        self.add_transaction()
                    case '3':
                        self.mine_block()
                    case '4':
                        self.display_blockchain()
                    case '5':
                        self.verify_chain()
                    case '6':
                        self.edit_block_demo()
                    case '7':
                        self.show_mempool()
                    case '8':
                        print("👋 Goodbye!")
                        sys.exit(0)
                    case _:
                        print("❌ Invalid choice. Please enter 1-8.")
                        
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    cli = BlockchainCLI()
    cli.run()