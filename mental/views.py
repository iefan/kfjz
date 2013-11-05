#coding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required  

@login_required(login_url="/login/")
def about(request):
    return render_to_response('about.html')