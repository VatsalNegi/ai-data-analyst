from django.urls import path
from .views import (
    dashboard,
    DatasetUploadView,
    DatasetInsightsView,
    DatasetChartsView,
    DatasetChatView
)

urlpatterns = [

    # Dashboard homepage
    path('', dashboard, name='home'),

    # API routes
    path('upload/', DatasetUploadView.as_view()),
    path('insights/<int:dataset_id>/', DatasetInsightsView.as_view()),
    path('charts/<int:dataset_id>/', DatasetChartsView.as_view()),
    path('chat/<int:dataset_id>/', DatasetChatView.as_view()),
]
