from users.models import User, Currency, Trade, Item, Inventory, Offer
from users.serializers import UserSerializer, CurrencySerializer, TradeSerializer, InventorySerializer, OfferSerializer

from .fixtiries import api_client, auth_api_client, user, create_bd, currency_serializer_data

import pytest


@pytest.mark.django_db
def test_create_user_post_request(api_client):
    """Test post request to /user/create/"""
    request_data = {"username": "TestUser",
                    "password": "pass123qq",
                    "first_name": "Pav",
                    "last_name": "Martysiuk",
                    "email": "matys3688@gmail.com",
                    "balance": 0

                    }
    url = '/user/create/'
    user_id = 1
    response = api_client.post(url, request_data, format='json')
    response_data = response.data
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user)
    serializer_data = serializer.data
    assert response_data == serializer_data


@pytest.mark.django_db
def test_create_user_get_request(auth_api_client, user):
    user = User.objects.get(username=user['username'])
    user_id = user.id
    serializer = UserSerializer(user)
    serializer_data = serializer.data
    url = f'/user/create/{user_id}/'
    response = auth_api_client.get(url)
    response_data = response.data
    assert response_data == serializer_data


@pytest.mark.django_db
def test_create_user_put_request(auth_api_client, user):
    new_request_data = {
        "username": "TestUser",
        "password": "pass123qq",
        "first_name": "Pav_add",
        "last_name": "Martysiuk",
        "email": "matys3688@gmail.com",
        "balance": 0

    }
    user = User.objects.get(username=user['username'])
    user_id = user.id
    url = f'/user/create/{user_id}/'
    response = auth_api_client.put(url, new_request_data, format='json')
    user = User.objects.get(username=new_request_data['username'])
    serializer = UserSerializer(user)
    serializer_data = serializer.data
    response_data = response.data
    assert response_data == serializer_data


@pytest.mark.django_db
def test_get_currency_request(api_client, currency_serializer_data):
    url = '/user/currency/'
    response = api_client.get(url)
    response_data = response.data
    assert currency_serializer_data == response_data


"""
@pytest.mark.django_db
def test_inventory_get_request(auth_api_client, create_bd):
    user_name = 'TestUser'
    url = '/user/inventory/'
    response = auth_api_client.get(url)
    response_data = response.data
    user = User.objects.get(username=user_name)
    inventory = Inventory(user=user)
    serializer = InventorySerializer(inventory)
    serializer_data = serializer.data
    assert serializer_data == response_data


@pytest.mark.django_db
def test_create_offer_post_request(auth_api_client, create_bd):
    url = '/user/create_offer/'
    user_name = 'TestUser'
    request_data ={
        "item": 2,
        "entry_quantity": 10,
        "order_type": "buy",
        "price": 1.2,
        "quantity": 10

    }
    user = User.objects.get(username=user_name)
    response = auth_api_client.post(url, request_data, format='json')
    offer = Offer.objects.get(user=user, item=request_data['item'])
    serializer = OfferSerializer(offer)
    serializer_data = serializer.data
    response_data = response.data
    assert response_data == serializer_data
"""
