from django.urls import path
from . import views

urlpatterns = [
    path("", views.soldat_list, name="soldat_list"),
    path("soldat/<str:id_character>/", views.soldat_detail, name="soldat_detail"),
    path(
        "soldat/<str:id_character>/<str:message>/",
        views.soldat_detail,
        name="soldat_detail_message",
    ),
]
