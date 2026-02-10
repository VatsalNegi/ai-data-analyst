from django.urls import path
from .views import DatasetUploadView, DatasetInsightsView, DatasetChartsView, DatasetChatView
from django.views.generic import TemplateView

urlpatterns = [
    path('upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('insights/<int:dataset_id>/', DatasetInsightsView.as_view(), name='dataset-insights'),
    path('charts/<int:dataset_id>/', DatasetChartsView.as_view(), name='dataset-charts'),
    path('chat/<int:dataset_id>/', DatasetChatView.as_view(), name='dataset-chat'),
    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
]
