from django.conf import settings
from django.db import models


has_sorl = 'sorl.thumbnail' in settings.INSTALLED_APPS

if has_sorl:
    from sorl.thumbnail.fields import ImageWithThumbnailsField


class Page(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True,
        related_name='children')
    url = models.CharField(blank=True, max_length=120)
    copy = models.TextField(blank=True, null=True)
    head = models.TextField(blank=True, null=True)
    container_only = models.BooleanField(default=False,
        help_text=u"""If set, this page will not be displayed, and will
        redirect to it's first child.""")
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ('parent__sort_order', 'sort_order', )

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.parent:
            self.url = '%s%s/' % (self.parent.url, self.slug, )
        else:
            if self.slug:
                self.url = '/%s/' % (self.slug, )
            else:
                self.url = '/'

        super(Page, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.url
        
    def is_child_of(self, page):
        if self == page or self.parent == page:
            return True
        if self.parent != None:
            return self.parent.is_child_of(page)
        return False


class Image(models.Model):
    UPLOAD_TO = 'pages/'

    title = models.CharField(blank=True, max_length=120, null=True)
    page = models.ForeignKey(Page, blank=True, null=True,
        related_name='related_images')

    if has_sorl:
        image = ImageWithThumbnailsField(
            upload_to=UPLOAD_TO,
            thumbnail={'size': (50, 50)},
            extra_thumbnails=settings.LEAF_IMAGE_SIZES)
    else:
        image = models.ImageField(upload_to=UPLOAD_TO)

    class Meta:
        ordering = ('title', )

    def __unicode__(self):
        return self.title
