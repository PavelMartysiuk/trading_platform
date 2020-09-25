from users.models import User, WatchList, Item, Inventory, Currency, Offer, Trade

from rest_framework import serializers

from django.contrib.auth.hashers import make_password


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ('id', 'user')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'item', 'quantity')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    watch_list = WatchListSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'password',
            'username',
            'balance',
            'watch_list'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        watch_list = validated_data.get('watch_list', None)
        password_in_sha1 = make_password(validated_data['password'])
        validated_data['password'] = password_in_sha1
        if watch_list:
            validated_data.pop('watch_list')
            user = User.objects.create(**validated_data)
            WatchList.objects.create(user=user, **watch_list)
            return user
        user = User.objects.create(**validated_data)
        return user


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
