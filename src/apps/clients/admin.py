from django.contrib import admin

from .forms import ClientGroupForm
from .models import ClientGroup, ClientUser

admin.site.register(ClientUser)


@admin.register(ClientGroup)
class ClientGroupAdmin(admin.ModelAdmin):
    form = ClientGroupForm
