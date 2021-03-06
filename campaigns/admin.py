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


class ProfileUserAdmin(admin.ModelAdmin):
    list_display = (
        'profile_user_id',
        'is_campaigner',
        'is_writer',
    )


class CampaignUserAdmin(admin.ModelAdmin):
    list_display = (
        'campaign_user_id',
    )


class WriterUserAdmin(admin.ModelAdmin):
    list_display = (
        'writer_user_id',
    )


class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        'writer',
        'campaign',
        'reply_text',
    )


admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.ProfileUser, ProfileUserAdmin)
admin.site.register(models.CampaignUser, CampaignUserAdmin)
admin.site.register(models.WriterUser, WriterUserAdmin)
admin.site.register(models.Reply, ReplyAdmin)
