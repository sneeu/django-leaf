from django.contrib import admin

#from forms import PostAdminForm
from models import Page


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'url', )

    fieldsets = (
        (None, {
            'fields': ('title', ('parent', 'slug', ), 'copy', )
        }),
        ('Advanced options', {
            'classes': ('collapse', ),
            'fields': ('description', 'keywords', 'head', )
        }),
    )


admin.site.register(Page, PageAdmin)
