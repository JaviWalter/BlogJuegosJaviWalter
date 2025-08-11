
from django.urls import path
from .views import ArticuloCreateView, ArticuloListView, ArticuloUpdateView, ArticuloDetailView, ArticuloDeleteView , ComentarioCreateView, ComentarioUpdateView, ComentarioDeleteView, aprobar_comentario

app_name = 'apps.blog'

urlpatterns = [
    path('', ArticuloListView.as_view(), name='lista_articulos'), # URL para mostrar todos los articulos
    path('<int:pk>/', ArticuloDetailView.as_view(), name='detalle_articulo'),  # URL para mostrar el detalle de un artículo específico, Por ejemplo: /blog/5/
    path('crear/', ArticuloCreateView.as_view(), name='crear_articulo'),
    path('<int:pk>/editar/', ArticuloUpdateView.as_view(), name='editar_articulo'),
    path('<int:pk>/eliminar/', ArticuloDeleteView.as_view(), name='eliminar_articulo'),

    #=====comentarios
    path('<int:articulo_id>/comentar', ComentarioCreateView.as_view(), name='agregar_comentario'),
    path('comentario/<int:pk>/editar', ComentarioUpdateView.as_view(), name='editar_comentario'),
    path('comentario/<int:pk>/eliminar', ComentarioDeleteView.as_view(), name='eliminar_comentario'),
    path('comentario/<int:pk>/aprobar', aprobar_comentario, name='aprobar_comentario'),
]