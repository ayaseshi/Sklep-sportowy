import os, sys
models_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, models_path)

from models.product import Product
from models.stock import Stock

from flask import Blueprint, jsonify, request

product_details = Blueprint('product_details', __name__, template_folder='templates')

@product_details.route('/api/product-details', methods=['POST'])
async def get_product_detail():
    submitted_data = request.get_json()
    id_p = submitted_data.get('productId')

    product = Product.get_by_id(id_p)

    if product:
        product_dict = product.to_dict()

        stock_list = Stock.get_by_product_id(id_p)
        sizes_and_amounts = {}
        for stock in stock_list:
            sizes_and_amounts[stock.size] = stock.amount

        product_dict['sizes_and_amounts'] = sizes_and_amounts
        return jsonify({'items': product_dict})
    else:
        return jsonify({'error': 'Produktu nie odnaleziono'})