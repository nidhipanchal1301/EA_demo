from django.db import models

from django.contrib.auth.models import User

from .utils.BaseModel import TimeStampedModel



class SurveyPermissionChoices(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    TELE_SALES = "tele_sales", "Tele Sales"
    TRADE_DEVELOPER = "trade_developer", "Trade Developer"


class SurveyPermission(models.Model):
    key = models.CharField(max_length=50, choices=SurveyPermissionChoices.choices)

    def __str__(self):
        return self.key

    class Meta:
        db_table = "survey_permissions"



class SurveyForm(TimeStampedModel):

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=255, null=True, blank=True)
    permissions = models.ManyToManyField(SurveyPermission, related_name="SurveyForm_permissions", blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):      
        return self.name
    
    class Meta:
        db_table = "survey_forms"


class SurveyQuestion(TimeStampedModel):

    class QuestionTypes(models.TextChoices):
        SHORT_TEXT ="short_text", "Short Text"
        LONG_TEXT = "long_text", "Long Text"
        DATE = "date", "Date"
        NUMBER = "number", "Number"
        MOBILE_NUMBER = "mobile_number", "Mobile Number"
        SINGLE_CHOICE = "single_choice", "Single Choice"
        MULTI_CHOICE = "multi_choice", "Multiple Choice"

    form = models.ForeignKey(SurveyForm, related_name="SurveyQuestion_form", on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    placeholder = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=20, choices=QuestionTypes.choices)
    mandatory = models.BooleanField(default=False)
    default_hide = models.BooleanField(default=False)
    use_for_analytics = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label} ({self.form.name})"
    
    class Meta:
        db_table = "survey_questions"


class SurveyOption(TimeStampedModel):
    question = models.ForeignKey(SurveyQuestion, related_name="SurveyOption_question", on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = "survey_options"
