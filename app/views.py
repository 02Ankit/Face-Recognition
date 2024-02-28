from django.shortcuts import render
from django.http import HttpResponse
from app.forms import FaceRecognitionForm
#connect views to machinelearning model
from app.machinelearning import pipeline_model
from django.conf import settings 
# we need to extract the data from model 
from app.models import FaceRecognition
import os 
# Create your views here.

# def index(request):
#     return HttpResponse("Hello World")

# def index1(request):
#     return HttpResponse("Second Response")

# def index2(request):
#     return render(request, 'index.html')

def index(request):
     form  = FaceRecognitionForm()
    #  Check wheter the request is GET or POST ?
     if request.method == 'POST':
          form = FaceRecognitionForm(request.POST or None, request.FILES or None)
          if form.is_valid():
               save =  form.save(commit=True)

                # extract the image object from database
               primary_key = save.pk
               imgobj = FaceRecognition.objects.get(pk=primary_key) 
               fileroot = str(imgobj.image)#image is key name from model of facerecognition
               filepath = os.path.join(settings.MEDIA_ROOT,fileroot)
               #just pass the filepath t pipeline model 
               results = pipeline_model(filepath)
               print(results)

               return render(request,'index.html',{'form':form,'upload':True,'results':results})

     return render(request, 'index.html', {'form':form, 'upload':False})
