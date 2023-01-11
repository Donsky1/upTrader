from django.db import models


class NameModelMixin(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class GlobalMenu(NameModelMixin):
    pass


class TreeMenu(NameModelMixin):
    global_parent = models.ForeignKey(GlobalMenu, on_delete=models.CASCADE, related_name='menu_items')
    parent = models.ForeignKey('self', max_length=50, blank=True, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        if self.parent:
            return '/category/%s/%s/%s' % (self.global_parent, self.parent, self.name)
        else:
            return '/category/%s/%s' % (self.global_parent, self.name)

    def get_parent_id(self):
        if self.parent:
            return self.parent.id
