from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView

from ..models import SurveyForm, SurveyQuestion, SurveyOption, SurveyPermission

from ..serializers.SurveyFormSerializers import SurveyFormCreateSerializer

from rest_framework.permissions import AllowAny



class SurveyFormCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = SurveyForm.objects.all()
    serializer_class = SurveyFormCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        form = SurveyForm.objects.create(name=data.get("name"), status=data.get("status", "active"),)
        permission_ids = data.get("permissions", [])
        permissions_qs = SurveyPermission.objects.filter(id__in=permission_ids)
        form.permissions.set(permissions_qs)
        form.refresh_from_db()  
        for q in data.get("questions", []):
            question = SurveyQuestion.objects.create(
                form=form,
                label=q.get("label"),
                placeholder=q.get("placeholder"),
                type=q.get("type"),
                mandatory=q.get("mandatory", False),
                default_hide=q.get("default_hide", False),
                use_for_analytics=q.get("use_for_analytics", False),
            )
            for opt in q.get("options", []):SurveyOption.objects.create(question=question, text=opt.get("text"))

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

        return Response(response_data, status=status.HTTP_201_CREATED)

    
class SurveyFormListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = SurveyForm.objects.prefetch_related('permissions', 'questions_form__options_question')

    def list(self, request, *args, **kwargs):
        forms = self.get_queryset()
        response = []

        for form in forms:
            total_questions = form.questions_form.count()
            questions_list = []
            for question in form.questions_form.all():
                questions_list.append({
                    "question": question.label,
                    "type": question.type,
                    "values": [opt.text for opt in question.options_question.all()]
                })

            form_data = {
                "id": form.id,
                "name": form.name,
                "permissions": [p.key for p in form.permissions.all()],
                "status": form.status,
                "total_questions": total_questions,
                "questions": questions_list
            }
            response.append(form_data)

        return Response(response)


class SurveyFormUpdateAPIView(UpdateAPIView):
    queryset = SurveyForm.objects.all().prefetch_related("permissions", "questions_form__options_question")
    permission_classes = [AllowAny]
    serializer_class = serializers.Serializer

    def update(self, request, *args, **kwargs):
        form = self.get_object()
        data = request.data
        form.name = data.get("name", form.name)
        form.status = data.get("status", form.status)
        form.save()

        if "permissions" in data:
            permission_ids = data.get("permissions", [])
            permissions_qs = SurveyPermission.objects.filter(id__in=permission_ids)
            form.permissions.set(permissions_qs)

        if "questions" in data:
            form.questions_form.all().delete()

            for q_data in data["questions"]:
                options_data = q_data.get("options", [])
                question = SurveyQuestion.objects.create(
                    form=form,
                    label=q_data.get("label"),
                    placeholder=q_data.get("placeholder"),
                    type=q_data.get("type"),
                    mandatory=q_data.get("mandatory", False),
                    default_hide=q_data.get("default_hide", False),
                    use_for_analytics=q_data.get("use_for_analytics", False)
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
    queryset = SurveyForm.objects.prefetch_related("permissions", "questions_form__options_question")

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
