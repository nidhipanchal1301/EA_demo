from rest_framework import serializers

from ..models import SurveyForm, SurveyQuestion, SurveyOption, SurveyPermission



class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyPermission
        fields = ("id", "key", "label",)


class SurveyOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ("id", "text",)


class SurveyQuestionListSerializer(serializers.ModelSerializer):
    options = SurveyOptionListSerializer(many=True, source="options_question")

    class Meta:
        model = SurveyQuestion
        fields = ("id", "label", "placeholder", "type", "mandatory", "default_hide", "use_for_analytics", "options",)


class SurveyFormListSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    questions = SurveyQuestionListSerializer(many=True, source="questions_form")

    class Meta:
        model = SurveyForm
        fields = ("id", "name", "status", "created_at", "permissions", "questions", )


class SurveyFormCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.CharField(default="active")
    permissions = serializers.ListField(child=serializers.CharField(), required=False)
    questions = serializers.ListField(required=False)


class SurveyFormUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    permissions = serializers.ListField(child=serializers.IntegerField(), required=False)
    questions = serializers.ListField(required=False)