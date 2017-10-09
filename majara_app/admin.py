from django.contrib import admin
from .models import Profile, Genre, Dialog, DialogText


class GenreAdmin(admin.ModelAdmin):
    readonly_fields = ['pictureMain', 'createdTime', 'changedTime', ]

    def pictureShow(self, obj):

        if obj.genre_cover == "":
            return "No Image"
        else:
            return "<img src='%s' height=50px>" % obj.genre_cover.url

    def pictureMain(self, obj):
        if obj.genre_cover == "":
            return "No Image"
        return "<img src='%s' height=200px>" % obj.genre_cover.url

    list_display = ("id", "title", "createdTime", "changedTime", "pictureShow",)
    list_display_links = list_display
    ordering = ('id', 'title', 'createdTime', 'changedTime',)

    pictureMain.allow_tags = True
    pictureShow.allow_tags = True


class DialogTextAdmin(admin.ModelAdmin):
    readonly_fields = ['pictureMain', 'createdTime', 'changedTime', ]

    def pictureShow(self, obj):
        if obj.photo == "":
            return "No Image"
        else:
            return "<img src='%s' height=50px>" % obj.photo.url

    def pictureMain(self, obj):
        if obj.photo == "":
            return "No Image"
        return "<img src='%s' height=200px>" % obj.photo.url

    def shortDescription(self, obj):
        if obj.text == "":
            return "No Text"
        else:
            return obj.text[0:50]

    pictureMain.allow_tags = True
    pictureShow.allow_tags = True
    shortDescription.allow_tags = True

    list_display = (
    "id", "dialogId", "textFrom", "type", "shortDescription", "createdTime", "changedTime", "pictureShow",)
    list_display_links = list_display
    ordering = ('id', 'type', 'createdTime', 'changedTime',)


class DialogAdmin(admin.ModelAdmin):
    readonly_fields = ['pictureMain', 'createdTime', 'changedTime', ]

    def pictureShow(self, obj):
        if obj.cover == "":
            return "No Image"
        else:
            return "<img src='%s' height=50px>" % obj.cover.url

    def pictureMain(self, obj):
        if obj.cover == "":
            return "No Image"
        return "<img src='%s' height=200px>" % obj.cover.url

    pictureMain.allow_tags = True
    pictureShow.allow_tags = True

    list_display = ("id", "genreId", "title", "createdTime", "changedTime", "pictureShow",)
    list_display_links = list_display
    ordering = ('id', 'title', 'createdTime', 'changedTime',)


admin.site.register(Profile)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Dialog, DialogAdmin)
admin.site.register(DialogText, DialogTextAdmin)
