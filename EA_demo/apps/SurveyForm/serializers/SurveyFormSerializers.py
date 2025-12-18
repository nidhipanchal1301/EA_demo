from rest_framework import serializers

from ..models import SurveyForm, SurveyQuestion, SurveyOption, SurveyPermission



class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyPermission
        fields = ("id", "key", "label",)

class SurveyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ("text",)



class SurveyOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ("id", "text",)


class SurveyQuestionListSerializer(serializers.ModelSerializer):
    options = SurveyOptionListSerializer(many=True, source="SurveyOption_question")

    class Meta:
        model = SurveyQuestion
        fields = ("id", "label", "placeholder", "type", "mandatory", "default_hide", "use_for_analytics", "options",)


class SurveyFormListSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    questions = SurveyQuestionListSerializer(many=True, source="SurveyQuestion_form")

    class Meta:
        model = SurveyForm
        fields = ("id", "name", "status", "created_at", "permissions", "questions", "total_questions", )



class SurveyFormCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
    permissions = serializers.ListField(child=serializers.IntegerField(), required=True, allow_empty=False)
    questions = serializers.ListField(child=serializers.DictField(), required=True, allow_empty=False )

    
    def validate_permissions(self, value):
        if not all(SurveyPermission.objects.filter(id=perm_id).exists() for perm_id in value):
            raise serializers.ValidationError("Some permissions are invalid")
        return value

    def validate_questions(self, value):
        for q in value:
            required_fields = ["label", "type", "options"]
            for field in required_fields:
                if field not in q:
                    raise serializers.ValidationError(f"Each question must have '{field}'")
            if not isinstance(q["options"], list) or len(q["options"]) == 0:
                raise serializers.ValidationError("Each question must have at least one option")
        return value


class SurveyFormUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    permissions = serializers.ListField(child=serializers.IntegerField(), required=False)
    questions = serializers.ListField(required=False)