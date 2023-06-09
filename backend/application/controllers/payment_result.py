from .handle_user import check_user_exists
from application.models.order import Order
from application.models.product import Product
from application.models.delivery_details import DeliveryDetails
from application.models.stock import Stock

from app import redis_client

from flask import Blueprint, jsonify, request

payment_success = Blueprint('payment_success', __name__, template_folder='templates')
payment_failure = Blueprint('payment_failure', __name__, template_folder='templates')

@payment_success.route('/api/successful-payment', methods=['GET'])
def handle_successful_payment():
    user_id = request.args.get('userId')
    order_id = request.args.get('orderId')

    redis_client.delete(user_id)

    order = Order.get_by_id(order_id)
    if order is None or not check_user_exists(user_id):
        return jsonify({'success': False, 'message': 'Nie znaleziono zamówienia o podanym identyfikatorze'})

    order.payment_status = "Paid"
    order.save()

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

@payment_success.route('/api/cancel-payment', methods=['PUT'])
def handle_unsuccessful_payment():
    submitted_data = request.get_json()
    order_id = submitted_data.get('orderId')

    order = Order.get_by_id(order_id)

    if order is None:
        return jsonify({'success': False, 'message': 'Nie znaleziono zamówienia o podanym identyfikatorze'})

    redis_client.delete(order.user_id)

    order.payment_status = "Cancelled"
    order.save()

    restore_stock(order)
                
    return jsonify({'success': True, 'message': 'Płatność została anulowana'})

def restore_stock(order):
    for product_data in order.products:
        product_id = product_data['id']
        product = Product.get_by_id(product_id)
        if product:
            size = product_data['size']
            amount = product_data['amount']
            stock = Stock.get_by_product_id_and_size(product_id, size)
            if stock:
                stock.amount += amount
                stock.save()
