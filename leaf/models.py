from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    url = models.CharField(blank=True, max_length=120)
    copy = models.TextField()

    class Meta:
        ordering = ('url', )

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
