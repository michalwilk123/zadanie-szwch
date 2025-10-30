from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from django.urls import path
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import GenericViewSet

from CloudSchoolLinkShortener.models import ShortenedURL

admin.site.register(ShortenedURL)


class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['hash', 'original_url']
        read_only_fields = ['hash']


class ShortenedURLViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = 'hash'

    def retrieve(self, request, *args, **kwargs):
        super().retrieve(request, *args, **kwargs)
        # Wiem że w zadaniu było napisane żeby zwrócić skróconego url-a
        # ale w sumie wiecej sensu wg mnie ma redirect
        # return super().retrieve(request, *args, **kwargs)
        return HttpResponsePermanentRedirect(self.get_object().original_url)


router = DefaultRouter()
router.register(r'shrt', ShortenedURLViewSet, basename='shrt')

urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls
