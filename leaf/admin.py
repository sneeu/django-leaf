from django.contrib import admin

import models


class ImageAdmin(admin.TabularInline):
    model = models.Image

    def _image_urls(self, obj):
        if models.has_sorl:
            return [value for value in obj.image.extra_thumbnails.values()]
        else:
            return [obj.image.url]

    def title_tag(self, obj):
        if obj.title is '':
            return u'<em>untitled image</em>'
        return obj.title
    title_tag.short_description = 'Title'
    title_tag.allow_tags = True

    def image_tag(self, obj):
        if models.has_sorl:
            return u'<img src="%s" />' % obj.image.thumbnail
        else:
            return u'<img src="%s" width="50" />' % obj.image.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def markdown(self, obj):
        r = ''
        for url in self._image_urls(obj):
            r += '<code>![%s](%s)</code><br/>' % (obj.title, url, )
        return r
    markdown.allow_tags = True


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'url', 'container_only', 'sort_order' )

    inlines = (ImageAdmin, )

    fieldsets = (
        (None, {
            'fields': ('title', ('parent', 'slug', ), 'container_only', 'copy', )
        }),
        ('Advanced options', {
            'classes': ('collapse', ),
            'fields': ('sort_order', 'description', 'keywords', 'head', )
        }),
    )


admin.site.register(models.Page, PageAdmin)
