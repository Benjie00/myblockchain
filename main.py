from Block import Block

blockchain = []

genesis_block = Block("The first block!", ["Ben sent 1 nugget to Jeff", "Mario sent 2 nuggets to Luigi"])
print("Genesis block hash: ", genesis_block.block_hash)

second_block = Block(genesis_block.block_hash, ["Mike sent  nuggets 50 to Ben", "Smith sent 10 nuggets to Mario"])

print("second block hash: ", second_block.block_hash)

third_block = Block(second_block.block_hash, ["John sent 5 nuggets to Ben", "Ben sent 7 nuggets to Mike"])

print("third block hash: ", third_block.block_hash)

