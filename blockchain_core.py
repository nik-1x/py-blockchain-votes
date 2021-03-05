import sqlite3
import hashlib
import datetime as date
import json

appconfig = {
    "prefix": "EZC",
    "db": ":memory:"
}

db = sqlite3.connect(appconfig["db"], check_same_thread=False)
cur = db.cursor()


def md5(str_v):
    stv = str(str_v).encode('utf-8')
    m = hashlib.md5()
    m.update(stv)
    return m.hexdigest()


def initBlockchain():
    global db, cur
    cur.execute("""CREATE TABLE IF NOT EXISTS blocks(
                    block_id INT,
                    prev_block_hash TEXT,
                    block_target TEXT,
                    block_sender TEXT,
                    block_amount TEXT,
                    block_hash TEXT,
                    block_time TEXT
                );""")
    # genesis block
    createBlock(1, "", "null", "null", 0, f"User null sent 0 {appconfig['prefix']} to user null",
                date.datetime.now())
    db.commit()


def createBlock(block_id, prev_hash, target, sender, amount, hash_, time):
    global db, cur
    cur.execute(f"""INSERT INTO blocks VALUES (
        '{block_id}', '{prev_hash}', '{target}', '{sender}', '{amount}', '{md5(hash_)}', '{time}'
    )""")


def getBlocks():
    global db, cur
    cur.execute("""SELECT * from blocks""")
    data = cur.fetchall()
    return data


def getLastBlock():
    all = getBlocks()
    if len(all) > 0:
        return all[-1]
    else:
        return [0]


def getBlock(block_id):
    global db, cur
    cur.execute(f"""SELECT * from blocks WHERE block_id='{block_id}'""")
    return cur.fetchall()


def addBlock(from_, to_, amount_):
    if int(getLastBlock()[0]) == 0:
        # genesis block
        createBlock(1, "", "null", "null", 0, f"User null sent 0 {appconfig['prefix']} to user null",
                    date.datetime.now())
    last_block = getLastBlock()
    last_block_data = json.dumps({
        "block_id": last_block[0],
        "prev_block_hash": last_block[1],
        "block_target": last_block[2],
        "block_sender": last_block[3],
        "block_amount": last_block[4],
        "block_hash": last_block[5],
        "block_time": last_block[6]
    })
    prev_block_hash = md5(last_block_data)
    createBlock((last_block[0] + 1), prev_block_hash, from_, to_, amount_,
                f"User {from_} sent {amount_} {appconfig['prefix']} to user {to_}", date.datetime.now())


def validate_block(block_id):
    curr_block = getBlock(block_id)
    if getLastBlock()[0] == block_id:
        return True
    next_block = getBlock(block_id + 1)

    current_block_hash = md5(json.dumps({
        "block_id": curr_block[0][0],
        "prev_block_hash": curr_block[0][1],
        "block_target": curr_block[0][2],
        "block_sender": curr_block[0][3],
        "block_amount": curr_block[0][4],
        "block_hash": curr_block[0][5],
        "block_time": curr_block[0][6]
    }))
    if current_block_hash == next_block[0][1]:
        return True
    else:
        return False

