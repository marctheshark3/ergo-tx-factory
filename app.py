from src.builder import ConvertTokens

import json
import os
import threading
import time
from queue import Queue
from flask import Flask, jsonify

app = Flask(__name__)
token_queue = Queue()

@app.route('/')
def index():
    return 'Welcome to my Flask app!'

@app.route('/generate-tokens/<wallet>', methods=['GET'])
def generate_tokens(wallet):
    converter = ConvertTokens()
    tokens = converter.build(wallet)

    tokens_data = {"wallet": wallet, "tokens": tokens}
    token_file = f'tokens_{wallet}.json'
    with open(token_file, 'w') as f:
        json.dump(tokens_data, f)
    
    token_queue.put(wallet)
    return jsonify(tokens_data)

def process_queue():
    while True:
        wallet = token_queue.get()
        if wallet:
            os.system(f'node dist/index.js --wallet={wallet}')
        token_queue.task_done()
        time.sleep(1)  # Simulate processing time

if __name__ == '__main__':
    threading.Thread(target=process_queue, daemon=True).start()
    app.run(port=5000)
