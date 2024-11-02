import uuid
from pathlib import Path

from django.conf import settings
from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from tinymce import models as tinymce_models


# Create your models here.

class Category(models.Model):
    name = models.CharField(verbose_name="分类名", max_length=255, unique=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("article:special_cate_article", args=[self.pk])


class Tag(models.Model):
    name = models.CharField(verbose_name="标签名", max_length=255, unique=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article:special_tag_article', args=[self.pk])


def article_cover_path(instance, cover_name):
    ext = cover_name.split('.')[-1]
    cover_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return Path("article", cover_name)


class Article(models.Model):
    STATUS_CHOICES = (
        (1, "发表"),
        (0, "草稿"),
    )
    title = models.CharField(verbose_name="标题", max_length=255)
    cover = models.FileField(verbose_name="封面", upload_to=article_cover_path, max_length=255)
    content = tinymce_models.HTMLField(verbose_name="内容")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="作者",
        on_delete=models.CASCADE,
        related_name="article_author"
    )
    post_time = models.DateTimeField("发布时间", auto_now_add=True)
    last_mod_time = models.DateTimeField("修改时间", auto_now=True)
    article_views = models.PositiveIntegerField(verbose_name="浏览量", default=0)
    # 数字越大越靠前
    article_order = models.IntegerField(verbose_name='排序', default=0)
    status = models.SmallIntegerField(verbose_name="发布状态", default=1)

    cover_thumbnail = ImageSpecField(
        source='cover',
        processors=[ResizeToFill(960, 740)],
        format='JPEG',
        options={'quality': 95}
    )
    category = models.ForeignKey(
        verbose_name="分类",
        to=Category,
        on_delete=models.CASCADE,
        related_name="article_category"
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name="标签集合",
        blank=True,
        null=True,
        related_name="article_tag"
    )

    class Meta:
        ordering = ['-article_order', '-post_time']
        verbose_name = "文章列表"
        verbose_name_plural = "文章列表"

    def body_to_string(self):
        return self.content

    def increase_views(self):
        self.article_views += 1
        self.save(update_fields=["article_views"])

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.pk])

    def __str__(self):
        return self.title
