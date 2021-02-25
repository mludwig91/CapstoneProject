"""
This module contains custom forms used to collect the information needed to create a model.
"""
from django import forms
from .models import UserInformation, SponsorCompany


class UserInformationForm(forms.ModelForm):
    """
    This form creates an instance of a UserInformation model and collects its fields
    """
    states = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
        ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'),
        ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'),
        ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
        ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
        ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]

    # Fields that will need to be completed in this form
    user_email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'readonly': 'readonly'}))  # read only
    first_name = forms.CharField(label='First Name', max_length=25)
    last_name = forms.CharField(label='Last Name', max_length=25)
    phone_number = forms.IntegerField(label='Phone Number', max_value=9999999999, min_value=1000000000)
    sponsor_company = forms.ModelChoiceField(label='Sponsor', queryset=SponsorCompany.objects.all())
    address = forms.CharField(label='Address', max_length=100)
    license_number = forms.CharField(label='License', max_length=20)
    state = forms.ChoiceField(label='State', choices=states)

    def __init__(self, *args, **kwargs):
        """function __init__ is called to instantiate the user information form

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(UserInformationForm, self).__init__(*args, **kwargs)

        # Validator that makes sure all the fields have been filled in
        for _field_name, field in self.fields.items():
            field.required = True

    class Meta:
        """
        A class that stores the meta information about this form
        """
        model = UserInformation
        fields = ['user_email', 'first_name', 'last_name', 'phone_number', 'sponsor_company', 'address', 'license_number', 'state']



