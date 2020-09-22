from rest_framework import routers

from users.views import (
    RetrieveDeleteInventoryGenericViewSet,
    RetrieveCurrencyGenericViewSet,
    RetrieveTradeGenericViewSet,
    CreateOfferGenericViewSet,
    CreateUserGenericViewSet,
)

router = routers.SimpleRouter()
router.register('inventory', RetrieveDeleteInventoryGenericViewSet)
router.register('currency', RetrieveCurrencyGenericViewSet)
router.register('create_offer', CreateOfferGenericViewSet)
router.register('trade_history', RetrieveTradeGenericViewSet)
router.register('', CreateUserGenericViewSet)
urlpatterns = router.urls
