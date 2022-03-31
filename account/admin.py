from django.contrib import admin
from django.contrib.auth.models import Group
from .models import BotUser

admin.site.unregister(Group)


@admin.register(BotUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("tg_id", "full_name", "phone", "is_active", "lang",)
    list_display_links = list_display
    readonly_fields = (
        'tg_id',
        'full_name',
        'phone',
        # 'lang'
    )

    def has_add_permission(self, request):
        return False
