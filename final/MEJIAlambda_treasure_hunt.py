from map_graph import graph
import json
import time
import random
import requests


"""
# Lambda Treasure Hunt - CS BW2
"""

# Set up token
token = "d7eb25dbcc55709091aa150b7a0ad1c255b64ae4"

# Initialization
# get current location and other stats before moving

def init(token):
    url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
    current = requests.get(url, headers={"Authorization": f"Token {token}"}).json()
    return current


def status_check():
    url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/status/"
    result = requests.post(
        url,
        headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
    )
    return result.json()


# Breadth First Search - Find the path from current location to target location
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def bfs(starting_room, destination):
    queue = Queue()
    queue.enqueue([starting_room])
    visited = set()
    while queue.size() > 0:
        path = queue.dequeue()
        room_id = path[-1]
        if room_id not in visited:
            if room_id == destination:
                return path
            else:
                for direction in graph[room_id][0]:
                    # if graph[room_id][0][direction] != "?":
                    new_path = path.copy()
                    new_path.append(graph[room_id][0][direction])
                    queue.enqueue(new_path)
            visited.add(room_id)
    return []


current = init(token)
status_check()


def movement(direction, next_room_id=None):
    url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    if next_room_id is not None:
        data = f'{{"direction":"{direction}","next_room_id": "{next_room_id}"}}'
    else:
        data = f'{{"direction":"{direction}"}}'

    result = requests.post(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
    ).json()
    return result

def journey(goal_room):
    path = bfs(55, 126)
    directions = []

    current = path[0]
    for room in path[1:]:
        options = graph[current][0]
        for item in options.items():
            if item[1] == room:
                journey.append(item)
                current = room

    for step in directions:
        results = movement(step[0], step[1])
        time.sleep(results["cooldown"])


# Take treasure
def take_item(treasure):
    url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/"
    data = f'{{"name":"{treasure}"}}'
    result = requests.post(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
    ).json()
    if len(result["errors"]) > 0:
        print(result["errors"])
    else:
        print(f"Taking {treasure}!")
    return result


# Sell Treasure
def sell_item(treasure):
    url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/"
    data = f'{{"name":"{treasure}", "confirm":"yes"}}'
    result = requests.post(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
    ).json()
    print(f"Selling {treasure} to shop.\n{result}")
    return result


# Sell all treasures
def sell_itmes_all():
    time.sleep(current['cooldown'])
    items = status_check()['inventory']
    for item in items:
    if 'treasure' in item:
        current = sell_item(item)
        time.sleep(current['cooldown'])

def name_change(new_name):
  url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/'
  data = f'{{"name":"{new_name}", "confirm":"aye"}}'
  result = requests.post(url, data=data,
                         headers={'Content-Type':'application/json',
                                  'Authorization': f'Token {token}'}).json()
  return result



"""
### Pray
"""
# Shrine - need to change name first
# 461 - Dash: You feel a mysterious power and speed coiling in your legs.
# 22 - Fly: Good for all places except cave terrain.
# 374 - Warp: needs items to use warp ability

def pray():
  url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/'
  result = requests.post(url, headers={'Content-Type':'application/json',
                                       'Authorization': f'Token {token}'})
  return result.json()

def wishing_well():
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/'
    data = f'{{"name":"well"}}'
    result = requests.post(url, data=data,
                            headers={'Content-Type':'application/json',
                                    'Authorization': f'Token {token}'}).json()
    print(result['description'])
    return result

def msg_decode(message):
  split_msg = message.split('\n')[2:]
  chr_msg = [chr(int(c,2)) for c in split_msg]
  decipher_msg = [chr_msg[x] for x in range(2,len(chr_msg),5)]
  decode_msg = "".join(decipher_msg)
  return int(''.join(i for i in decode_msg if i.isdigit()))

def get_last_proof():

  url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/'
  result = requests.get(url, 
                        headers={'Content-Type':'application/json',
                                 'Authorization': f'Token {token}'}).json()
  return result

def proof_of_work(last_proof, current_level):
    """
    Get the last valid proof to use to mine a new block. 
    Also returns the current difficulty level, which is the number of 0's 
    required at the beginning of the hash for a new proof to be valid.
    The proof of work algorithm for this blockchain is 
    not the same as we used in class.
    """
    start = timer()
    print(f"\nLast proof: {last_proof} -- Searching for next proof..\n")
    proof = 1000000
    while valid_proof(last_proof, proof, current_level) is False:
      proof += 1
    print(f"Proof found: {proof} in {timer() - start:.3f}s")
    return proof

def proof_of_work(last_proof, current_level):
    """
    Get the last valid proof to use to mine a new block. 
    Also returns the current difficulty level, which is the number of 0's 
    required at the beginning of the hash for a new proof to be valid.
    The proof of work algorithm for this blockchain is 
    not the same as we used in class.
    """
    start = timer()
    print(f"\nLast proof: {last_proof} -- Searching for next proof..\n")
    proof = 1000000
    while valid_proof(last_proof, proof, current_level) is False:
      proof += 1
    print(f"Proof found: {proof} in {timer() - start:.3f}s")
    return proof

def mine_coin(new_proof):
  url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/'
  data = f'{{"proof":{new_proof}}}'
  result = requests.post(url, data=data,
                         headers={'Content-Type':'application/json',
                                  'Authorization': f'Token {token}'}).json()
  return result

def mvp():
    from timeit import default_timer as timer
    # Run forever until interrupted
    while True:
    # Get the last proof from the server
    current_proof = get_last_proof()
    time.sleep(1)
    proof = current_proof['proof']
    current_level = current_proof['difficulty']

    new_proof = proof_of_work(proof, current_level)
    reponse = mine_coin(new_proof)
    print(reponse)
    time.sleep(reponse['cooldown'])

def coin_balance():
  url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/'
  result = requests.get(url, 
                        headers={'Content-Type':'application/json',
                                 'Authorization': f'Token {token}'}).json()
  return result
