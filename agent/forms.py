# from crm.lead.models import User
from django.db.models import fields
# from crm.lead.forms import LeadForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
# from django.contrib.auth import get_user_model

user = get_user_model()


class AgentModelForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ('email', 'username', 'first_name', 'last_name', )
