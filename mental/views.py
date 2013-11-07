#coding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required  
import datetime
from forms import MentalForm

@login_required(login_url="/login/")
def about(request):
    return render_to_response('about.html')


def mentalinput(request):
    # request.session['gameclass'] = ""
    today   = datetime.date.today()

    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    form = MentalForm()
    # print form
    # gameclass = request.session['gameclass']
    if request.method == "POST":
        form = MentalForm(request.POST)
        if form.is_valid():
            # request.session['startdate'] = request.POST['startdate']
            # request.session['starttime'] = request.POST['starttime']
            return HttpResponseRedirect('/about/') # Redirect
    return render_to_response('mentalinput.html', {"form":form,"jscal_min":jscal_min, "jscal_max":jscal_max})

