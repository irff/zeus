from flask import jsonify

from zeus import app
from zeus.services import category as _category
from zeus.utils import auth

@app.route("/categories", methods=['GET'])
@auth.require_token
def get_categories():
    categories = _category.get_categories()

    categories_json = []
    for category in categories:
        categories_json.append(category.name)

    return jsonify({
        'categories': categories_json
    }), 200
