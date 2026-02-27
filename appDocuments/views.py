from django.shortcuts import render  # noqa: F401

from .forms import IpemDataRegisterForm


def home(request):
    ...


def ipemData_receive(request):
    ...


def ipemData_send(request):
    POST = None
    if request.POST:
        POST = request.POST

    form = IpemDataRegisterForm(POST)
    return render(request,
                  'appDocuments/pages/ipem_data.html',
                  context={'form': form}
                  )
