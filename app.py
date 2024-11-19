from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the GroceryItem model
class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    checked = db.Column(db.Boolean, default=False)

# Initialize database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        data = request.json
        new_item = GroceryItem(name=data['name'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'id': new_item.id, 'name': new_item.name, 'checked': new_item.checked}), 201

    all_items = GroceryItem.query.all()
    items = [{'id': item.id, 'name': item.name, 'checked': item.checked} for item in all_items]
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['PUT', 'DELETE'])
def update_or_delete_item(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    if request.method == 'PUT':
        data = request.json
        item.name = data.get('name', item.name)
        item.checked = data.get('checked', item.checked)
        db.session.commit()
        return jsonify({'id': item.id, 'name': item.name, 'checked': item.checked})

    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)


## For querying the database - sqlite 3, SELECT * from grocery_item (grocery_item is the table name)
## Use WSL (ubuntu, not bash)