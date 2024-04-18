from config.schema import schema
from django.contrib import admin
from django.urls import path
from strawberry.django.views import GraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema)),
]
