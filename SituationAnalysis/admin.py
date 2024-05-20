from django.contrib import admin
from .models import Suggestion


@admin.register(Suggestion)    ## 监听表单
class SuggestionModeAdmin(admin.ModelAdmin):
    list_display = ('month', "suggestion")
    search_fields = ('month',)
    list_filter = ('month', )
