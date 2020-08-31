from django.shortcuts import render

# Create your views here.
def school(request):
    return render(request, 'school.html')