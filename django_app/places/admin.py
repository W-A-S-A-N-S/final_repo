from django.contrib import admin
from .models import Place, PlaceReview, PlaceBookmark

admin.site.register(Place)
admin.site.register(PlaceReview)
admin.site.register(PlaceBookmark)