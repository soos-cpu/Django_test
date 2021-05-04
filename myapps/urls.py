from django.urls import path

from . import views

app_name = 'myapps'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('homepage', views.homepage, name='homepage'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
    # path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('note', views.note, name='note'),
    path('odoo', views.odoo, name='note/odoo'),
    path('ggl_house', views.ggl_house, name='ggl_house'),
    path('update_ggl_house_info', views.update_ggl_house_info, name='update_ggl_house_info'),
    path('ggl_house_search', views.ggl_house_search, name='ggl_house_search'),
]
