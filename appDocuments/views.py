from django.shortcuts import render  # noqa: F401


def home(request):
    ...


def ipemData(request):
    return render(request, 'appDocuments/pages/ipem_data.html')
