from django.urls import path
from . import views
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
path("", views.index, name="index"),
path("test", views.test, name="test"),
path("pred", views.pred, name="pred"),
path("tags", views.tags, name="tags"),
path("v1/", views.v1, name="view 1"),
path("pyfun",views.pyfun),
path("predict",views.predict)
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)