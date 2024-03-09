import json
from Block import Block


class Blockchain:

    def __init__(self):
        self.difficulty = 5  # Initial difficulty
        # Target time to mine a block (seconds)
        self.TARGET_BLOCK_TIME = 10
        self.ADJUSTMENT_INTERVAL = 10
        self.chain = []
        # Automatically attempt to load the existing blockchain
        self.load_blockchain_from_file()

    def create_genesis_block(self):
        genesis_block = Block(0, "Genesis Block", "0")
        genesis_block.mine(self.difficulty)
        return genesis_block

    def add_block(self, data):
        # The ID of the new block is the current length of the chain
        block_id = len(self.chain)
        previous_hash = self.chain[-1].hash if self.chain else "0"
        # Create a new block with the next ID, data, and the previous block's hash
        new_block = Block(block_id, data, previous_hash)
        new_block.mine(self.difficulty)

        # Difficulty adjustment and validation logic remains the same
        if len(self.chain) % self.ADJUSTMENT_INTERVAL == 0:
            self.adjust_difficulty()

        # Temporarily append the new block for validation
        temp_chain = self.chain[:] + [new_block]
        if self.is_valid(temp_chain):
            self.chain.append(new_block)
        else:
            raise ValueError("Invalid block or blockchain state.")

    def is_valid(self, chain):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            # Check that the block's hash is correct
            if current_block.hash != current_block.compute_hash():
                print("Invalid block hash on ")
                return False

            # Check that the block points to the correct previous block
            if current_block.previous_hash != previous_block.hash:
                return False

            # Optional: Check if the hash meets the difficulty criteria
            # This might involve re-verifying the PoW, which can be computationally intensive
            # For simplicity, you might skip this or use a lighter check
        return True

    def adjust_difficulty(self):
        if len(self.chain) <= self.ADJUSTMENT_INTERVAL:
            return  # Not enough blocks to adjust difficulty

        # Calculate the time taken to mine the last ADJUSTMENT_INTERVAL blocks
        start_time = self.chain[-self.ADJUSTMENT_INTERVAL - 1].timestamp
        end_time = self.chain[-1].timestamp
        actual_time_taken = end_time - start_time

        # Calculate the expected time to mine ADJUSTMENT_INTERVAL blocks
        expected_time = self.TARGET_BLOCK_TIME * self.ADJUSTMENT_INTERVAL

        # Adjust difficulty
        if actual_time_taken < expected_time / 2:
            self.difficulty += 1  # Increase difficulty if blocks are mined too quickly
        elif actual_time_taken > expected_time * 2:
            # Decrease difficulty if blocks are mined too slowly, but keep it at least 1
            self.difficulty = max(1, self.difficulty - 1)

    def save_blockchain_to_file(self, filename="blockchain.json"):
        chain_data = []
        for block in self.chain:
            chain_data.append(block.__dict__)

        with open(filename, 'w') as file:
            json.dump(chain_data, file, indent=4)

    def load_blockchain_from_file(self, filename="blockchain.json"):
        try:
            with open(filename, 'r') as file:
                if file.read(1):  # Check if the file is not empty
                    file.seek(0)  # Reset file read position
                    chain_data = json.load(file)
                    self.chain = [self.dict_to_block(
                        data) for data in chain_data]
                else:
                    # File is empty, handle accordingly (e.g., initialize a new blockchain)
                    self.chain = [self.create_genesis_block()]
        except FileNotFoundError:
            self.chain = [self.create_genesis_block()]

    def dict_to_block(self, block_dict):
        # Create a Block object from block_dict without computing the hash again
        block = Block(
            id=block_dict['id'],
            data=block_dict['data'],
            previous_hash=block_dict['previous_hash']
        )
        # Set attributes directly to avoid recomputing the hash unintentionally
        block.timestamp = block_dict['timestamp']
        block.nonce = block_dict['nonce']
        # Assuming the hash was saved and is correct
        block.hash = block_dict['hash']

        return block
