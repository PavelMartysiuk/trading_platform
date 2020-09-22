import pytest
from users.models import User, Currency, Trade, Item, Inventory, Offer
from users.serializers import UserSerializer, CurrencySerializer, TradeSerializer, InventorySerializer, OfferSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient


@pytest.fixture
def user():
    """Func creates user in bd and returns user data using serializer """
    request_data = {
        "username": "TestUser",
        "password": "pass123qq",
        "first_name": "Pav",
        "last_name": "Martysiuk",
        "email": "matys3688@gmail.com",
        "balance": 0

    }
    User.objects.create(username=request_data["username"],
                        password=make_password(request_data["password"]),
                        first_name=request_data["first_name"],
                        last_name=request_data["last_name"],
                        email=request_data["email"],
                        balance=request_data["balance"]
                        )

    return request_data


@pytest.fixture
def create_bd(user):
    user_name = 'TestUser'
    user = User.objects.get(username=user_name)
    item_1 = Item.objects.create(code=1, name='item1', actual_price=1,
                                 logo='https://yandex.by/images/search?from=tabbar&text=картинка&pos=21&img_url=https%3A%2F%2Fsun9-64.userapi.com%2Fc854324%2Fv854324709%2F6a2b0%2FWFtqoxXUzEk.jpg&rpt=simage')
    item_2 = Item.objects.create(code=2, name='item2', actual_price=10,
                                 logo='https://yandex.by/images/search?from=tabbar&text=картинка&pos=21&img_url=tps%3A%2F%2Fsun9-64.userapi.com%2Fc854324%2Fv854324709%2F6a2b0%2FWFtqoxXUzEk.jpg&rpt=simage')
    Inventory.objects.create(user=user, item=item_1, quantity=10, reversed_quantity=10)
    Inventory.objects.create(user=user, item=item_2, quantity=10, reversed_quantity=10)


@pytest.fixture
def currency_serializer_data():
    """Func creates currency objects in bd and returns this data using serializer"""
    Currency.objects.create(code=1, name='Euro')
    Currency.objects.create(code=2, name='Dollar')
    currencies = Currency.objects.all()
    serializer = CurrencySerializer(currencies, many=True)
    serializer_data = serializer.data
    return serializer_data


@pytest.fixture
def api_client():
    """Func creates and returns client object"""
    return APIClient()


@pytest.fixture
def auth_api_client(api_client, user):
    """Func creates and returns auth user"""
    auth_url = '/auth/jwt/create/'
    response = api_client.post(auth_url, user, format='json')
    access_token = response.data['access']
    access_token = 'Bearer' + access_token
    api_client.credentials(HTTP_AUTHORIZATION=access_token)
    return api_client


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
