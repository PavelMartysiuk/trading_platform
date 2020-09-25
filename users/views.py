from users.serializers import (
    InventorySerializer,
    CurrencySerializer,
    OfferSerializer,
    TradeSerializer,
    UserSerializer,
)
from users.models import User, Inventory, Currency, Trade, Offer

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import viewsets

from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404


def validate_sell_offer(offer):
    user_id = offer['user']
    entry_quantity_sell_item = offer['entry_quantity']
    try:
        sell_item = Inventory.objects.get(user=user_id)
    except Inventory.DoesNotExist:
        raise Http404("You don't have this item")

    quantity_sell_item = sell_item.quantity
    if entry_quantity_sell_item > quantity_sell_item:
        return False
    return True


class CreateUserGenericViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        """Func creates new user in db"""
        self.get_permission(self.create.__name__)
        return super().create(request)

    def get_permission(self, func_name):
        """Func return permission for funcs"""
        if func_name == 'create':
            CreateUserGenericViewSet.permission_classes = (AllowAny,)
        else:
            CreateUserGenericViewSet.permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        """Func retrieves user by pk"""
        self.get_permission(self.retrieve.__name__)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Func updates user data by pk"""
        self.get_permission(self.update.__name__)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """"Func deletes user by pk"""
        self.get_permission(self.destroy.__name__)
        return self.destroy(request, *args, **kwargs)


class RetrieveDeleteInventoryGenericViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin, ):
    permission_classes = (IsAuthenticated,)
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def list(self, request, *args, **kwargs):
        """Func retrieves user inventory by user id"""
        user_id = request.user.id
        self.queryset = get_list_or_404(Inventory, user=user_id)
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Func deletes user inventory"""
        inventory_pk = kwargs['pk']
        user_id = request.user.id
        # delete obj  only from current user inventory.
        # if user doesn't have inventory obj by pk func returns 404 error
        get_object_or_404(Inventory, id=inventory_pk, user=user_id)
        return super().destroy(request, *args, **kwargs)


class RetrieveCurrencyGenericViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    """Class retrieves currensies and one currency by pk"""
    permission_classes = (AllowAny,)
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CreateOfferGenericViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()

    def create(self, request):
        """Func creates new offer"""
        user_id = request.user.id
        offer = request.data
        offer['user'] = user_id
        entry_quantity = offer['entry_quantity']
        offer['quantity'] = entry_quantity
        offer_type = offer['order_type']
        if offer_type == 'sell':
            active_offer = validate_sell_offer(offer)
            if active_offer:
                return super().create(request)
            return Response({'response': 'bad input data'})
        elif offer_type == 'buy':
            return super().create(request)


class RetrieveTradeGenericViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin, ):
    """Class retrieves all trade history and one trade by pk"""
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = (AllowAny,)
