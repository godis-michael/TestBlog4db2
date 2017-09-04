from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import SelectDateWidget
from smart_selects.form_fields import ChainedModelChoiceField
from cities_light.models import Country, Region, City
from .models import User, Article


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.',
        validators=[
            RegexValidator(
                regex=r'^[A-Z][a-z]+$',
                code='invalid_first_name',
                message='First name should be 2 or more letters starting from capital.'),
        ])
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.',
        validators=[
            RegexValidator(
                regex=r'^[A-Z][a-z]+$',
                code='invalid_last_name',
                message='Surname name should be 2 or more letters starting from capital.'),
        ])
    birth_date = forms.DateField(
        required=False,
        # widget=SelectDateWidget(years=range(1900, 2017)),
        help_text='Optional.')
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.')

    # country = forms.ModelChoiceField(
    #     Country.objects.all(),
    #     empty_label='select country',
    #     label='country')
    # region = ChainedModelChoiceField(
    #     queryset = Region.objects.all(),
    #     empty_label='select region',
    #     label='region',
    #     to_app_name='blog',
    #     to_model_name='region',
    #     chained_field='country',
    #     chained_model_field='country',
    #     foreign_key_app_name='blog',
    #     foreign_key_model_name='user',
    #     foreign_key_field_name='country',
    #     show_all=False,
    #     auto_choose=True,)
    #     # sort=True)
    # city = ChainedModelChoiceField(
    #     queryset=City.objects.all(),
    #     empty_label='select city',
    #     label='city',
    #     to_app_name='blog',
    #     to_model_name='city',
    #     chained_field='region',
    #     chained_model_field='region',
    #     foreign_key_app_name='blog',
    #     foreign_key_model_name='user',
    #     foreign_key_field_name='city',
    #     show_all=False,
    #     auto_choose=True,)
    #     # sort=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'birth_date',
            'country',
            'region',
            'city',
            'email',
            'password1',
            'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'Select country, region and city below'



class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'title',
            'text',)
