#coding=utf8
from django.shortcuts import render_to_response
# from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required  
import datetime
from forms import MentalForm, MentalForm2, ApprovalForm, ApprovalForm2, ApplyForm
from models import MentalModel, ApprovalModel

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
            return HttpResponseRedirect('/mentalselect/') # Redirect
    return render_to_response('mentalinput.html', {"form":form,"jscal_min":jscal_min, "jscal_max":jscal_max})

def mentalselect(request, curname="", curppid="", curcounty=""):
    curppname = [u"姓名", u"区县", u"身份证号", u"户口类别", u"监护人", u"联系电话", u"修改"]
    curpp     = [[["","","","","",""], "", "",]]

    if request.method == 'POST':
        curname = request.POST['name']
        curppid = request.POST['ppid']
        curcounty = request.POST['county']

    cur_re = MentalModel.objects.filter(name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty)
    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            # ApprovalModel.objects.get(mental__ppid=ipp.ppid, isenterfile="否")
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

def approvallist(request, curcounty="", curapproval=""):
    '''批准列表'''
    curppname = [u"姓名", u"区县", u"身份证号", u"户口类别", u"监护人", u"联系电话", u"修改", u"批准"]
    curpp     = [[["","","","","",""], "", "",]]

    if request.method == 'POST':
        if curapproval!="" or curcounty!= "":
            pass
        else:
            curcounty = request.POST['county']
            curapproval = request.POST['isapproval']

    if curapproval == "":
        cur_re = ApprovalModel.objects.filter(mental__county__icontains=curcounty)
    else:
        cur_re  = ApprovalModel.objects.filter(approvalsn__isnull = bool(int(curapproval)), mental__county=curcounty)

    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            if not ipp.approvalsn:
                curpp.append([[ipp.mental.name, ipp.mental.county, ipp.mental.ppid, ipp.mental.iscity, ipp.mental.guardian, ipp.mental.phone], "", ipp.mental.ppid])
            else:
                curpp.append([[ipp.mental.name,  ipp.mental.county, ipp.mental.ppid, ipp.mental.iscity, ipp.mental.guardian, ipp.mental.phone], ipp.id, '--'])
    else:
        curpp[0][0][0] = "没有登记"

    return render_to_response('approvallist.html', {'curpp': curpp, 'curppname':curppname})

def approvalinput(request, curppid=""):
    '''批准视图'''

    # 如果为空，则跳转到所有申请表中
    if curppid == "":
        return HttpResponseRedirect('/approvallist/')

    # 如果已经申批，则跳转
    # try:
    #     curpp = ApprovalModel.objects.get(approvalsn__isnull=False)
    #     return HttpResponseRedirect('/approvallist/')
    # except ApprovalModel.DoesNotExist:
    #     pass

    # 如果当前批准列表中不存在该ppid，则跳转
    try:
        curpp = ApprovalModel.objects.get(mental__ppid=curppid)
    except ApprovalModel.DoesNotExist:
        return HttpResponseRedirect('/approvallist/')

    nomodifyinfo = [u"姓名：%s"  % curpp.mental.name, u"身份证号：%s" % curpp.mental.ppid]

    today   = datetime.date.today()

    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    curpp.approvaldate = today
    form = ApprovalForm(instance=curpp)
    if request.method == "POST":
        form = ApprovalForm(request.POST, instance=curpp)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/approvallist/') # Redirect
    return render_to_response('approvalinput.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max})

def approvalmodify(request, curid="0"):
    if curid == "0":
        return HttpResponseRedirect('/approvallist/')

    try:
        curpp = ApprovalModel.objects.get(id=curid)
    except ApprovalModel.DoesNotExist:
        return HttpResponseRedirect('/approvallist/')

    nomodifyinfo = [u"申批编号：%s"  % curpp.approvalsn, u"姓名：%s"  % curpp.mental.name, \
    u"身份证号：%s" % curpp.mental.ppid, u"区县：%s" % curpp.mental.county,]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    form = ApprovalForm2(instance=curpp)
    if request.method == "POST":
        form = ApprovalForm2(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return approvallist(request, curpp.mental.county, '1')

    return render_to_response('approvalmodify.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max})

def applyinput(request, curppid="111456789000"):
    '''申请求助视图'''
    if curppid == "":
        return HttpResponseRedirect('/applylist/')

    # 如果已经申请，则跳转
    try:
        ApprovalModel.objects.get(mental__ppid=curppid)
        return HttpResponseRedirect('/applylist/')
    except ApprovalModel.DoesNotExist:
        pass

    # 如果原信息总表中不存在，则跳转
    try:
        curpp = MentalModel.objects.get(ppid=curppid)
    except MentalModel.DoesNotExist:
        return HttpResponseRedirect('/applylist/')

    nomodifyinfo = [u"姓名：%s"  % curpp.name, u"身份证号：%s" % curpp.ppid]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    # form = ApplyForm(instance=curpp)    
    form = ApplyForm(initial={'mental':curpp})
    # print form
    if request.method == "POST":
        form = ApplyForm(request.POST)        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/applylist/') # Redirect
    return render_to_response('applyinput.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max})

def applylist(request, curname="", curppid=""):
    curcounty = "金平区"

    curppname = [u"姓名", u"区县", u"身份证号", u"户口类别", u"监护人", u"联系电话", u"修改", u"申请求助"]
    curpp     = [[["","","","","",""], "", "",]]

    if request.method == 'POST':
        curname = request.POST['name']
        curppid = request.POST['ppid']

    cur_re = MentalModel.objects.filter(name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty)
    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            try:
                ApprovalModel.objects.get(mental__ppid=ipp.ppid, isenterfile="否")
                curpp.append([[ipp.name,  ipp.county, ipp.ppid, ipp.iscity, ipp.guardian, ipp.phone], ipp.id, '--'])
            except ApprovalModel.DoesNotExist:
                curpp.append([[ipp.name,  ipp.county, ipp.ppid, ipp.iscity, ipp.guardian, ipp.phone], ipp.id, ipp.ppid])
    else:
        curpp[0][0][0] = "没有登记"

    return render_to_response('applylist.html', {'curpp': curpp, 'curppname':curppname})
    # return mentalselect(request, curname="", curppid="", curcounty=county)