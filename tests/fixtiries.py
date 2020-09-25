from users.models import User, Currency, Trade, Item, Inventory, Offer

from users.serializers import (
    InventorySerializer,
    CurrencySerializer,
    TradeSerializer,
    UserSerializer,
)

from rest_framework.test import APIClient

from django.contrib.auth.hashers import make_password

import pytest

from faker import Faker


@pytest.fixture
def api_client():
    """Func creates and returns client object"""
    return APIClient()


@pytest.fixture
def user():
    """Func generates user data"""
    faker = Faker()
    request_data = {
        "username": faker.user_name(),
        "password": faker.password(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "balance": 10.0

    }

    return request_data


@pytest.fixture
def user_obj_from_db(user):
    """Func creates user in db and return user obj from db"""

    user_obj = User.objects.create(
        username=user['username'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=make_password(user['password']),
        balance=user['balance']
    )
    return user_obj


@pytest.fixture
def user_serializer_data(user_obj_from_db):
    """Func serializes user_obj form db"""
    serializer = UserSerializer(user_obj_from_db)
    serializer_data = serializer.data
    return serializer_data


@pytest.fixture
def auth_api_client(api_client, user_obj_from_db):
    """Func creates auth user"""
    api_client.force_authenticate(user=user_obj_from_db)
    return api_client


@pytest.fixture
def create_currency():
    """Func creates currencies objects in db and return this objects """
    Currency.objects.create(code=1, name='Euro')
    Currency.objects.create(code=2, name='Dollar')
    currencies = Currency.objects.all()
    return currencies


@pytest.fixture
def currency_serializer_data(create_currency):
    """Func serializes currency objects"""
    serializer = CurrencySerializer(create_currency, many=True)
    serializer_data = serializer.data
    return serializer_data


@pytest.fixture
def create_inventory(user_obj_from_db, ):
    """Func create inventory for user_obj_form_db """
    item_1 = Item.objects.create(
        code=1,
        name='item1',
        actual_price=1,
        logo='https://yandex.by/images/search?from=tabbar&text=картинка&pos=21&img_url=https%3A%2F%2Fsun9-64.userapi.com%2Fc854324%2Fv854324709%2F6a2b0%2FWFtqoxXUzEk.jpg&rpt=simage')
    item_2 = Item.objects.create(
        code=2,
        name='item2',
        actual_price=10,
        logo='https://yandex.by/images/search?from=tabbar&text=картинка&pos=21&img_url=tps%3A%2F%2Fsun9-64.userapi.com%2Fc854324%2Fv854324709%2F6a2b0%2FWFtqoxXUzEk.jpg&rpt=simage')
    Inventory.objects.create(user=user_obj_from_db, item=item_1, quantity=10, reversed_quantity=10)
    Inventory.objects.create(user=user_obj_from_db, item=item_2, quantity=10, reversed_quantity=10)
    user_inventory = Inventory.objects.filter(user=user_obj_from_db)
    return user_inventory


@pytest.fixture
def serializer_data_user_inventory(create_inventory):
    """"Func serializes inventory objects"""
    serializer = InventorySerializer(create_inventory, many=True)
    serializer_data = serializer.data
    return serializer_data


@pytest.fixture
def create_offers(user_obj_from_db, create_inventory):
    """Func create offer in db"""
    first_item_index = 0
    inventory_obj = create_inventory[first_item_index]
    item = inventory_obj.item
    item_quantity = inventory_obj.quantity
    buy_offer = Offer.objects.create(
        user=user_obj_from_db,
        item=item,
        order_type='buy',
        entry_quantity=item_quantity,
        quantity=item_quantity,
        price=1.2)
    sell_offer = Offer.objects.create(
        user=user_obj_from_db,
        item=item,
        order_type='sell',
        entry_quantity=item_quantity,
        quantity=item_quantity,
        price=1.2
    )

    return buy_offer, sell_offer


@pytest.fixture
def create_trade(create_offers):
    """Func creates trade in db"""
    buy_offer_index = 0
    sell_offer_index = 1
    buy_offer = create_offers[buy_offer_index]
    sell_offer = create_offers[sell_offer_index]
    buyer = buy_offer.user
    seller = sell_offer.user
    item = buy_offer.item
    quantity = buy_offer.quantity
    price = buy_offer.price
    Trade.objects.create(
        buyer_offer=buy_offer,
        seller_offer=sell_offer,
        buyer=buyer,
        seller=seller,
        item=item,
        quantity=quantity,
        unit_price=price,
    )
    Trade.objects.create(
        buyer_offer=buy_offer,
        seller_offer=sell_offer,
        buyer=buyer,
        seller=seller,
        item=item,
        quantity=quantity,
        unit_price=price,
    )
    trades = Trade.objects.all()
    return trades


@pytest.fixture
def serializer_data_trade(create_trade):
    """Func serializes trade objects"""
    serializer = TradeSerializer(create_trade, many=True)
    serializer_data = serializer.data
    return serializer_data
