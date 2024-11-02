import json

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.db.models import Count
from pyecharts.charts import Funnel, Pie, Bar
import pyecharts.options as opts

from comment.models import Comment
from article.models import *


# Create your views here.

def chart_view(request):
    return render(request, "data_analysis/data_view.html")


# 分析评论最多的文章
def most_comment_article(request):
    comment_count = Article.objects.annotate(comment_count=Count("band_object")).order_by('-comment_count')[0:5]
    comment_count = [[article.title, article.comment_count] for article in comment_count]
    c = (
        Funnel()
        .add(
            series_name="",
            data_pair=comment_count,
            gap=2,
            label_opts=opts.LabelOpts(
                is_show=True,
                position="inside",
                formatter="{c}",
                font_size=18
            ),
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b} : {c}"),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_top="92%", orient="horizontal"),
            title_opts=opts.TitleOpts(
                title="文章评论数量排行榜",
                pos_left="center",  # 标题的位置
                pos_top="0px",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=32,  # 大小
                    font_weight="bold",  # 加粗与否
                    font_family="Arial",  # 字体：Arial、Times New Roman、FangSong、KaiTi
                    font_style="normal",  # 斜体、下划线、正常  italic
                ),
            )
        )
        .set_series_opts(

        )
        .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(c))


# 分析各个分类的文章数目
def cate_articles_per(request):
    cate_articles = Category.objects.annotate(cate_articles=Count("article_category")).order_by("-cate_articles")
    cate_articles = [[cate.name, cate.cate_articles] for cate in cate_articles]
    c = (
        Pie()
        .add(
            "",
            cate_articles,
            label_opts=opts.LabelOpts(
                is_show=True,
                # position="inside",
                formatter="{b}:{c}",
                font_size=18
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_top="92%", orient="horizontal"),
            title_opts=opts.TitleOpts(
                title="文章分类数量占比",
                pos_left="center",  # 标题的位置
                pos_top="0px",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=32,  # 大小
                    font_weight="bold",  # 加粗与否
                    font_family="Arial",  # 字体：Arial、Times New Roman、FangSong、KaiTi
                    font_style="normal",  # 斜体、下划线、正常  italic
                ),
            )
        )
        .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(c))


# 分析各个标签的文章数目
def article_views_rank(request):
    article_views = Article.objects.order_by("-article_views")[:5]
    article_title_list = [article.title for article in article_views]
    article_views_list = [article.article_views for article in article_views]
    c = (
        Bar()
        .add_xaxis(article_title_list)
        .add_yaxis("", article_views_list)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_inverse=True),
            legend_opts=opts.LegendOpts(is_show=True),
            title_opts=opts.TitleOpts(
                title="文章浏览量排行榜",
                pos_left="center",  # 标题的位置
                pos_top="0px",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=32,  # 大小
                    font_weight="bold",  # 加粗与否
                    font_family="Arial",  # 字体：Arial、Times New Roman、FangSong、KaiTi
                    font_style="normal",  # 斜体、下划线、正常  italic
                ),
            )
        )
        .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(c))
