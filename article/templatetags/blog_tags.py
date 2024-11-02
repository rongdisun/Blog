from django import template
from article.models import Article, Category, Tag
from django.db.models.aggregates import Count
import pytz
from datetime import datetime

register = template.Library()


@register.simple_tag
def get_all_category():
    return Category.objects.annotate(num_articles=Count("article_category"))


@register.simple_tag
def get_all_tags():
    return Tag.objects.annotate(num_articles=Count("article_tag"))


@register.filter
def contains(value, arg):
    """Check if 'value' contains the 'arg' substring."""
    return arg in value
