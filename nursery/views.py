from django.shortcuts import render

from .models import Children


def top_view(request):
    children_list = Children.objects.all()
    return render(request, "nursery/top.html", {"children_list": children_list})
