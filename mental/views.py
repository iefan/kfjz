#coding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required  
import datetime
from forms import MentalForm, MentalForm2, ApprovalForm, ApplyForm
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
            return HttpResponseRedirect('/admin/') # Redirect
    return render_to_response('mentalinput.html', {"form":form,"jscal_min":jscal_min, "jscal_max":jscal_max})

def mentalselect(request, name="", ppid=""):
    curppname = [u"姓名", u"区县", u"身份证号", u"户口类别", u"监护人", u"联系电话", u"修改", u"申请求助"]
    curpp     = [[["","","","","",""], "", ""]]

    if request.method == 'POST':
        if name == "" and ppid=="":
            name = request.POST['name']
            ppid = request.POST['ppid']

        cur_re = MentalModel.objects.filter(name__icontains=name, ppid__icontains=ppid)
        if len(cur_re) != 0:
            curpp = []
            for ipp in cur_re:
                curpp.append([[ipp.name,  ipp.county, ipp.ppid, ipp.iscity, ipp.guardian, ipp.phone], ipp.id, ipp.ppid])
        else:
            curpp[0][0][0] = "没有登记"

    return render_to_response('mentalselect.html', {'curpp': curpp, 'curppname':curppname})

def mentalmodify(request, curid="0"):
    if curid == "0":
        return HttpResponseRedirect('/mentalselect/')

    try:
        curpp = MentalModel.objects.get(id=curid)
    except MentalModel.DoesNotExist:
        return HttpResponseRedirect('/mentalselect/')

    nomodifyinfo = [u"姓名：%s"  % curpp.name, u"身份证号：%s" % curpp.ppid]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    form = MentalForm2(instance=curpp)
    if request.method == "POST":
        form = MentalForm2(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return mentalselect(request, curpp.name, curpp.ppid)

    return render_to_response('mentalmodify.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max})

def approvalinput(request):
    '''批准视图'''
    form = ApprovalForm()
    if request.method == "POST":
        form = ApprovalForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/') # Redirect
    return render_to_response('approvalinput.html', {"form":form})

def applyinput(request, curppid="111456789000"):
    '''申请求助视图'''
    if curppid == "":
        return HttpResponseRedirect('/mentalselect/')

    try:
        curpp = MentalModel.objects.get(ppid=curppid)
    except MentalModel.DoesNotExist:
        return HttpResponseRedirect('/mentalselect/')

    nomodifyinfo = [u"姓名：%s"  % curpp.name, u"身份证号：%s" % curpp.ppid]

    form = ApplyForm()
    if request.method == "POST":
        form = ApplyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/') # Redirect
    return render_to_response('applyinput.html', {"form":form, "nomodifyinfo":nomodifyinfo,})