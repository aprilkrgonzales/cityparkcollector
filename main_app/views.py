from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import uuid
import boto3
from .models import Park, Feature, Photo
from .forms import VisitForm

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'cityparkcollector-bucket'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('parks')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {
        'form': form, 
        'error_message': error_message
    }
    return render(request, 'registration/signup.html', context)

@login_required
def parks_index(request):
    # parks = Park.objects.all()
    # ^^^ this code will make all parks appear ^^^
    parks = Park.objects.filter(user=request.user)
    # ^^^ this code will make only the parks the user has created appear ^^^
    return render(request, 'parks/index.html', {'parks': parks})

@login_required
def parks_detail(request, park_id):
    park = Park.objects.get(id=park_id)
    features_park_doesnt_have = Feature.objects.exclude(id__in = park.features.all().values_list('id'))
    visit_form = VisitForm()
    return render(request, 'parks/detail.html', {
        'park': park,
        'visit_form': visit_form,
        'features': features_park_doesnt_have
    })

@login_required
def add_visit(request, park_id):
    form = VisitForm(request.POST)
    form.instance.user = request.user
    if form.is_valid():
        new_visit = form.save(commit=False)
        new_visit.park_id = park_id
        new_visit.save()
    return redirect(
        'detail', 
        park_id=park_id
    )

#  ^^^ function for create visit

# class VisitCreate(CreateView):
#     model = VisitForm
#     fields = '__all__'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

class ParkCreate(LoginRequiredMixin, CreateView):
    model = Park
    fields = ['name', 'neighborhood', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ParkUpdate(LoginRequiredMixin, UpdateView):
    model = Park
    fields = ['neighborhood', 'description']

class ParkDelete(LoginRequiredMixin, DeleteView):
    model = Park
    success_url = '/parks/'

class ParkList(LoginRequiredMixin, ListView):
    model = Park

@login_required
def assoc_feature(request, park_id, feature_id):
    Park.objects.get(id=park_id).features.add(feature_id)
    return redirect('detail', park_id=park_id)

@login_required
def unassoc_feature(request, park_id, feature_id):
    Park.objects.get(id=park_id).features.remove(feature_id)
    return redirect('detail', park_id=park_id)

class FeatureCreate(LoginRequiredMixin, CreateView):
    model = Feature
    fields = '__all__'
    success_url = '/features/'

class FeatureDetail(LoginRequiredMixin, DetailView):
    model = Feature

class FeatureList(LoginRequiredMixin, ListView):
    model = Feature

class FeatureUpdate(LoginRequiredMixin, UpdateView):
    model = Feature
    fields = ['name']

class FeatureDelete(LoginRequiredMixin, DeleteView):
    model = Feature
    success_url = '/features/'

@login_required
def add_photo(request, park_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, park_id=park_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', park_id=park_id)
