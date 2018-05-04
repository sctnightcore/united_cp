from unitedcp.ragnarok.models import (Vendings, VendingItems)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class VendingsList(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        vendors_list = VendingItems.objects.values('vending_id', 'cartinventory_id__nameid__name_japanese', 'price', 'amount', 'cartinventory_id__card0__name_japanese',
                                                   'cartinventory_id__card1__name_japanese', 'cartinventory_id__card2__name_japanese', 'cartinventory_id__card3__name_japanese',
                                                   'cartinventory_id__nameid', 'vending_id__title', 'vending_id__map', 'vending_id__char_id__name', 'cartinventory_id__refine', 'cartinventory_id__nameid__slots').all()

        last_vendors = None

        return Response(
            {
                'vendorsList': vendors_list,
                'randVendors': last_vendors
            },
            status=200,
            content_type='application/json'
        )
