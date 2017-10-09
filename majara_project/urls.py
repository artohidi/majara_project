from django.conf.urls import url
from django.contrib import admin
from majara_app import views
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^admin/', admin.site.urls),  # for django admin.
                  url(r'^genreList/', views.GenreViewSet.as_view(), name='genre_list'),  # for telegram bot, good done.
                  url(r'^dialogListByGenreId/', views.DialogListByGenreIdViewSet.as_view({'post': 'list'}),
                      name='dialog_list_by_genre_id'),  # good done.
                  url(r'^getDialogById/(?P<DialogId>.+)', views.GetDialogByIdViewSet.as_view(),
                      name='get_dialog_by_id'),  # good done.
                  url(r'^dialogList/', views.DialogList.as_view(), name='dialog_list'),  # good done.
                  url(r'^saveDialogText/', views.SaveDialogText, name='save_dialog_text'),  # for api, good done.
                  url(r'^saveDialog/', views.SaveDialog, name='save_dialog'),
                  url(r'^updateDialogText/', views.UpdateDialogText, name='update_dialog_text')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
