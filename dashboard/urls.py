from django.urls import path
from .import views 
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('get_datos/', login_required(views.get_datos), name='get_datos'),
    path('categorias/', login_required(views.categorias), name='categorias'),
    path('sub_categorias/', login_required(views.subcategorias), name='subcategorias'),
    path('estado/', login_required(views.estado), name='estado'),
    path('ciudad/', login_required(views.ciudad), name='ciudad'),
    path('ventas/', login_required(views.listar_ventas), name='ventas'),
    path('ventas/crear/', login_required(views.create), name='create'),
    path('ventas/edit}', login_required(views.edit), name='edit'),
    path('delete/<int:id>/', login_required(views.delete), name='delete'),
    path('ventas/edit/<int:id>/', login_required(views.edit), name='edit'),
]

