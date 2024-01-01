from django.shortcuts import render

# Create your views here.
def index(request):
    names = "john,doe,mark,swain"
    return render(request, "index.html", {'names': names})