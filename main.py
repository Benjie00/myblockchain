from Blockchain import Blockchain
from Block import Block

if __name__ == "__main__":

    blockchain = Blockchain()

    # Adding blocks to the chain
    blockchain.add_block("the big Block")

    blockchain.save_blockchain_to_file()

    # Displaying the blockchain
    for block in blockchain.chain:
        print(f"Block Hash {block.id}: {block.hash}")
