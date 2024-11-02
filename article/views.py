from django.shortcuts import render
from django.views.generic import *
from .models import *


# Create your views here.

class PaginatorMixin:
    def get_page(self, paginator, page, page_offset=2):
        left_more_page = False
        right_more_page = False
        # 获取当前页码
        # 如果当前页面是7
        current_num = page.number
        if current_num <= page_offset + 2:
            left_range = range(1, current_num)
        else:
            left_more_page = True
            left_range = range(current_num - page_offset, current_num)
        if current_num >= paginator.num_pages - page_offset - 1:
            right_range = range(current_num + 1, paginator.num_pages + 1)
        else:
            right_more_page = True
            right_range = range(current_num + 1, current_num + page_offset + 1)
        return {
            'left_range': left_range,
            'right_range': right_range,
            'left_more_page': left_more_page,
            'right_more_page': right_more_page,
        }


class Index(ListView, PaginatorMixin):
    template_name = "index.html"
    model = Article
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        page = context.get('page_obj')
        paginator = context.get('paginator')
        context_data = self.get_page(paginator, page)
        context.update(context_data)
        return context


class ArticleDetail(DetailView):
    template_name = "article/article_detail.html"
    model = Article

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.increase_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        comments = self.object.band_object.all()
        tags = self.object.tags.all()
        context["tags"] = tags
        context["comments"] = comments
        return context


class SpecialCateArticle(ListView, PaginatorMixin):
    template_name = "article/cate_article.html"
    model = Article
    paginate_by = 1

    def get_queryset(self):
        pk = self.kwargs["pk"]
        cate = Category.objects.get(pk=pk)
        return cate.article_category.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecialCateArticle, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        cate = Category.objects.get(pk=pk)
        page = context.get('page_obj')
        paginator = context.get('paginator')
        context_data = self.get_page(paginator, page)
        context.update(context_data)
        context["cate"] = cate
        print(cate)
        return context


class SpecialTagArticle(ListView, PaginatorMixin):
    template_name = "article/tag_article.html"
    model = Article
    paginate_by = 2

    def get_queryset(self):
        pk = self.kwargs["pk"]
        tag = Tag.objects.get(pk=pk)
        return tag.article_tag.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecialTagArticle, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        tag = Tag.objects.get(pk=pk)
        context["tag"] = tag
        page = context.get('page_obj')
        paginator = context.get('paginator')
        context_data = self.get_page(paginator, page)
        context.update(context_data)
        return context
