from flask import Flask, jsonify, request

app = Flask(__name__)

items = [
    {"id": 1, "name": "Cong Zhou", "description": "This is Cong Zhou"},
    {"id": 2, "name": "Rui Bao", "description": "This is Rui Bao"}
]


@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404


@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.get_json()
    new_item['id'] = items[-1]['id'] + 1 if items else 1
    items.append(new_item)
    return jsonify(new_item), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = request.get_json()
    for item in items:
        if item['id'] == item_id:
            item.update(updated_item)
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({"message": "Item deleted"})


if __name__ == '__main__':
    app.run(debug=True)