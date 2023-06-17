import os, sys
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, backend_path)

from app import redis_client

models_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, models_path)

from models.order import Order
from models.product import Product
from models.delivery_details import DeliveryDetails

from flask import Blueprint, jsonify, request, redirect

payment_success = Blueprint('payment_success', __name__, template_folder='templates')
payment_failure = Blueprint('payment_failure', __name__, template_folder='templates')

@payment_success.route('/api/successful-payment', methods=['GET'])
async def handle_successful_payment():
    user_id = request.args.get('userId')
    order_id = request.args.get('orderId')

    redis_client.delete(user_id)

    order = Order.get_by_id(order_id)
    order.payment_status = "Paid"
    order.save()
    
    if order is None:
        return jsonify({'success': False, 'message': 'Nie znaleziono zamówienia o podanym identyfikatorze'})

    products = []
    for product_data in order.products:
        product = Product.get_by_id(product_data['id'])
        if product:
            product_dict = product.to_dict()
            product_dict['amount'] = product_data['amount']
            products.append(product_dict)

    delivery_details = DeliveryDetails.get_by_id(order.delivery_data_id)
    if delivery_details is None:
        return jsonify({'success': False, 'message': 'Nie znaleziono szczegółów dostawy dla zamówienia'})

    order_dict = order.to_dict()
    order_dict['products'] = products
    order_dict['delivery_details'] = delivery_details.to_dict()

    return jsonify({'success': True, 'message': 'Zamówienie zostało zakończone', 'order': order_dict})

@payment_failure.route('/api/payment', methods=['GET'])
async def handle_unsuccessful_payment():
    pass