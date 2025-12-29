from django.contrib import admin
from .models import Shortform, ShortformComment, TranslationEntry

admin.site.register(Shortform)
admin.site.register(ShortformComment)
admin.site.register(TranslationEntry)