from django.contrib import admin

from . import models


class CampaignAdmin(admin.ModelAdmin):
    date_hierarchy = 'due_date'
    list_display = (
        'id',
        'title',
        'description',
        'link',
        'due_date',
        'replies_num',
    )
    list_filter = (
        'due_date',
        'replies_num',
    )
    search_fields = (
        'id',
        'title',
        'due_date',
        'replies_num',
    )


admin.site.register(models.Campaign, CampaignAdmin)
