import hashlib

class Block:

    def __init__(self, previous_hash, transactionArr) -> None:
        self.transactionArr = transactionArr
        self.previous_hash = previous_hash
        
        string_to_hash = "".join(transactionArr) + previous_hash #string containing all the transactions appended together with the previous_hash string appended to it. 

        self.block_hash = hashlib.sha256(string_to_hash.encode()).hexdigest() #turn the string_to_hash into a unicode, then hash it, then turn the hashcode into a string.  


        
