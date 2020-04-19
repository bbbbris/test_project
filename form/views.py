import datetime, pytz
import requests
from PIL import Image

from django.forms import modelform_factory
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from . import constants
from .forms import BaseApplicationForm
from .models import PersonalInfo

def thanks(request):
    return render(request, 'form/thanks.html')

@csrf_exempt
def pdf_collector(request):
    print("#######################")
    print(request.FILES['pdf'].name)
    return HttpResponse('')

def get_job_application_from_hash(session_hash):
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    max_age = 300 
    exclude_before = now - datetime.timedelta(seconds=max_age)
    return PersonalInfo.objects.filter(session_hash=session_hash,modified__gte=exclude_before).exclude(stage=constants.COMPLETE).first()


class PersonalInfoView(FormView):
    template_name = 'form/personal_info.html'
    job_application = None
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        session_hash = request.session.get("session_hash", None)
        self.job_application = get_job_application_from_hash(session_hash)
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session["session_hash"] = form.instance.session_hash
        current_stage = form.cleaned_data.get("stage")
        new_stage = constants.STAGE_ORDER[constants.STAGE_ORDER.index(current_stage)+1]
        form.instance.stage = new_stage
        form.save()
        if new_stage == constants.COMPLETE:
            picture_name = self.request.FILES['picture'].name
            image = Image.open('media/uploads/' + picture_name)
            im1 = image.convert('RGB')
            im1.save('media/converts/' + picture_name + '.pdf')
            with open('media/converts/' + picture_name + '.pdf', 'rb') as pdf:
                requests.post('http://localhost:8000/form/pdf-image/', files = {'pdf':pdf})

            return redirect(reverse("form:thanks"))
        # else
        return redirect(reverse("form:personal_info"))

    def get_form_class(self):
        stage = self.job_application.stage if self.job_application else constants.STAGE_1
        fields = PersonalInfo.get_fields_by_stage(stage)
        return modelform_factory(PersonalInfo, BaseApplicationForm, fields)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.job_application
        return kwargs
