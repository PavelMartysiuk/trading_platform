from __future__ import absolute_import, unicode_literals

from .models import Offer, User, Inventory, Trade

from celery.task import periodic_task

from datetime import timedelta


def edit_balance(buyer, seller, total_price):
    """Func edits user balance"""
    seller.balance += total_price
    buyer.balance -= total_price
    seller.save()
    buyer.save()


def edit_inventory(buyer_item_in_inventory, seller_item_in_inventory, quantity):
    """Func edits item quantity in user inventory"""
    buyer_item_in_inventory.quantity += quantity
    seller_item_in_inventory.quantity -= quantity
    buyer_item_in_inventory.save()
    seller_item_in_inventory.save()


def edit_item_quantity_in_offer(buyer_offer, seller_offer, quantity):
    """Func edits item quantity in offer"""
    buyer_offer.quantity -= quantity
    seller_offer.quantity -= quantity
    buyer_offer.save()
    seller_offer.save()


def write_trade_history(buyer_offer, seller_offer, buyer_id,
                        seller_id, item, quantity, price, ):
    buyer = User.objects.get(id=buyer_id)
    seller = User.objects.get(id=seller_id)
    trade = Trade(buyer_offer=buyer_offer, seller_offer=seller_offer,
                  seller=seller, buyer=buyer, item=item, quantity=quantity,
                  unit_price=price, )
    trade.save()


def change_offer_status(offer):
    """Func changes offer status to False"""
    offer.is_active = False
    offer.save()


def trade(buyer_offer, seller_offer, item, item_price):
    buy_quantity = buyer_offer.quantity
    sell_quantity = seller_offer.quantity
    seller_id = seller_offer.user.id
    buyer_id = buyer_offer.user.id
    seller = User.objects.get(id=seller_id)
    buyer = User.objects.get(id=buyer_id)
    buyer_item_in_inventory = Inventory.objects.get(user=buyer_id, item=item)
    seller_item_in_inventory = Inventory.objects.get(user=seller_id, item=item)

    if buy_quantity >= sell_quantity:
        total_price = item_price * sell_quantity
        edit_item_quantity_in_offer(buyer_offer, seller_offer, sell_quantity)
        edit_balance(buyer, seller, total_price)
        edit_inventory(buyer_item_in_inventory, seller_item_in_inventory, sell_quantity)
        write_trade_history(buyer_offer, seller_offer, buyer_id, seller_id,
                            item, sell_quantity, item_price)
        if buy_quantity == sell_quantity:
            change_offer_status(seller_offer)
            change_offer_status(buyer_offer)
        else:
            change_offer_status(seller_offer)
    elif buy_quantity < sell_quantity:
        total_price = buy_quantity * item_price
        edit_item_quantity_in_offer(buyer_offer, seller_offer, buy_quantity)
        edit_balance(buyer, seller, total_price)
        edit_inventory(buyer_item_in_inventory, seller_item_in_inventory, buy_quantity)
        write_trade_history(
            buyer_offer, seller_offer, buyer_id, seller_id, item, buy_quantity, item_price
        )
        change_offer_status(buyer_offer)


@periodic_task(run_every=timedelta(minutes=1), name='trading')
def trading():
    sell_offers = Offer.objects.filter(order_type='sell', is_active=True)
    buy_offers = Offer.objects.filter(order_type='buy', is_active=True)
    for buy_offer in buy_offers:
        buy_item = buy_offer.item
        buy_item_price = buy_offer.price
        for sell_offer in sell_offers:
            sell_item = sell_offer.item
            sell_item_price = sell_offer.price
            if buy_item == sell_item and buy_item_price == sell_item_price != 0:
                trade(buy_offer, sell_offer, sell_item, buy_item_price)
