from django.contrib import admin

# Register your models here.


from favorite.models import Favourite

admin.site.register(Favourite)