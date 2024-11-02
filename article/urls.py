from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('article_detail/<pk>', views.ArticleDetail.as_view(), name="article_detail"),

    path('special_cate_article/<pk>', views.SpecialCateArticle.as_view(), name="special_cate_article"),
    path('special_tag_article/<pk>', views.SpecialTagArticle.as_view(), name="special_tag_article")

]