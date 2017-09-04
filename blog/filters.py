from .models import Article
import django_filters


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['title',]
