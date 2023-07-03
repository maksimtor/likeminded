from django.contrib import admin

# Register your models here.
class HomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_1', 'user_2')

# admin.site.register(HomeAdmin)