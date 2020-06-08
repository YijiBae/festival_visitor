from django.forms import ModelForm
from fes_visitor.models import Option

#view에서 생성할 수 있다. 

class Form(ModelForm):
    class Meta:
        model = Option
        fields = ['fes_name', 'fes_start_year', 'fes_start_month', 'fes_start_day', 'fes_end_year', 'fes_end_month', 'fes_end_day'] 

