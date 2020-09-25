from users.models import User, Offer
from users.serializers import OfferSerializer, UserSerializer

from tests.fixtiries import (
    serializer_data_user_inventory,
    currency_serializer_data,
    serializer_data_trade,
    user_serializer_data,
    create_inventory,
    user_obj_from_db,
    auth_api_client,
    create_currency,
    create_offers,
    create_trade,
    api_client,
    user,
)

import pytest

from faker import Faker


@pytest.mark.django_db
def test_create_user_post_request(api_client, user):
    """Test post request to /user/create/"""
    url = '/user/'
    response = api_client.post(url, user, format='json')
    response_data = response.data
    user = User.objects.get(username=user['username'])
    serializer = UserSerializer(user)
    serializer_data = serializer.data
    assert response_data == serializer_data


@pytest.mark.django_db
def test_create_user_get_request(auth_api_client, user_serializer_data):
    user_id = user_serializer_data['id']
    url = f'/user/{user_id}/'
    response = auth_api_client.get(url)
    response_data = response.data
    assert response_data == user_serializer_data


@pytest.mark.django_db
def test_create_user_put_request(auth_api_client, user_serializer_data, user):
    faker = Faker()
    user['first_name'] = faker.first_name()
    user_id = user_serializer_data['id']
    url = f'/user/{user_id}/'
    response = auth_api_client.put(url, user, format='json')
    user_obj = User.objects.get(username=user['username'])
    serializer = UserSerializer(user_obj)
    serializer_data = serializer.data
    response_data = response.data
    assert response_data == serializer_data


@pytest.mark.django_db
def test_get_currency_request(api_client, currency_serializer_data):
    url = '/user/currency/'
    response = api_client.get(url)
    response_data = response.data
    assert currency_serializer_data == response_data


@pytest.mark.django_db
def test_get_currency_request_with_pk(api_client, currency_serializer_data):
    first_item_index = 0
    serializer_currency_data = currency_serializer_data[first_item_index]
    currency_id = serializer_currency_data['id']
    url = f'/user/currency/{currency_id}/'
    response = api_client.get(url)
    response_data = response.data
    assert response_data == serializer_currency_data


@pytest.mark.django_db
def test_inventory_get_request(auth_api_client, serializer_data_user_inventory):
    url = '/user/inventory/'
    response = auth_api_client.get(url)
    response_data = response.data
    assert serializer_data_user_inventory == response_data


@pytest.mark.django_db
def test_inventory_get_request_with_pk(auth_api_client, serializer_data_user_inventory):
    first_item_index = 0
    inventory_serializer_data = serializer_data_user_inventory[first_item_index]
    inventory_id = inventory_serializer_data['id']
    url = f'/user/inventory/{inventory_id}/'
    response = auth_api_client.get(url)
    response_data = response.data
    assert inventory_serializer_data == response_data


def offer_serializer_data(user, item, order_type):
    offer = Offer.objects.get(user=user, item=item, order_type=order_type)
    serializer = OfferSerializer(offer)
    serializer_data = serializer.data
    return serializer_data


@pytest.mark.django_db
def test_create_offer_post_request(auth_api_client, create_inventory, user_obj_from_db):
    url = '/user/create_offer/'
    first_item_index = 0
    item = create_inventory[first_item_index]
    item_id = item.id
    item_quantity = item.quantity

    request_data = {
        "item": item_id,
        "entry_quantity": item_quantity,
        "order_type": "buy",
        "price": 1.2,

    }
    response = auth_api_client.post(url, request_data, format='json')
    response_data = response.data
    serializer_data = offer_serializer_data(user=user_obj_from_db, item=request_data['item'],
                                            order_type=request_data['order_type'])
    assert response_data == serializer_data


@pytest.mark.django_db
def test_trade_history_get_request(api_client, serializer_data_trade):
    url = '/user/trade_history/'
    response = api_client.get(url)
    response_data = response.data
    assert serializer_data_trade == response_data


@pytest.mark.django_db
def test_trade_history_request_with_pk(api_client, serializer_data_trade):
    first_item_index = 0
    trade_serializer_data = serializer_data_trade[first_item_index]
    trade_id = trade_serializer_data['id']
    url = f'/user/trade_history/{trade_id}/'
    response = api_client.get(url)
    response_data = response.data
    assert response_data == trade_serializer_data
