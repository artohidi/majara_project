from rest_framework import serializers

from .models import Genre, Dialog, DialogText


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DialogListByGenreIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = '__all__'


class GetDialogByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = '__all__'

    Dialog_Text = serializers.SerializerMethodField()

    def get_Dialog_Text(self, obj):
        return obj.dialogtext_set.values_list('id', 'textFrom', 'type', 'text', 'photo')
