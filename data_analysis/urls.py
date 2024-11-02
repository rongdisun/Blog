from django.urls import path
from . import views

app_name = "data_analysis"

urlpatterns = [
    path("chart_view/", views.chart_view, name="chart_view"),
    path("most_comment_article/", views.most_comment_article, name="most_comment_article"),
    path("cate_articles_per/", views.cate_articles_per, name="cate_articles_per"),
    path("article_views_rank/", views.article_views_rank, name="article_views_rank"),
]
