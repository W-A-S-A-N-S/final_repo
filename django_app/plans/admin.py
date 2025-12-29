from django.contrib import admin
from .models import TravelPlan, PlanDetail, TravelPost, Comment

admin.site.register(TravelPlan)
admin.site.register(PlanDetail)
admin.site.register(TravelPost)
admin.site.register(Comment)