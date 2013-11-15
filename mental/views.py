#coding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required  
import datetime
from forms import MentalForm
from models import MentalModel

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
            form.save()
            # request.session['startdate'] = request.POST['startdate']
            # request.session['starttime'] = request.POST['starttime']
            return HttpResponseRedirect('/admin/') # Redirect
    return render_to_response('mentalinput.html', {"form":form,"jscal_min":jscal_min, "jscal_max":jscal_max})

def mentalselect(request, name="", ppid=""):
    curppname = [u"姓名", u"区县", u"身份证号", u"户口类别", u"监护人", u"联系电话"]
    curpp     = ["","","","","",""]

    if request.method == 'POST':
        if name == "" and ppid=="":
            name = request.POST['name']
            ppid = request.POST['ppid']

        cur_re = MentalModel.objects.filter(name__icontains=name, ppid__icontains=ppid)
        if len(cur_re) != 0:
            curtotal = []
            for ipp in cur_re:
                curtotal.append([ipp.name,  ipp.county, ipp.ppid, ipp.iscity, ipp.guardian, ipp.phone])
            curpp =curtotal
        else:
            curpp[0] = "没有登记"

    return render_to_response('mentalselect.html', {'curpp': curpp, 'curppname':curppname})