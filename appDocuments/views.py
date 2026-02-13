from django.shortcuts import render  # noqa: F401

from .forms import IpemDataRegisterForm


def home(request):
    ...


def ipemData(request):
    form = IpemDataRegisterForm()
    return render(request,
                  'appDocuments/pages/ipem_data.html',
                  context={'form': form}
                  )
