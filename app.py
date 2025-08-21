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
        print("8. Modify Difficulty")
        print("9. Save Blockchain")      # New
        print("10. Load Blockchain")     # New
        print("11. Blockchain Info")     # New
        print("12. Exit")
        print("="*50)
        
    def create_genesis_block(self):
        if len(self.blockchain.chain) > 0:
            print("❌ Genesis block already exists!")
            return
            
        try:
            print("⛏️ Mining genesis block...")
            # Mine genesis block automatically
            genesis = self.blockchain.new_block(mine=True)
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
            previous_hash = self.blockchain.last_block.current_hash
            new_block = self.blockchain.new_block(previous_hash=previous_hash, mine=True)
            print("\n⛏️ Block mined successfully!")
            print(new_block)
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

    def modify_difficulty_menu(self):
        """Menu for difficulty management"""
        try:
            print(f"\n🎯 Current difficulty: {self.blockchain.difficulty}")
            print(f"Target pattern: {'0' * self.blockchain.difficulty}")
            
            new_difficulty = int(input("Enter new difficulty (1-6 recommended): "))
            self.blockchain.modify_difficulty(new_difficulty)
            
        except ValueError:
            print("❌ Please enter a valid integer")
        except Exception as e:
            print(f"❌ Error modifying difficulty: {e}")

    def save_blockchain(self):
        """Save blockchain to file"""
        try:
            filename = input("Enter filename (default: blockchain.pkl): ").strip()
            if not filename:
                filename = "blockchain.pkl"
            
            if self.blockchain.save_blockchain(filename):
                print("💾 Blockchain saved successfully!")
            
        except Exception as e:
            print(f"❌ Error saving: {e}")

    def load_blockchain(self):
        """Load blockchain from file"""
        try:
            filename = input("Enter filename (default: blockchain.pkl): ").strip()
            if not filename:
                filename = "blockchain.pkl"
            
            if self.blockchain.load_blockchain(filename):
                print("📂 Blockchain loaded successfully!")
                # Show summary
                info = self.blockchain.get_blockchain_info()
                print(f"📊 {info['total_blocks']} blocks, {info['total_transactions']} transactions")
            
        except Exception as e:
            print(f"❌ Error loading: {e}")

    def show_blockchain_info(self):
        """Display blockchain statistics"""
        info = self.blockchain.get_blockchain_info()
        print(f"\n📊 BLOCKCHAIN INFORMATION")
        print("=" * 30)
        print(f"Total Blocks: {info['total_blocks']}")
        print(f"Total Transactions: {info['total_transactions']}")
        print(f"Pending Transactions: {info['pending_transactions']}")
        print(f"Difficulty: {info['difficulty']}")
        print(f"Chain Valid: {'✅ Yes' if info['chain_valid'] else '❌ No'}")
        if info['last_block_hash']:
            print(f"Last Block Hash: {info['last_block_hash'][:16]}...")

    def run(self):
        while True:
            self.show_menu()
            try:
                choice = input("\nEnter your choice (1-12): ").strip()
                
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
                        self.modify_difficulty_menu()
                    case '9':
                        self.save_blockchain()         # New
                    case '10':
                        self.load_blockchain()         # New
                    case '11':
                        self.show_blockchain_info()   # New
                    case '12':
                        print("👋 Goodbye!")
                        sys.exit(0)
                    case _:
                        print("❌ Invalid choice. Please enter 1-12.")
                        
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    cli = BlockchainCLI()
    cli.run()