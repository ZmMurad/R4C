from django.urls import path
from robots.views import create_robot_or_gets, get_robot,download_excel_report


urlpatterns = [
    path('',create_robot_or_gets,name='robots'),
    path('<int:pk>/', get_robot,name='get_robot'),
    path('report/',download_excel_report,name='report')
]
