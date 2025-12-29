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


class SurveyFormCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
    permissions = serializers.ListField(child=serializers.IntegerField(), required=True, allow_empty=False)
    questions = serializers.ListField(child=serializers.DictField(), required=True, allow_empty=False )

    
    def validate_permissions(self, value):
        if SurveyPermission.objects.filter(id__in=value).count() != len(value):
            raise serializers.ValidationError("Some permissions are invalid")
        return value

    def validate_questions(self, value):
        for index, q in enumerate(value, start=1):
            for field in ["label", "type", "options"]:
                if field not in q:
                    raise serializers.ValidationError(
                        f"Question {index}: '{field}' is required"
                    )

            options = q["options"]
            if not isinstance(options, list) or not options:
                raise serializers.ValidationError(
                    f"Question {index}: options must be a non-empty list"
                )

            for opt in options:
                if isinstance(opt, dict):
                    if "text" not in opt or not opt["text"]:
                        raise serializers.ValidationError(
                            f"Question {index}: option must contain 'text'"
                        )
                elif not isinstance(opt, str):
                    raise serializers.ValidationError(
                        f"Question {index}: option must be string or object"
                    )

            if "mandatory" in q and not isinstance(q["mandatory"], bool):
                raise serializers.ValidationError(
                    f"Question {index}: mandatory must be boolean"
                )

            if "placeholder" in q and not isinstance(q["placeholder"], str):
                raise serializers.ValidationError(
                    f"Question {index}: placeholder must be string"
                )

        return value
    

class SurveyFormResponseSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

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

    def validate_permissions(self, value):
        if not all(SurveyPermission.objects.filter(id=perm_id).exists() for perm_id in value):
            raise serializers.ValidationError("Some permissions are invalid")
        return value

    def validate_questions(self, value):
        for index, q in enumerate(value, start=1):
            for field in ["label", "type", "options"]:
                if field not in q:
                    raise serializers.ValidationError(f"Question {index}: '{field}' is required")

            options = q["options"]
            if not isinstance(options, list) or not options:
                raise serializers.ValidationError(f"Question {index}: options must be a non-empty list")

            for opt in options:
                if isinstance(opt, dict):
                    if "text" not in opt or not opt["text"]:
                        raise serializers.ValidationError(f"Question {index}: option must contain 'text'")
                elif not isinstance(opt, str):
                    raise serializers.ValidationError(f"Question {index}: option must be string or object")

            if "mandatory" in q and not isinstance(q["mandatory"], bool):
                raise serializers.ValidationError(f"Question {index}: mandatory must be boolean")
            if "placeholder" in q and not isinstance(q["placeholder"], str):
                raise serializers.ValidationError(f"Question {index}: placeholder must be string")
        return value
    

class SurveyFormDetailSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

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
