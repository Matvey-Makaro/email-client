from django.contrib import admin

from game_store.models import *
from django.utils.html import format_html


class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'cat']
    search_fields = ['name']
    list_filter = ['name']

    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.photo.url))

    image_tag.short_description = 'Product Image Preview'
    readonly_fields = ['image_tag']


admin.site.site_header = "vKiiNGz Game Shop Dashboard"
admin.site.site_title = "vKiiNGz Game Shop"
admin.site.index_title = "Welcome to vKiiNGz Game Shop Dashboard"

admin.site.register(Game, GameAdmin)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
