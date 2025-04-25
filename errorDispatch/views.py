from django.shortcuts import render  # type: ignore


def loadReport(request):
    return render(request, 'errorDispatch/pages/errordispatch.html')
