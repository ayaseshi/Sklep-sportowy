import os, sys
models_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, models_path)

from models.product import Product

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, backend_path)

from config.FirebaseManager import FirebaseManager

firebase_manager = FirebaseManager()

from flask import Blueprint, jsonify, request

main_page_products = Blueprint('main_page_products', __name__, template_folder='templates')
main_page_products_filtered = Blueprint('main_page_products_filtered', __name__, template_folder='templates')

@main_page_products.route('/api/products', methods=['GET'])
async def get_products():
    pageIndex = int(request.args.get('pageIndex'))
    pageSize = int(request.args.get('pageSize'))

    start_index = pageIndex * pageSize
    end_index = start_index + pageSize

    products = Product.get_recently_added(end_index)
    products = products[start_index:end_index]

    products_dict = [product.to_dict() for product in products]
    return jsonify({'items': products_dict, 'totalItems': Product.get_product_count()})

@main_page_products_filtered.route('/api/filtered-products', methods=['GET'])
async def get_products_filtered():
    pageIndex = int(request.args.get('pageIndex'))
    pageSize = int(request.args.get('pageSize'))
    price_order = str(request.args.get('priceOrder'))
    category_id = str(request.args.get('category'))
    brand_id = str(request.args.get('brand'))

    start_index = pageIndex * pageSize
    end_index = start_index + pageSize

    products = Product.get_all()

    if price_order == 'asc':
        products.sort(key=lambda p: float(p.price))
    elif price_order == 'desc':
        products.sort(key=lambda p: float(p.price), reverse=True)
    else:
        products.reverse()

    if category_id != 'None':
        products = [product for product in products if product.category_id == category_id]

    if brand_id != 'None':
        products = [product for product in products if product.brand_id == brand_id]

    products = products[start_index:end_index]
    products_dict = [product.to_dict() for product in products]
    return jsonify({'items': products_dict, 'totalItems': len(products_dict)})