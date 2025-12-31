from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from ..models import SurveyForm, SurveyQuestion, SurveyOption, SurveyPermission

from ..serializers.SurveyFormSerializers import (SurveyFormCreateSerializer, SurveyFormListSerializer,
                                                SurveyFormDetailSerializer, SurveyFormResponseSerializer, 
                                                SurveyFormUpdateSerializer,)
                                                


class SurveyFormCreateAPIView(CreateAPIView):
    queryset = SurveyForm.objects.all().prefetch_related("permissions", "SurveyQuestion_form__SurveyOption_question")
    permission_classes = [AllowAny]
    serializer_class = SurveyFormCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        instance = SurveyForm.objects.create(name=data["name"],status=data.get("status", "active"))
        permissions_qs = SurveyPermission.objects.filter(id__in=data["permissions"])
        instance.permissions.set(permissions_qs)

        questions_to_create = [
            SurveyQuestion(
                form=instance,
                label=q.get("label"),
                placeholder=q.get("placeholder", ""),
                type=q.get("type"),
                mandatory=q.get("mandatory", False),
                default_hide=q.get("default_hide", False),
                use_for_analytics=q.get("use_for_analytics", False),
            )
            for q in data["questions"]
        ]

        created_questions = SurveyQuestion.objects.bulk_create(questions_to_create)

        options_to_create = [
            SurveyOption(
                question=created_q,
                text=(opt.get("text") if isinstance(opt, dict) else opt)
            )
            for created_q, original_q in zip(created_questions, data["questions"])
            for opt in original_q.get("options", [])
            if original_q.get("type") in ["single_choice", "multi_choice"]
        ]


        if options_to_create:
            SurveyOption.objects.bulk_create(options_to_create)

        response_serializer = SurveyFormResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)



    
class SurveyFormListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SurveyFormListSerializer
    queryset = SurveyForm.objects.prefetch_related("permissions","SurveyQuestion_form__SurveyOption_question")

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search")    

        if search:
            queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(permissions__key__icontains=search)
        ).distinct()
        return queryset


class SurveyFormUpdateAPIView(UpdateAPIView):
    queryset = SurveyForm.objects.all().prefetch_related("permissions", "SurveyQuestion_form__SurveyOption_question")
    permission_classes = [AllowAny]
    serializer_class = SurveyFormUpdateSerializer

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

            options_to_create = [
                SurveyOption(question=question, text=(opt.get("text")if isinstance(opt, dict)else opt))
                for question, q_data in zip(created_questions, data["questions"])
                for opt in q_data.get("options", [])
            ]

            SurveyOption.objects.bulk_create(options_to_create)

        response_serializer = SurveyFormResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    

class SurveyFormDetailAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = SurveyFormDetailSerializer
    queryset = SurveyForm.objects.prefetch_related("permissions", "SurveyQuestion_form__SurveyOption_question")
