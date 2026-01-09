from rest_framework import serializers

from ..models import SurveyForm, SurveyQuestion, SurveyOption, SurveyPermission



class SurveyPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyPermission
        fields = ("id", "key",)
        

class SurveyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ("text",)


class SurveyQuestionSerializer(serializers.ModelSerializer):
    options = SurveyOptionSerializer(many=True, source="SurveyOption_question")

    class Meta:
        model = SurveyQuestion
        fields = (  "label", "type", "options",)


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
    permissions = serializers.SlugRelatedField(many=True, read_only=True, slug_field="key")  
    questions = SurveyQuestionSerializer(many=True, source="SurveyQuestion_form")
    total_questions = serializers.IntegerField(source="SurveyQuestion_form.count", read_only=True)

    class Meta:
        model = SurveyForm
        fields = ("id", "name", "permissions", "status", "total_questions", "questions",)


class SurveyOptionCreateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)


class SurveyQuestionCreateSerializer(serializers.Serializer):
    label = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    placeholder = serializers.CharField(required=False, allow_blank=True)
    mandatory = serializers.BooleanField(required=False, default=False)
    default_hide = serializers.BooleanField(required=False, default=False)
    use_for_analytics = serializers.BooleanField(required=False, default=False)

    options = SurveyOptionCreateSerializer(many=True, required=False)

    def validate(self, data):
        q_type = data.get("type")
        options = data.get("options", [])

        if q_type in ["single_choice", "multiple_choice"]:
            if not options:
                raise serializers.ValidationError({'options': "Options required for choice questions"})

        if q_type == "single_choice" and len(options) != 1:
            raise serializers.ValidationError({'single_choice': "Must have exactly 1 option"})

        if q_type == "multiple_choice" and len(options) < 2:
            raise serializers.ValidationError({'multiple_choice': "Must have at least 2 options"})

        return data


class SurveyFormCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[("active", "Active"), ("inactive", "Inactive")],default="active")
    permissions = serializers.ListField(child=serializers.IntegerField(),required=True,allow_empty=False)
    questions = SurveyQuestionCreateSerializer(many=True)

    def validate(self, attrs):
        permissions = attrs.get("permissions")
        if SurveyPermission.objects.filter(id__in=permissions).count() != len(permissions):
            raise serializers.ValidationError({'permissions': "Some permissions are invalid"})

        questions = attrs.get("questions")

        if not questions:
            raise serializers.ValidationError({'questions': "Questions cannot be empty"})

        if not any(q.get("mandatory", False) for q in questions):
            raise serializers.ValidationError({'mandatory': "At least one question must be mandatory=True"})

        return attrs


class SurveyFormResponseSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(many=True, read_only=True, slug_field="key")
    questions = SurveyQuestionSerializer(many=True, source="SurveyQuestion_form")
    total_questions = serializers.IntegerField(source="SurveyQuestion_form.count", read_only=True)

    class Meta:
        model = SurveyForm
        fields = ("id", "name", "permissions", "status", "total_questions", "questions",)

    def get_permissions(self, obj):
        return [p.key for p in obj.permissions.all()]

    def get_total_questions(self, obj):
        return obj.SurveyQuestion_form.count()

    def get_questions(self, obj):
        return [
            {
                "question": q.label,
                "type": q.type,
                "values": [opt.text for opt in q.SurveyOption_question.all()]
            }
            for q in obj.SurveyQuestion_form.all()
        ]


class SurveyFormUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=[("active", "Active"), ("inactive", "Inactive")],  required=False)
    permissions = serializers.ListField(child=serializers.IntegerField(), required=False)
    questions = serializers.ListField(child=serializers.DictField(), required=False)

    def validate(self, attrs):
        if "permissions" in attrs:
            permissions = attrs["permissions"]
            if SurveyPermission.objects.filter(id__in=permissions).count() != len(permissions):
                raise serializers.ValidationError({'permissions': "Some permissions are invalid"})

        if "questions" in attrs:
            questions = attrs["questions"]
            if not questions:
                raise serializers.ValidationError({'questions': "Questions cannot be empty"})
            
            if not any(q.get("mandatory", False) for q in questions):
                raise serializers.ValidationError({'mandatory': "At least one question must be mandatory=True"})

        return attrs
    

class SurveyFormDetailSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(many=True, read_only=True, slug_field="key")
    questions = SurveyQuestionSerializer(many=True, source="SurveyQuestion_form"    )

    class Meta:
        model = SurveyForm
        fields = ("id", "name", "permissions", "status", "questions")
