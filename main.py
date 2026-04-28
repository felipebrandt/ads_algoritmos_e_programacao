from shoppinglib.users import user_exists, create_user, get_user_password
from shoppinglib.shopping_list import ShoppingListManager


class App:

    def __init__(self):
        self.shopping = ShoppingListManager()

    @staticmethod
    def validate_login(login, password):
        if not user_exists(login):
            return False
        saved_password = get_user_password(login)
        return saved_password == password

    @staticmethod
    def register_user(username, password):
        if user_exists(username):
            return False
        create_user(username, password)
        return True

    def create_list(self, name, market):
        return self.shopping.manager('create',name=name, market=market)

    def add_item(self, name, barcode, price, quantity):
        return self.shopping.manager('add_item',name=name, barcode=barcode, price=price, quantity=quantity)

    def get_items(self):
        return self.shopping.manager('get_items')

    def get_item_by_barcode(self, barcode):
        return self.shopping.manager('get_item_by_barcode',barcode=barcode)

