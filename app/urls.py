from django.urls import path
from . import views
from django.conf import settings

app_name = 'app'



urlpatterns = [
    path('', views.home, name='home'),
    path('admin-site/dashboard/', views.dashboard, name='dashboard'),
    path('view/thesis/', views.view_thesis, name='view_thesis'),
    path('view/memories/', views.view_memories, name='view_memories'),
    path('view/details/<str:document_type>/<int:document_id>/', views.document_details, name='document_details'),
    path('add/comment/<str:document_type>/<int:document_id>/', views.add_comment, name='add_comment'),
    path('delete/comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('add/thesis/', views.add_thesis, name='add_thesis'),
    path('add/memory/', views.add_memory, name='add_memory'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    

]




