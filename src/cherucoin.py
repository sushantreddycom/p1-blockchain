# Tutorial 2 - Create a crypto currency called 'Cherucoin'

from crypt import methods
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
from blockchain import Blockchain

from uuid import uuid4
from urllib.parse import urlparse

class Cherucoin(Blockchain):
    def __init__(self):
        super().__init__()

    def add_txn (self, sender, receiver, amount):
        return super().add_txn({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }) 


# app = Flask(__name__)

# cheruCoin = Cherucoin()

# # Create a node address
# @app.route('/mine_cherucoin', methods=['GET'])
# def mine_cherucoin():
#     prev_block = cheruCoin.get_previous_block()
#     prev_proof = prev_block['proof']
#     new_proof = cheruCoin.proof_of_work(prev_proof)
#     prev_hash = cheruCoin.hash(prev_block)
#     new_block = cheruCoin.create_block(new_proof, prev_hash)
#     response = {'message': 'Congratulations. You added a new block', 'index': new_block['index'], 'timestamp': new_block['timestamp'], 'proof': new_block['proof'], 'prev_hash': new_block['prev_hash'], 'transactions': new_block['txns']}
#     return jsonify(response), 200

# @app.route('/post_txns', methods=['POST'])
# def post_txns():
#     txn_json = request.get_json()
#     txn_keys = ['sender', 'receiver', 'amount']
#     if not all (key in txn_json for key in txn_keys):
#         response = {'message': 'Some elements in transaction are missing'}
#         return jsonify(response), 400 

#     index = cheruCoin.add_txn(txn_json['sender'], txn_json['receiver'], txn_json['amount'])
#     response = {'message': 'Transactions added to block', 'block_index': index, 'transaction': cheruCoin.txns[-1] }
#     return jsonify(response), 201


# # connecting new nodes to the network
# @app.route('/connect_node', methods=['POST'])
# def connect_nodes():
#     nodes_json = request.get_json()
#     node_addresses = nodes_json.get('nodes')
#     if node_addresses is None:
#         response = {'message': 'No nodes'}
#         return jsonify(response), 400
 
#     for address in node_addresses:
#         cheruCoin.add_node(address) 
    
#     return jsonify({'message': f'All nodes connected. Total nodes in block chain are {len(cheruCoin.nodes)}', 'nodes': list(cheruCoin.nodes)}), 201

# # creating a consensus across all nodes in the network
# @app.route ('/consensus', methods=['GET'])
# def consensus():
#     is_chain_replaced = cheruCoin.replace_chain()
#     if is_chain_replaced:
#         response = {'message': 'Chain is successfully replaced with longest chain' , 'chain': cheruCoin.chain}
#     else:
#         response = {'message': 'All good. Chain is the longest ' }

#     return jsonify(response), 200

# To listen to all public IP's, we can use the host 0.0.0.0
# local host - 127.0.0.1: 5000 - this is only used for localhost debug mode
# app.run(host = '0.0.0.0', port=5002 )




