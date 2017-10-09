from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from future.utils import python_2_unicode_compatible


def genreDirectory(instance, filename):
    filename = "genre_%s" % (filename,)
    return "genre/{0}".format(filename, )


def dialogDirectory(instance, filename):
    filename = "dialog_%s" % (filename,)
    return "dialog/{0}".format(filename, )


def textDirectory(instance, filename):
    filename = "dialogTxt_%s" % (filename,)
    return "dialogTxt/{0}".format(filename, )


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    father_name = models.CharField(max_length=20, blank=True)
    national_id = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    verification_code = models.CharField(max_length=10, default="Null")
    activation_flag = models.IntegerField(default=0)
    sign_in_flag = models.IntegerField(default=0)

    def __str__(self):
        return "{0}-{1}-{2}-{3}".format(self.id, self.first_name, self.last_name, self.national_id)


@python_2_unicode_compatible
class Genre(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True, verbose_name="Title")
    genre_cover = models.ImageField(upload_to=genreDirectory, blank=True, verbose_name="Picture")
    createdTime = models.DateTimeField(auto_now_add=True)
    changedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}-{1}".format(self.id, self.title)


@python_2_unicode_compatible
class Dialog(models.Model):
    genreId = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Genre")
    title = models.CharField(max_length=200, verbose_name="Title")
    cover = models.ImageField(upload_to=dialogDirectory, blank=True, verbose_name="Picture")
    createdTime = models.DateTimeField(auto_now_add=True)
    changedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}-{1}".format(self.id, self.title)


@python_2_unicode_compatible
class DialogText(models.Model):
    dialogId = models.ForeignKey(Dialog, on_delete=models.CASCADE, verbose_name="Dialog")
    textFrom = models.CharField(max_length=255, blank=True, verbose_name="From")
    type = models.CharField(max_length=10, choices=(('Text', 'Text'), ('Image', 'Image')), blank=False,
                            verbose_name="Type")
    text = models.TextField(blank=True, verbose_name="Dialog Text")
    photo = models.ImageField(upload_to=textDirectory, blank=True, verbose_name="Picture")
    createdTime = models.DateTimeField(auto_now_add=True)
    changedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}){1}-{2}-{3}".format(self.id, self.textFrom, self.type, self.text)
