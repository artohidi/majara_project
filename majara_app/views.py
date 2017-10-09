from __future__ import unicode_literals
import json
import random
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings
from .models import Profile, Genre, Dialog, DialogText
from .serializer import GenreSerializer, DialogListByGenreIdSerializer, GetDialogByIdSerializer
from rest_framework.permissions import AllowAny

from django.http import JsonResponse


class GenreViewSet(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GenreSerializer

    def get_queryset(self):
        queryset = Genre.objects.all()
        return queryset


class DialogList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GenreSerializer

    def get_queryset(self):
        queryset = Dialog.objects.all()
        return queryset


class DialogListByGenreIdViewSet(RetrieveModelMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = DialogListByGenreIdSerializer

    def get_queryset(self):
        queryset = Dialog.objects.all()
        data = json.loads(self.request.body)
        genre_id = data.get('genre_id', '')
        if genre_id is not None:
            queryset = queryset.filter(genreId=genre_id)
        return queryset


class GetDialogByIdViewSet(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetDialogByIdSerializer

    def get_queryset(self):
        queryset = Dialog.objects.all()
        dialog_id = self.kwargs['DialogId']
        if dialog_id is not None:
            queryset = queryset.filter(id=dialog_id)
        return queryset


@csrf_exempt
def SaveDialog(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        genre_id = data.get('genre_id', '')
        if not Genre.objects.filter(id=genre_id).first() is None:
            title_get = data.get('title', '')
            obj = Dialog.objects.create(genreId=Genre.objects.get(id=genre_id))
            obj.title = title_get
            obj.save()
            return JsonResponse({"result": "Dialog created successfully", "Dialog ID": obj.id, "Genre ID": genre_id,
                                 "Title ": obj.title})
        return JsonResponse({"result": " Genre ID is'nt Exist."})


@csrf_exempt
def UpdateDialogText(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dialog_id = data.get('dialog_id', '')
        obj = DialogText.objects.filter(id=dialog_id).first()
        if obj is None:
            return JsonResponse({"result": "Dialog ID is'nt Exist."})
        text = data.get('text', '')
        obj.textFrom, obj.text = text.split(":")
        obj.save()
        return JsonResponse(
            {"result": "Dialog Text Changed Successfully", "Dialog Text ID": obj.id, "Dialog ID": dialog_id,
             "Text ": obj.text})


@csrf_exempt
def SaveDialogText(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        dialog_id = params.get("dialog_id", "")
        print("armin")
        if not Dialog.objects.filter(id=dialog_id).first() is None:
            type_get = params.get("type", "")
            text = params.get("text", "")
            from_get, text_get = text.split(":")
            obj = DialogText.objects.create(dialogId=Dialog.objects.get(id=dialog_id))
            obj.type = type_get
            obj.textFrom = from_get
            obj.text = text_get
            obj.save()
            return JsonResponse(
                {"result": "successfully created", "Dialog Text ID": obj.id, "Dialog ID": dialog_id, "From": from_get,
                 "Text": text_get})
        return JsonResponse({"result": "Dialog Id is'nt Exist"})


@csrf_exempt
def verification_code_set():
    numbers = random.sample(range(1, 10), 4)
    number = "".join(map(str, numbers))
    return number


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username_get = data.get("username", "Null")
        first_name_get = data.get("first_name", "Null")
        last_name_get = data.get("last_name", "Null")
        verification_code_get = data.get("verification_code", "Null")
        u = User.objects.filter(username=username_get).first()
        p = Profile.objects.filter(user=u).first()
        if u is None:
            u = User.objects.create(username=username_get)
            u.save()
            p = Profile.objects.create(user=u)
            p.first_name = first_name_get
            p.last_name = last_name_get
            p.verification_code = verification_code_set()
            p.save()
            return JsonResponse({"status 1": "user created carefully.", "verification code": p.verification_code})
        else:
            if p.verification_code == "Null":
                p.verification_code = verification_code_set()
                p.save()
                return JsonResponse({"status 2_verification code is": p.verification_code})
            elif p.verification_code == verification_code_get:
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(u)
                token = jwt_encode_handler(payload)
                p.token = token
                p.activation_flag = 1
                p.sign_in_flag = 1
                p.save()
                return JsonResponse({"status 3": "account registered carefully.", "token is": p.token})
            else:
                return JsonResponse({"status 4": "verification code is wrong."})
    else:
        return JsonResponse({"status 5": "error occurred."})


@csrf_exempt
def profileUpdate(request):
    auth = request.META['HTTP_AUTHORIZATION'].split()[1]
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name_get = data.get("first_name", "")
        last_name_get = data.get("last_name", "")
        father_name_get = data.get("father_name", "")
        national_id_get = data.get("national_id", "")
        address_get = data.get("address", "")
        postal_code_get = data.get("postal_code", "")
        p = Profile.objects.filter(token=auth).first()
        p.first_name = first_name_get
        p.last_name = last_name_get
        p.father_name = father_name_get
        p.national_id = national_id_get
        p.address = address_get
        p.postal_code = postal_code_get
        p.save()
        return JsonResponse({"status 1": "profile updated carefully."})
    return JsonResponse({"status 2": "error occurred."})


@csrf_exempt
def signOut(request):
    auth = request.META['HTTP_AUTHORIZATION'].split()[1]
    if request.method == 'POST':
        p = Profile.objects.filter(token=auth).first()
        p.sign_in_flag = 0
        p.token = "Null"
        p.verification_code = "Null"
        p.save()
        return JsonResponse({"status 1": "user sign out carefully."})
    return JsonResponse({"status 2": "error occurred."})


@csrf_exempt
def showProfile(request):
    if request.method == 'GET':
        auth = request.META['HTTP_AUTHORIZATION'].split()[1]
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        user = jwt_decode_handler(auth)
        username = user['username']
        u = User.objects.filter(username=username).first()
        p = Profile.objects.filter(user=u).first()
        print(p.user, p.first_name, p.last_name, p.father_name, p.national_id, p.address, p.postal_code)
        input()
        return JsonResponse(
            {"status 1": "profile data", "username": p.user, "first name": p.first_name, "last name": p.last_name,
             "father name": p.father_name, "national id": p.national_id, "address": p.address,
             "postal code": p.postal_code})
    else:
        return JsonResponse({"status 2": "error occurred"})
