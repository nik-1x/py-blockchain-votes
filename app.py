from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from blockchain_core import *

app = Flask(__name__)
app.debug = True

initBlockchain()


@app.route('/')
def index():
    all_blocks_ = getBlocks()
    return render_template("blockchain.html", blocks_all=all_blocks_)

@app.route('/getlastblock')
def last_block():
    block_ = getLastBlock()
    return jsonify(block_)


@app.route('/getAllBlocks')
def all_blocks():
    all_ = getBlocks()
    return jsonify(all_)


@app.route('/validate_block/<block_id>')
def validate_block_by_id(block_id):
    lastblock_id = int(getLastBlock()[0])
    if lastblock_id != 0 and int(block_id) < lastblock_id + 1 and int(block_id) > 0:
        return jsonify({
            "block_id": block_id,
            "is_valid": validate_block(int(block_id))
        })
    else:
        return jsonify({
            "error": "incorrect block_id",
        })


@app.route('/getblock/<block_id>', methods=["GET", "POST"])
def get_block(block_id: int):
    if block_id != "":
        block_id_ = int(block_id)
        last_block = getLastBlock()
        return jsonify(getBlock(block_id_)) if block_id_ > 0 else jsonify({
            "error": "no block with this id"
        })
    else:
        return jsonify({
            "error": "no block with this id"
        })


@app.route('/getblock')
@app.route('/getblock/')
def get_block_404():
    return jsonify({
        "error": "no block given"
    })


@app.route('/addblock/<who>/<vote>')
def add_block(who, vote):
    amo_ = "1"
    addBlock(who, vote, amo_)
    return jsonify({
        "response": [
            f"vote from {who} added to {vote}"
        ]
    })


@app.route('/addblock/')
def add_block_404_1():
    return jsonify({
        "error": "no values given"
    })


@app.route('/addblock/<a>')
@app.route('/addblock/<a>/')
def add_block_404_2(a):
    return jsonify({
        "error": "no values given"
    })


if __name__ == '__main__':
    app.run()
