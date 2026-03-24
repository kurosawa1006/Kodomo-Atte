from django.shortcuts import render


def top_view(request):
    return render(request, "nursery/top.html")
