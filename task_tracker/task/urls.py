from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Uygulama adı
app_name = 'task'

# URL Yönlendirmeleri
urlpatterns = [
    path('', views.home, name='home'),  # Ana sayfa
    path('task_list/', views.task_list, name='task_list'),  # Tüm görevleri listele
    path('task/<int:pk>/', views.task_detail, name='task_detail'),  # Belirli bir görevin detayları
    path('new/', views.task_create, name='task_create'),  # Yeni görev oluştur
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),  # Belirli bir görevi sil
    path('category/list/', views.category_list, name='category_list'),  # Tüm kategorileri listele
    path('category/create/', views.category_create, name='category_create'),  # Yeni kategori oluştur
    path('category/<int:category_id>/', views.task_list_by_category, name='task_list_by_category'),  # Kategorilere göre görevleri listele
    path('project/create/', views.project_create, name='project_create'),  # Yeni proje oluştur
    path('project_list/', views.project_list, name='project_list'),  # Tüm projeleri listele
    path('project_list/', views.project_list, name='project_detail'),  # Tüm projeleri listele
    path('project/<int:pk>/', views.project_detail, name='project_detail'),  # Proje detayları
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),

    #path('project/<int:pk>/task_create/', views.task_create_for_project, name='task_create_for_project'),  # Proje için görev oluşturma

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Statik dosyalar için URL yönlendirmesi
