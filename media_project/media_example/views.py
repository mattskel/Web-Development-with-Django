import os
from django.shortcuts import render
from django.conf import settings

from .forms import UploadForm

# Create your views here.
def media_example(request):
  if request.method == 'POST':
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
      save_path = os.path.join(settings.MEDIA_ROOT, form.cleaned_data["file_upload"].name)

      with open(save_path, 'wb') as output_file:
        for chunk in form.cleaned_data['file_upload'].chunks():
          output_file.write(chunk)

  else:
    form = UploadForm()
  
  return render(request, 'media-example.html', {'form': form})