from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from ..models import SurveyForm, SurveyQuestion, SurveyOption, SurveyPermission

from ..serializers.SurveyFormSerializers import (SurveyFormCreateSerializer, SurveyFormListSerializer,
                                                SurveyFormDetailSerializer, SurveyFormResponseSerializer,)



class SurveyFormCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SurveyFormCreateSerializer
    queryset = SurveyForm.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        form = SurveyForm.objects.create(name=data["name"], status=data["status"])
        permissions_qs = SurveyPermission.objects.filter(id__in=data["permissions"])
        form.permissions.set(permissions_qs)

        for q in data["questions"]:
            question = SurveyQuestion.objects.create(
                form=form,
                label=q.get("label"),
                placeholder=q.get("placeholder", ""),
                type=q.get("type"),
                mandatory=q.get("mandatory", False),
                default_hide=q.get("default_hide", False),
                use_for_analytics=q.get("use_for_analytics", False),)

            SurveyOption.objects.bulk_create([
                SurveyOption(
                    question=question,
                    text=opt.get("text") if isinstance(opt, dict) else opt
                )
                for opt in q.get("options", [])
            ])

        response_serializer = SurveyFormResponseSerializer(form, context={"request": request})

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    
class SurveyFormListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SurveyFormListSerializer
    queryset = SurveyForm.objects.prefetch_related("permissions","SurveyQuestion_form__SurveyOption_question")

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search")    
        if search:
            queryset = queryset.filter(name=search)
        return queryset


class SurveyFormUpdateAPIView(UpdateAPIView):
    queryset = SurveyForm.objects.all().prefetch_related("permissions", "SurveyQuestion_form__SurveyOption_question")
    permission_classes = [AllowAny]
    serializer_class = serializers.Serializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        instance.name = data.get("name", instance.name)
        instance.status = data.get("status", instance.status)
        instance.save()

        if "questions" in data:
            instance.SurveyQuestion_form.all().delete()
            questions_to_create = [
                SurveyQuestion(
                    form=instance,
                    label=q.get("label"),
                    placeholder=q.get("placeholder", ""),
                    type=q.get("type"),
                    mandatory=q.get("mandatory", False),
                    default_hide=q.get("default_hide", False),
                    use_for_analytics=q.get("use_for_analytics", False)
                )
                for q in data["questions"]
            ]
            
            created_questions = SurveyQuestion.objects.bulk_create(questions_to_create)
            options_to_create = []
            for question, q_data in zip(created_questions, data["questions"]):
                opts = [
                    SurveyOption(
                        question=question,
                        text=opt.get("text") if isinstance(opt, dict) else opt
                    )
                    for opt in q_data.get("options", [])
                ]
                options_to_create.extend(opts)
            SurveyOption.objects.bulk_create(options_to_create)

        response_serializer = SurveyFormResponseSerializer(instance, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    

class SurveyFormDetailAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = SurveyFormDetailSerializer
    queryset = SurveyForm.objects.prefetch_related("permissions", "SurveyQuestion_form__SurveyOption_question")
