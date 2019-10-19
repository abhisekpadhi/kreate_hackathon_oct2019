from app.models import Order
from app.models import OrderPickup
from app.models import Transaction
from app.UserManager import UserManager


class OrderManager:
    def __init__(self):
        self.user_manager = UserManager()

    def get_all_orders_for_collector(self, collector_id=None):
        if not collector_id:
            return None

        collector = self.user_manager.get_user_by_id(user_id=collector_id)

        if collector:
            orders_pickups = OrderPickup.objects.filter(collector=collector)
            return orders_pickups
        else:
            return None

    def get_order_by_id(self, order_id=None):
        if not order_id:
            return None

        if Order.objects.filter(id=order_id).exists():
            return Order.objects.get(id=order_id)
        else:
            return None

    def get_payable_by_order(self, order=None):
        if not order:
            return None

        transactions = Transaction.objects.filter(order=order)
        payable = order.total

        if transactions:
            payable = order.total - sum([txn.amt for txn in transactions])

        return payable

