import hashlib
import time


class Block:

    def __init__(self, id, data, previous_hash,) -> None:
        self.timestamp = time.time()
        self.id = id
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = f"{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    # PoW mining
    def mine(self, difficulty):
        print(f"Starting mining for block {self.id}...")
        start_time = time.time()  # Start time for mining
        self.nonce = 0
        computed_hash = self.compute_hash()
        attempt = 0
        while not computed_hash.startswith('0' * difficulty):
            self.nonce += 1
            computed_hash = self.compute_hash()
            print(f"attempt: {attempt}")
            attempt += 1
        self.hash = computed_hash
        end_time = time.time()  # End time for mining
        mining_time = end_time - start_time  # Time taken to mine the block
        print(
            f"Block {self.id} mined in {mining_time:.2f} seconds with nonce {self.nonce}")
