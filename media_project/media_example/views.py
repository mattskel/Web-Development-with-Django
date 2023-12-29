from django.shortcuts import render

# Create your views here.
def media_example(request):
  return render(request, 'media-example.html')