from django.test import TestCase
from accounts.models import  User, UserInformation, SponsorCompany

class TestModel(TestCase):
    def setUp(self):
        company = SponsorCompany.objects.create(company_name = 'The Empire', company_phone_number = 1233211234, company_street_address= '101 Death Star avenue', company_city = 'StormTrooper City', company_state = 'SC', company_zipcode = 66666, company_point_ratio = 1, company_about_info = 'This is a test sponsor company info')
        company.save()
        uzer = User.objects.create(username="joe dirt", email="testy@aol.com",  first_name="joe")
        uzer.save()
        driverUser = UserInformation.objects.create(user = uzer, role_name = 'driver',first_name='joe',last_name='master', phone_number =6666666666, is_email_verified=True,is_active_account = 'True', sponsor_company = company, points = 100, state = 'SC', item_count = 0)
        driverUser.save()

    def test_driver_sponsor_and_company_creation(self):
        darth = UserInformation.objects.get(first_name = 'joe')
