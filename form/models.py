import datetime

from django.db import models
from django.utils import timezone

from . import constants
import hashlib, random, sys
from django.db import models
from . import constants

def create_session_hash():
  hash = hashlib.sha1()
  hash.update(str(random.randint(0,sys.maxsize)).encode('utf-8'))
  return hash.hexdigest()

class PersonalInfo(models.Model):
    # operational
    session_hash = models.CharField(max_length=40, unique=True)
    stage = models.CharField(max_length=10, default=constants.STAGE_1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    hidden_fields = ['stage', 'date_of_birth']
    required_fields = ['name', 'email', 'age']

    # stage 1
    name = models.CharField(max_length=100, verbose_name='Név')
    birthname = models.CharField(max_length=100, verbose_name='Születési név (na nem egyezik)', blank=True)
    place = models.CharField(max_length=100, verbose_name='Születési hely')
    gender = models.CharField(max_length=100, verbose_name='Nem')
    haircolor = models.CharField(max_length=20, verbose_name='Hajszín', blank=True)

    # stage 2
    url = models.CharField(max_length=100, verbose_name='Saját honlap', blank=True)
    email = models.EmailField(max_length=50, verbose_name='E-mail cím')
    phone_number = models.CharField(max_length=100, verbose_name='Telefonszám')
    marital_status = models.CharField(max_length=100, verbose_name='Családi állapot', blank=True)
    address = models.CharField(max_length=100, verbose_name='Cím')

    # stage 3
    picture = models.FileField(upload_to='media/uploads/', verbose_name='Töltsön fel egy képet magáról!')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.session_hash:
            while True:
                session_hash = create_session_hash()
                if PersonalInfo.objects.filter(session_hash=session_hash).count() == 0:
                    self.session_hash = session_hash
                    break

    @staticmethod
    def get_fields_by_stage(stage):
        fields = ['stage']
        if stage == constants.STAGE_1:
            fields.extend(['name', 'birthname', 'place', 'gender', 'haircolor'])
        elif stage == constants.STAGE_2:
            fields.extend(['url', 'email', 'phone_number', 'marital_status', 'address'])
        elif stage == constants.STAGE_3:
            fields.extend(['picture'])
        return fields
