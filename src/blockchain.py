# Module 1- create a blockchain

from urllib.parse import urlparse
from flask import Flask, jsonify # web server
import datetime # use date time 
import json 
import hashlib #create hash functions
import requests


# Part 1: Create a blockchain
class Blockchain:

    def __init__(self):
        self.chain = [] # chain with list of blocks
        self.txns = [] # list of transactions
        self.nodes = set() #creates a sequence of iterable elements
        self.create_block(proof =1, prev_hash = '0')

    def create_block(self, proof, prev_hash):
        block = {
            'index': len(self.chain) + 1,
            'proof': proof,
            'prev_hash': prev_hash,
            'timestamp': str(datetime.datetime.now()),
            'txns': self.txns
        }
        self.txns = [] # since we added txns to the block, we empty list of txns
        self.chain.append(block)        
        return block
    
    def get_previous_block(self):
        return self.chain[-1] # collects last element in the list
    
    # function to generate proof-of-work. find a nonce that gives a hash below a particular difficulty level
    # difficulty level is set to 0000
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest() # we took an assymetric function so that we don't end up with same hash 2 times (had we used a symmetric function), 
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof # proof of work completed

    # function to create a hash from previous block
    # each block has index, proof, previous hash, timestamp
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        hash_operation= hashlib.sha256(encoded_block).hexdigest()
        return hash_operation
    

    # check if chain is valid
    # this will be done by checking if previous hash of current block is same as has of previous block
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        is_chain_valid = True

        while block_index < len(chain):
            current_block = chain[block_index]
            # chk1 1: check if previous hash of current block is same as hash of previous block
            if current_block['prev_hash'] != self.hash(prev_block):
                is_chain_valid = False
                return is_chain_valid

            # chk 2: check if hash of current block jas 4 leading zeroes (validate proof of work)
            prev_proof = prev_block['proof']
            proof = current_block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()

            if(hash_operation[:4] != '0000'):
                is_chain_valid = False
                return is_chain_valid

            block_index += 1
            prev_block = current_block
        return is_chain_valid

    # Add a new transaction 
    def add_txn (self, txn):
        self.txns.append(txn)
        prev_block = self.get_previous_block() 
        return prev_block["index"] + 1 # returns index of block to which txns will be appended

    # add node by sending address of the node
    # each node is an address 
    # since we are simulating on local, we use multiple ports of a address as a node

    def add_node(self, address):
        parse_url = urlparse(address)
        self.nodes.add(parse_url.netloc)

    # replace chain - consensus algorithm
    # if there is a longest chain in a node, we replace the chain of current node with longest chain
    # loop over all nodes in the network - call a requrest method to access the node
    # Once we get a node, access its chain, check if its a valid chain
    # if its valid, check if length of nodes of that chain is more than current chain
    # if yes, update chain and continue loop untill all nodes in network are covered

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                chain = response.json()["chain"]
                chain_length = response.json()["length"]
                if chain_length > max_length and self.is_chain_valid(chain):
                    max_length = chain_length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False

#Part 2: Mining our block chain

# Connecting a Web app

# app = Flask(__name__)

# blockchain = Blockchain()

# @app.route('/mine_block', methods=['GET'])
# def mine_block():
#     prev_block = blockchain.get_previous_block()
#     prev_proof = prev_block['proof']
#     new_proof = blockchain.proof_of_work(prev_proof)
#     prev_hash = blockchain.hash(prev_block)
#     new_block = blockchain.create_block(new_proof, prev_hash)
#     response = { 'message': 'Congratulations. You just mined a new block', 'index': new_block['index'], 'timestamp': new_block['timestamp'], 'proof': new_block['proof'], 'previous_hash': new_block['prev_hash']}
#     return jsonify(response), 200


# # Getting full blockchain
# @app.route('/get_chain', methods= ['GET'])
# def get_chain():
#     response =  {'message': 'full chain', 'length': len(blockchain.chain), 'chain' : blockchain.chain}
#     return jsonify(response), 200

# # check if blockchain is valid
# @app.route('/is_valid_chain', methods = ['GET'])
# def is_valid_chain():
#     is_valid = blockchain.is_chain_valid(blockchain.chain)
#     response = {'is_valid': is_valid, 'message': f"Block chain is {'valid' if is_valid else 'invalid'}"}
#     return jsonify(response), 200    

# # To listen to all public IP's, we can use the host 0.0.0.0
# # local host - 127.0.0.1: 5000 - this is only used for localhost debug mode
# app.run(host = '0.0.0.0', port=5002 )