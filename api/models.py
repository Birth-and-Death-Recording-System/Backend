from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from rand import generate_random_unique_number as unique_numbers
from django_countries.fields import CountryField

# Create your models here.
GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
ID_CHOICES = [('G', 'Ghana Card'), ('V', "Voter's ID"), ('N', "NHIS"), ('D', "Driver's License"), ('P', 'Passport')]
RELATIONSHIP_CHOICES = [('P', 'Parent'), ('S', 'Sibling'), ('Se', 'Self'), ('G', 'Guardian'), ('O', 'Other')]
BURIAL_CHOICES = [('B', 'Buried'), ('N', 'Not Buried')]


class User(AbstractUser):
    ROLE_CHOICES = [('N', 'Nurse'), ('D', 'Doctor')]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    username = models.CharField('Username', max_length=255, unique=True)
    email = models.EmailField('Email', unique=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='N')
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default='M')

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    username = models.CharField('Username', max_length=255, unique=True)
    birth_date = models.DateField('Birth', blank=True, null=True)
    email = models.EmailField('Email', null=False)
    phone_number = models.CharField('Phone Number', blank=True, default='', max_length=10, validators=[MinLengthValidator(10), RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits long and contain only numbers.')],)
    gender = models.CharField('Gender', max_length=10, choices=GENDER_CHOICES, default='M')

    def __str__(self):
        return f'{self.user.username} Profile'


class Birth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    CIN = models.CharField('CIN', max_length=50, unique=True, blank=True)
    First_Name = models.CharField('First Name', max_length=255, blank=True)
    Last_Name = models.CharField('Last Name', max_length=255, blank=True)
    Other_Name = models.CharField('Other Names', max_length=255, blank=True)
    date = models.DateField('Date of Birth')
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default='M')
    City = models.CharField('City', max_length=255)
    Place_of_Birth = models.CharField('Place Of Birth', max_length=255)
    # Informant
    Informant_name = models.CharField('Informant Name', max_length=255)
    Relationship = models.CharField('Relationship', max_length=255, choices=RELATIONSHIP_CHOICES)
    Informant_Phone_Number = models.IntegerField("Informant's Phone Number", blank=True, default=0000000000)
    # Particulars of Father
    Father_First_Name = models.CharField("Father's First Name", max_length=255, blank=True)
    Father_Last_Name = models.CharField("Father's Last Name", max_length=255, blank=True)
    Father_Nationality = models.CharField("Father's Nationality", max_length=255)
    Father_ID_type = models.CharField("Father's ID Type", max_length=255, choices=ID_CHOICES, blank=True)
    Father_ID_Number = models.CharField("Father's ID Number", max_length=255, blank=True)
    Father_DOB = models.DateField("Father's DOB", max_length=255, blank=True)
    Father_Phone_Number = models.IntegerField("Father's Phone Number", blank=True, default=0000000000)
    # Particulars of Mother
    Mother_First_Name = models.CharField("Mother's First Name", max_length=255, blank=True)
    Mother_Last_Name = models.CharField("Mother's Last Name", max_length=255, blank=True)
    Mother_Nationality = models.CharField("Mother's Nationality", max_length=255)
    Mother_ID_type = models.CharField("Mother's ID Type", max_length=255, choices=ID_CHOICES, blank=True)
    Mother_ID_number = models.CharField("Mother's ID Number", max_length=255)
    Mother_DOB = models.DateField("Mother's DOB", max_length=255)
    Mother_Phone_Number = models.IntegerField("Mother's Phone Number", blank=True, default=0000000000)

    def __str__(self):
        return self.CIN + " " + self.First_Name

    @property
    def age(self):
        if self.Father_DOB is not None:
            father_age = date.today().year - self.Father_DOB.year
            return father_age

        if self.Mother_DOB is not None:
            mother_age = date.today().year - self.Mother_DOB.year
            return mother_age

    def save(self, *args, **kwargs):
        if not self.CIN:
            self.CIN = unique_numbers()
        super().save(*args, **kwargs)


class Death(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deaths", null=True)
    surname = models.CharField("Surname", max_length=255, blank=True)
    first_name = models.CharField("First Name", max_length=255, blank=True)
    Other_Name = models.CharField("Other Name", max_length=255, blank=True)
    birth_date = models.DateField("Birth Date", blank=True)
    Gender = models.CharField("Gender", max_length=1, choices=GENDER_CHOICES)
    Burial_Status = models.CharField("Burial Status", max_length=1, choices=BURIAL_CHOICES, default='N', blank=True)
    Nationality = models.CharField("Nationality", max_length=255)
    ID_Type = models.CharField("ID_Type", choices=ID_CHOICES, max_length=1, blank=True)
    ID_Number = models.CharField("ID_Number", max_length=255, blank=True)
    Residence_addr = models.CharField("Residence Address", max_length=255)
    # Deceased Identification Particulars
    date = models.DateField("Death Date", blank=True)
    Cause_of_Death = models.TextField("Cause of Death", blank=True)
    Place_of_Death = models.TextField("Place of Death", blank=True)
    Address_of_place = models.TextField("Address of Place", blank=True)
    # Particulars of Informant
    Informant_Name = models.CharField("Informant Name", max_length=255, blank=True)
    Informant_ID_Type = models.CharField("ID_Type", choices=ID_CHOICES, max_length=255, blank=True)
    Informant_ID_Number = models.CharField("ID_Number", max_length=255, blank=True)
    Relationship_Type = models.CharField("Relationship Type", choices=RELATIONSHIP_CHOICES, max_length=255, blank=True)
    Phone_Number = models.IntegerField("Phone Number", blank=True, default=0000000000)
    Email_Address = models.EmailField("Email Address", max_length=255, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.first_name


class ActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.user.username + " - " + self.action_type


# models.py


class BirthRecord(models.Model):
    recorder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    birth = models.ForeignKey(Birth, on_delete=models.CASCADE, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True, null=True)
    action_type = models.CharField(max_length=50, default="Birth recorded")
    details = models.TextField(blank=True, default="none")

    def __str__(self):
        if self.recorder and self.recorder.username:
            return f"{self.recorder.username} - {self.birth.First_Name if self.birth else 'No Birth'}"
        else:
            return "Recorder is None - No Birth Record"


class DeathRecord(models.Model):
    recorder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    death = models.ForeignKey(Death, on_delete=models.CASCADE, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True, null=True)
    action_type = models.CharField(max_length=50, default="Death recorded")
    details = models.TextField(blank=True, default="none")

    def __str__(self):
        if self.death:
            return f"{self.recorder.username} - {self.death.first_name}"
        else:
            return f"{self.recorder.username} - [Deleted Death]"
