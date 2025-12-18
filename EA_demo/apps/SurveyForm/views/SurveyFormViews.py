from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView

from ..models import SurveyForm, SurveyQuestion, SurveyOption, SurveyPermission

from ..serializers.SurveyFormSerializers import SurveyFormCreateSerializer, SurveyFormListSerializer

from rest_framework.permissions import AllowAny



class SurveyFormCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = SurveyForm.objects.all().prefetch_related("permissions", "SurveyQuestion_form__options_question")
    serializer_class = SurveyFormCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        form = SurveyForm.objects.create(name=data["name"], status=data["status"])
        permissions_qs = SurveyPermission.objects.filter(id__in=data["permissions"])

        questions_data = []
        options_data = []

        for q in data["questions"]:
            questions_data.append(SurveyQuestion(
                form=form,
                label=q["label"],
                type=q["type"],
                placeholder=q.get("placeholder", ""),
                mandatory=q.get("mandatory", False),
                default_hide=q.get("default_hide", False),
                use_for_analytics=q.get("use_for_analytics", False)
            ))

        created_questions = SurveyQuestion.objects.bulk_create(questions_data)

        for question_instance, q in zip(created_questions, data["questions"]):
            for opt in q["options"]:
                options_data.append(SurveyOption(
                    question=question_instance,
                    text=opt
                ))

        SurveyOption.objects.bulk_create(options_data)

        response_data = {
            "id": form.id,
            "name": form.name,
            "status": form.status,
            "created_at": form.created_at,
            "permissions": [p.key for p in permissions_qs],
            "questions": [
                { 
                    "label": q["label"],
                    "type": q["type"],
                    "placeholder": q.get("placeholder", ""),
                    "mandatory": q.get("mandatory", False),
                    "default_hide": q.get("default_hide", False),
                    "use_for_analytics": q.get("use_for_analytics", False),
                    "options": q["options"]
                } for q in data["questions"]
            ]
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    
class SurveyFormListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = SurveyForm.objects.prefetch_related('permissions', 'SurveyQuestion_form__SurveyOption_question')
    serializer_class = SurveyFormListSerializer

    def list(self, request, *args, **kwargs):
        search = request.query_params.get("search")
        forms = self.get_queryset()
        if search:
            forms = forms.filter(name   =search)
        response = []

        for form in forms:
            total_questions = form.SurveyQuestion_form.count()
            questions_list = []

            for question in form.SurveyQuestion_form.all():
                questions_list.append({
                    "question": question.label,
                    "type": question.type,
                    "values": [opt.text for opt in question.SurveyOption_question.all()]
                })

            response.append({
                "id": form.id,
                "name": form.name,
                "permissions": [p.key for p in form.permissions.all()],
                "status": form.status,
                "total_questions": total_questions,
                "questions": questions_list
            })
        return Response(response)


class SurveyFormUpdateAPIView(UpdateAPIView):
    queryset = SurveyForm.objects.all().prefetch_related("permissions", "SurveyQuestion_form__options_question")
    permission_classes = [AllowAny]
    serializer_class = serializers.Serializer

    def update(self, request, *args, **kwargs):
        form = self.get_object()
        data = request.data
        form.name = data.get("name", form.name)
        form.status = data.get("status", form.status)
        form.save()

        if "permissions" in data:
            permissions_qs = SurveyPermission.objects.filter(id__in=data["permissions"])
            form.permissions.set(permissions_qs)

        if "questions" in data:
            form.questions_form.all().delete()

            for q in data["questions"]:
                question = SurveyQuestion.objects.create(
                    form=form,
                    label=q.get("label"),
                    placeholder=q.get("placeholder", ""),
                    type=q.get("type"),
                    mandatory=q.get("mandatory", False),
                    default_hide=q.get("default_hide", False),
                    use_for_analytics=q.get("use_for_analytics", False)
                )
                for opt_data in options_data:
                    SurveyOption.objects.create(
                        question=question,
                        text=opt_data.get("text")
                    )

        response_data = {
            "id": form.id,
            "name": form.name,
            "status": form.status,
            "created_at": form.created_at,
            "permissions": [p.key for p in form.permissions.all()],
            "questions": []
        }

        for i, question in enumerate(form.questions_form.all(), start=1):
            response_data["questions"].append({
                "label": f"q{i}",
                "placeholder": question.placeholder,
                "type": question.type,
                "mandatory": question.mandatory,
                "default_hide": question.default_hide,
                "use_for_analytics": question.use_for_analytics,
                "options": [opt.text for opt in question.options_question.all()]
            })

        return Response(response_data, status=status.HTTP_200_OK)
    

class SurveyFormDetailAPIView(RetrieveAPIView):
    serializer_class = serializers.Serializer
    permission_classes = [AllowAny]
    queryset = SurveyForm.objects.prefetch_related("permissions", "SurveyQuestion_form__options_question")

    def retrieve(self, request, *args, **kwargs):
        form = self.get_object()

        questions = []
        for question in form.questions_form.all():
            questions.append({
                "question": question.label,
                "type": question.type,
                "values": [opt.text for opt in question.options_question.all()]
            })

        response_data = {
            "id": form.id,
            "name": form.name,
            "permissions": [p.key for p in form.permissions.all()],
            "status": form.status,
            "total_questions": form.questions_form.count(),
            "questions": questions
        }

        return Response(response_data)
