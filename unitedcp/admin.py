from django.contrib import admin
from unitedcp.models import PanelLogs
from unitedcp.guides.models import (UserGuide, UserGuideTag, UserGuideReward)
from unitedcp.shop.models import *
from unitedcp.staff.news.models import CPNews


admin.site.register(CPNews)
admin.site.register(PanelLogs)
admin.site.register(UserGuide)
admin.site.register(UserGuideTag)
admin.site.register(UserGuideReward)
admin.site.register(Shop)
admin.site.register(ShopCategories)
