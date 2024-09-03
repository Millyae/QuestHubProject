from django_filters import FilterSet, CharFilter, DateTimeFilter
from .models import Advertisement

class AdvertisementFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Название')
    content = CharFilter(field_name='content', lookup_expr='icontains', label='Содержание')
    author = CharFilter(field_name='author__username', lookup_expr='icontains', label='Автор')
    created_at = DateTimeFilter(field_name='created_at', lookup_expr='icontains', label='Дата создания')

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'author', 'created_at']