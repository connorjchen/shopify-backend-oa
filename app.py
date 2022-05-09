import json
from flask import Flask, jsonify, request, make_response, abort

app = Flask(__name__)

inventory = [
  {
    'id': 1,
    'name': "Chairs",
    'count': 3,
  },
  {
    'id': 4,
    'name': "Tables",
    'count': 2,
  }
]

deletions = [
  {
    'id': 2,
    'name': "Spoons",
    'count': 19,
    'comment': "Sold all spoons to IKEA"
  },
  {
    'id': 3,
    'name': "Forks",
    'count': 32,
    'comment': "Sold all spoons to Target"
  }
]

id_count = 5

@app.route('/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@app.route('/api/inventory/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def process_inventory_request():
  if (request.method == 'GET'):
    return make_response(jsonify({'success':True, 'data':inventory}), 200)
  elif (request.method == 'POST'):
    user_input = request.json
    if not user_input.get('name') or not user_input.get('count'):
      return make_response(jsonify({'success':False, 'error':'Name or count not found'}), 404)
    global id_count
    inventory.append({
      'id': id_count,
      'name': user_input.get('name'),
      'count': user_input.get('count')
    })
    id_count += 1
    return make_response(jsonify({'success':True, 'data':inventory}), 201)
  elif (request.method == 'PATCH'):
    user_input = request.json
    if not user_input.get('id'):
      return make_response(jsonify({'success':False, 'error':'id not found'}), 404)
    idx = 0
    while(True):
      if(inventory[idx]['id'] == user_input.get('id')):
        break
      idx += 1
    if user_input.get('name'):
      inventory[idx]['name'] = user_input.get('name')
    if user_input.get('count'):
      inventory[idx]['count'] = user_input.get('count')
    return make_response(jsonify({'success':True, 'data':inventory}), 200)
  elif (request.method == 'DELETE'):
    user_input = request.json
    if not user_input.get('id') or user_input.get('isDelete') is None:
      return make_response(jsonify({'success':False, 'error':'id or delete/undelete type not found'}), 404)
    if user_input.get('isDelete') == True:
      idx = 0
      while(True):
        if(inventory[idx]['id'] == user_input.get('id')):
          break
        idx += 1
      deletions.append(inventory[idx])
      del inventory[idx]
      if(user_input.get('comment')):
        deletions[len(deletions) - 1]['comment'] = user_input.get('comment')
      else:
        deletions[len(deletions) - 1]['comment'] = ""
      return make_response(jsonify({'success':True, 'data':deletions}), 200)
    else:
      idx = 0
      while(True):
        if(deletions[idx]['id'] == user_input.get('id')):
          break
        idx += 1
      deletions[idx].pop('comment')
      inventory.append(deletions[idx])
      del deletions[idx]
      return make_response(jsonify({'success':True, 'data':inventory}), 200)
    

@app.route('/api/deletions/', methods=['GET'])
def process_deletions_request():
  if (request.method == 'GET'):
    return make_response(jsonify({'success':True, 'data':deletions}), 200)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# deletion no work