from shoppinglib.models import Item, ShoppingList, ShoppingListItem, PriceHistory


class ShoppingListManager:

    def manager(self, operation, name=None, market=None, price=None, quantity=None, barcode=None):

        if operation == 'create':
            return ShoppingList.create(
                name=name,
                market=market
            )
        if operation == 'get_list':
            return (
                ShoppingList
                .select()
                .order_by(ShoppingList.created_at.desc())
                .first()
            )
        if operation == 'add_item':
            current_list = self.manager('get_list')

            if not current_list:
                raise Exception("Não foi criada lista de compras")

            item = Item.get_or_none(Item.bar_code == barcode)

            if not item:
                item = Item.create(
                    name=name,
                    bar_code=barcode
                )

            ShoppingListItem.create(
                shopping_list=current_list,
                item=item,
                quantity=quantity,
                price=price
            )

            PriceHistory.create(
                item=item,
                price=price,
                market=current_list.market
            )
        if operation == 'get_items':
            current_list = self.manager('get_list')

            if not current_list:
                return []

            items = []

            for entry in current_list.items:
                item = entry.item
                price = entry.price

                items.append({
                    "name": item.name,
                    "barcode": item.bar_code,
                    "quantity": entry.quantity,
                    "price": price,
                    "total": price * entry.quantity
                })

            return items
        if operation == 'get_item_by_barcode':
            item = Item.get_or_none(Item.bar_code == barcode)

            if not item:
                return None

            last_price = (
                PriceHistory
                .select()
                .where(PriceHistory.item == item)
                .order_by(PriceHistory.created_at.desc())
                .first()
            )

            last_list_item = (
                ShoppingListItem
                .select()
                .where(ShoppingListItem.item == item)
                .order_by(ShoppingListItem.created_at.desc())
                .first()
            )

            return {
                "name": item.name,
                "barcode": item.bar_code,
                "price": last_price.price if last_price else "",
                "quantity": last_list_item.quantity if last_list_item else ""
            }
        else:
            return None
