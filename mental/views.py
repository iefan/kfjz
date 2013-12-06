#coding=utf8
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required  
import datetime
from forms import MentalForm, MentalForm2, ApprovalForm, ApprovalForm2, ApplyForm, InHospitalForm, OutHospitalForm, CalcHospitalForm, ApprovalOverForm
from models import MentalModel, ApprovalModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #增加分页功能
from decimal import getcontext, Decimal as D, ROUND_UP
getcontext().prec = 28
getcontext().rounding = ROUND_UP

from django.contrib.auth.views import login
def myuser_login(request, *args, **kwargs):
    if request.method == 'POST':
        request.session.set_expiry(600) #设置 cookie 时间 10 分钟
        # if not request.POST.get('remember', None):
        #     request.session.set_expiry(0)
 
    return login(request, *args, **kwargs)

@login_required(login_url="/login/")
def about(request):
    # print request.COOKIES, type(request.COOKIES)
    user = request.user
    print user.unitgroup
    return render_to_response('about.html', {'hellotxt':'hello world',}, context_instance=RequestContext(request))

def mentalinput(request):
    # print request.user
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
            # ApprovalModel.objects.get(mental__ppid=ipp.ppid, enterfiledate="否")
            curpp.append([[ipp.name,  ipp.county, ipp.ppid, ipp.iscity, ipp.guardian, ipp.phone], ipp.id, ipp.ppid])
    else:
        curpp[0][0][0] = "没有记录"

    #===========分页================
    paginator = Paginator(curpp, 3) # Show 3 contacts per page
    page = request.GET.get('page')
    try:
        curlistinfo = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        curlistinfo = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        curlistinfo = paginator.page(paginator.num_pages)
    #===========分页================

    return render_to_response('mentalselect.html', {'curpp': curlistinfo, 'curppname':curppname}, context_instance=RequestContext(request))

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

def approvallistover(request, curcounty="", curover=""):
    '''已经结算人员信息列表'''
    curppname = [u"姓名", u"区县", u"身份证号", u"户口类别",  u"医院", u"医院结算日期", u"核结", u"核结日期"]
    curpp     = [[["","","","","", ""], "","",]]

    if request.method == 'POST':
        if curover!="" or curcounty!= "":
            pass
        else:
            curcounty = request.POST['county']
            curover = request.POST['iscalchospital']

    #只查询已经结算的人员信息
    if curover == "":
        cur_re = ApprovalModel.objects.filter( dateclose__isnull=False, mental__county__icontains=curcounty)
    else:
        cur_re  = ApprovalModel.objects.filter( dateclose__isnull=False,enterfiledate__isnull = bool(int(curover)), mental__county__icontains=curcounty)

    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            if not ipp.enterfiledate: #没有核结
                curpp.append([[ipp.mental.name, ipp.mental.county, ipp.mental.ppid, ipp.mental.iscity, ipp.hospital, ipp.dateclose], ipp.id, ""])
            else: #已经核结                
                curpp.append([[ipp.mental.name,  ipp.mental.county, ipp.mental.ppid, ipp.mental.iscity, ipp.hospital, ipp.dateclose], "", ipp.enterfiledate])
    else:
        curpp[0][0][0] = "没有记录"

    return render_to_response('approvallistover.html', {'curpp': curpp, 'curppname':curppname})

def approvalover(request, curid="0"):
    if curid == "0":
        return HttpResponseRedirect('/approvallistover/')

    # 检查当前id是否已经归档
    try:
        curpp = ApprovalModel.objects.get(enterfiledate__isnull=True, id=curid)
    except ApprovalModel.DoesNotExist:
        return HttpResponseRedirect('/approvallistover/')

    nomodifyinfo = [u"申批编号：%s"  % curpp.approvalsn, u"姓名：%s"  % curpp.mental.name, \
    u"身份证号：%s" % curpp.mental.ppid, u"区县：%s" % curpp.mental.county,]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    form = ApprovalOverForm(instance=curpp)
    if request.method == "POST":
        form = ApprovalOverForm(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return approvallistover(request, curpp.mental.county, '')

    return render_to_response('approvalover.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max})

def approvallist(request, curcounty="", curapproval=""):
    '''批准列表'''
    curppname = [u"姓名", u"区县", u"身份证号", u"户口类别", u"监护人", u"联系电话", u"修改/入院", u"批准"]
    curpp     = [[["","","","","",""], "", "",]]

    if request.method == 'POST':
        if curapproval!="" or curcounty!= "":
            pass
        else:
            curcounty = request.POST['county']
            curapproval = request.POST['isapproval']

    # 只显示未归档人员
    if curapproval == "":
        cur_re = ApprovalModel.objects.filter(enterfiledate__isnull=True, mental__county__icontains=curcounty)
    else:
        cur_re  = ApprovalModel.objects.filter(enterfiledate__isnull=True, approvalsn__isnull = bool(int(curapproval)), mental__county=curcounty)

    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            if not ipp.approvalsn:
                curpp.append([[ipp.mental.name, ipp.mental.county, ipp.mental.ppid, ipp.mental.iscity, ipp.mental.guardian, ipp.mental.phone], "", ipp.mental.ppid])
            else:
                tmpitem = ipp.id
                if ipp.indate and not ipp.outdate: #已入院
                    tmpitem = "--"
                elif ipp.outdate:
                    tmpitem = "over"
                curpp.append([[ipp.mental.name,  ipp.mental.county, ipp.mental.ppid, ipp.mental.iscity, ipp.mental.guardian, ipp.mental.phone], tmpitem, '--'])
    else:
        curpp[0][0][0] = "没有记录"

    return render_to_response('approvallist.html', {'curpp': curpp, 'curppname':curppname})

def approvalinput(request, curppid=""):
    '''批准视图'''

    # 如果为空，则跳转到所有申请表中
    if curppid == "":
        return HttpResponseRedirect('/approvallist/')

    # 如果已经申批，则跳转
    # 如果当前批准列表中不存在该ppid，则跳转
    try:
        curpp = ApprovalModel.objects.get(enterfiledate__isnull=True, approvalsn__isnull=True, mental__ppid=curppid)
    except ApprovalModel.DoesNotExist:
        return HttpResponseRedirect('/approvallist/')

    curppall = ApprovalModel.objects.filter(mental__ppid=curppid)
    curpp.savetimes = len(curppall)  #救助次数

    nomodifyinfo = [u"姓名：%s"  % curpp.mental.name, u"身份证号：%s" % curpp.mental.ppid]

    today   = datetime.date.today()

    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    curpp.notifystart = today
    curpp.notifyend   = today + datetime.timedelta(60)
    curpp.approvaldate = today
    curpp.approvalsn = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    curpp.isapproval = u"同意"
    form = ApprovalForm(instance=curpp)
    if request.method == "POST":
        if request.POST['period'] == u"急性":
            curpp.daysfoodlimit = 60
        else:
            curpp.daysfoodlimit = 90

        form = ApprovalForm(request.POST, instance=curpp)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/approvallist/') # Redirect
    return render_to_response('approvalinput.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max})

def approvalmodify(request, curid="0"):
    if curid == "0":
        return HttpResponseRedirect('/approvallist/')

    # 只能修改未入院的人员信息
    try:
        curpp = ApprovalModel.objects.get(indate__isnull=True, id=curid)
    except ApprovalModel.DoesNotExist:
        return HttpResponseRedirect('/approvallist/')

    nomodifyinfo = [u"申批编号：%s"  % curpp.approvalsn, u"姓名：%s"  % curpp.mental.name, \
    u"身份证号：%s" % curpp.mental.ppid, u"区县：%s" % curpp.mental.county,]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    form = ApprovalForm2(instance=curpp)
    if request.method == "POST":
        if request.POST['period'] == u"急性":
            curpp.daysfoodlimit = 60
        else:
            curpp.daysfoodlimit = 90

        form = ApprovalForm2(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return approvallist(request, curpp.mental.county, '')

    return render_to_response('approvalmodify.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max})

def applyinput(request, curppid="111456789000"):
    '''申请求助视图'''
    if curppid == "":
        return HttpResponseRedirect('/applylist/')

    # 如果已经申请，则跳转
    try:
        ApprovalModel.objects.get(approvalsn__isnull=True, mental__ppid=curppid)
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

    curppname = [u"姓名", u"区县", u"身份证号", u"户口类别", u"监护人", u"联系电话", u"修改", u"申请求助",u"申核情况"]
    curpp     = [[["","","","","",""], "", "", "",]]

    if request.method == 'POST':
        if curname!="" or curppid!= "":
            pass
        else:
            curname = request.POST['name']
            curppid = request.POST['ppid']

    cur_re = MentalModel.objects.filter(name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty)
    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            try:
                #只查询未出院的人员
                overpp = ApprovalModel.objects.get(outdate__isnull=True, mental__ppid=ipp.ppid, enterfiledate__isnull=True,)
                if overpp.isapproval == u"同意":
                    curpp.append([[ipp.name,  ipp.county, ipp.ppid, ipp.iscity, ipp.guardian, ipp.phone], "", '--', overpp.isapproval])
                else:
                    curpp.append([[ipp.name,  ipp.county, ipp.ppid, ipp.iscity, ipp.guardian, ipp.phone], ipp.id, '--', overpp.isapproval])
            except ApprovalModel.DoesNotExist:
                curpp.append([[ipp.name,  ipp.county, ipp.ppid, ipp.iscity, ipp.guardian, ipp.phone], "", ipp.ppid, ""])
    else:
        curpp[0][0][0] = "没有记录"

    return render_to_response('applylist.html', {'curpp': curpp, 'curppname':curppname})
    # return mentalselect(request, curname="", curppid="", curcounty=county)

def applymodify(request, curppid="0"):
    if curppid == "0":
        return HttpResponseRedirect('/applylist/')

    # 如果还没有申请，则不存在修改的问题，直接跳转到申请列表
    # 只能修改未经批准的申请
    try:
        curpp = ApprovalModel.objects.get(approvalsn__isnull=True, mental__id=curppid)
    except ApprovalModel.DoesNotExist:
        return HttpResponseRedirect('/applylist/')

    nomodifyinfo = [u"申请人姓名：%s"  % curpp.mental.name, \
    u"身份证号：%s" % curpp.mental.ppid, u"经济状况：%s" % curpp.mental.economic,]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    form = ApplyForm(instance=curpp)
    if request.method == "POST":
        form = ApplyForm(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return applylist(request, curpp.mental.name, curpp.mental.ppid)

    return render_to_response('applymodify.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max})

def hospitallist(request, curcounty="", curinhospital=""):
    '''医院信息列表'''
    curppname = [u"姓名", u"区县", u"有效起始时间", u"有效终止时间", u"救助疗程", u"审核时间", u"确认入院", u"入院时间",]
    curpp     = [[["","","","","",""], "", "",]]

    if request.method == 'POST':
        if curcounty!="" or curinhospital!= "":
            pass
        else:
            curcounty = request.POST['county']
            curinhospital = request.POST['inhospital']

    # 不显示归档人员
    if curinhospital == "":
        cur_re = ApprovalModel.objects.filter(enterfiledate__isnull=True, mental__county__icontains=curcounty)
    else:
        cur_re  = ApprovalModel.objects.filter(enterfiledate__isnull=True, indate__isnull = bool(int(curinhospital)), mental__county__icontains=curcounty)

    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            # print ipp.indate, ipp.approvalsn, '=================='
            if ipp.approvalsn:
                # print ipp.indate, ipp.approvalsn
                if not ipp.indate:
                    curpp.append([[ipp.mental.name, ipp.mental.county, ipp.notifystart, ipp.notifyend, ipp.period, ipp.approvaldate], ipp.id, "",])
                else:
                    if not ipp.outdate:
                        curpp.append([[ipp.mental.name, ipp.mental.county, ipp.notifystart, ipp.notifyend, ipp.period, ipp.approvaldate], '', ipp.indate, ])
                    else:
                        curpp.append([[ipp.mental.name, ipp.mental.county, ipp.notifystart, ipp.notifyend, ipp.period, ipp.approvaldate], 'over', "", ])

    else:
        curpp[0][0][0] = "没有记录"

    return render_to_response('hospitallist.html', {'curpp': curpp, 'curppname':curppname})

def inhospital(request, curid="1"):
    '''医院入院视图'''
    if curid == "":
        return HttpResponseRedirect('/hospitallist/')

    # 如果已经入院，则跳转
    try:
        ApprovalModel.objects.get(indate__isnull=False, id=curid)
        return HttpResponseRedirect('/hospitallist/')
    except ApprovalModel.DoesNotExist:
        pass

    # 如果信息总表中不存在,即可能用户手动输入urls使得id不存在，则跳转
    try:
        curpp = ApprovalModel.objects.get(enterfiledate__isnull=True, indate__isnull=True, id=curid)
    except MentalModel.DoesNotExist:
        return HttpResponseRedirect('/hospitallist/')

    nomodifyinfo = [u"审批号：%s"  % curpp.approvalsn,u"姓名：%s"  % curpp.mental.name, u"区县：%s" % curpp.mental.county]

    today   = datetime.date.today()
    jscal_min = int((today - datetime.timedelta(15)).isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(15)).isoformat().replace('-', ''))

    curpp.indate = today
    form = InHospitalForm(instance=curpp)    
    # form = InHospitalForm(initial={'mental':curpp})
    # print form
    if request.method == "POST":
        curpp.saveok = u"已确认"
        form = InHospitalForm(request.POST, instance=curpp)        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hospitallist/') # Redirect
    return render_to_response('hospitalin.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max})

def hospitallistout(request, curcounty="", curouthospital=""):
    '''已经入院人员信息列表'''
    curppname = [u"姓名", u"区县",  u"救助疗程", u"入院时间", u"确认出院",u"出院时间",]
    curpp     = [[["","","","",], "", "",]]

    if request.method == 'POST':
        if curcounty!="" or curouthospital!= "":
            pass
        else:
            curcounty = request.POST['county']
            curouthospital = request.POST['outhospital']

    if curouthospital == "": #查询已经入院人员，不显示归档人员
        cur_re = ApprovalModel.objects.filter(enterfiledate__isnull=True, indate__isnull=False, mental__county__icontains=curcounty)
    else:
        cur_re  = ApprovalModel.objects.filter(enterfiledate__isnull=True, indate__isnull=False, outdate__isnull = bool(int(curouthospital)), mental__county__icontains=curcounty)

    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            # print ipp.indate, ipp.approvalsn, '=================='
            if ipp.approvalsn:
                # print ipp.indate, ipp.approvalsn
                if not ipp.outdate:
                    curpp.append([[ipp.mental.name, ipp.mental.county, ipp.period, ipp.indate], ipp.id, "",])
                else:
                    curpp.append([[ipp.mental.name, ipp.mental.county, ipp.period, ipp.indate], 'over', ipp.outdate, ])
    else:
        curpp[0][0][0] = "没有记录"

    return render_to_response('hospitallistout.html', {'curpp': curpp, 'curppname':curppname})

def outhospital(request, curid="1"):
    '''医院出院视图'''
    if curid == "":
        return HttpResponseRedirect('/hospitallistout/')

    # 如果已经出院，则跳转
    try:
        ApprovalModel.objects.get(outdate__isnull=False, id=curid)
        return HttpResponseRedirect('/hospitallistout/')
    except ApprovalModel.DoesNotExist:
        pass

    # 如果信息总表中不存在,即可能用户手动输入urls使得id不存在，则跳转，不显示已经归档人员
    try:
        curpp = ApprovalModel.objects.get(enterfiledate__isnull=True, outdate__isnull=True, id=curid)
    except MentalModel.DoesNotExist:
        return HttpResponseRedirect('/hospitallistout/')

    nomodifyinfo = [u"审批号：%s"  % curpp.approvalsn,u"姓名：%s"  % curpp.mental.name, \
        u"区县：%s" % curpp.mental.county, u"入院时间：%s" % curpp.indate]

    today   = datetime.date.today()
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))
    jscal_min = int(today.isoformat().replace('-', ''))

    curpp.outdate = today
    form = OutHospitalForm(instance=curpp)  
    # print form
    if request.method == "POST":
        form = OutHospitalForm(request.POST, instance=curpp)        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hospitallistout/') # Redirect
    return render_to_response('hospitalout.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max})

def hospitallistcalc(request, curcounty="", curcalchospital=""):
    '''已经出院待结算人员信息列表'''
    curppname = [u"姓名", u"区县",  u"救助疗程", u"出院时间", u"住院总费用", u"修改",u"结算",]
    curpp     = [[["","","","","",], "", "",]]

    if request.method == 'POST':
        if curcounty!="" or curcalchospital!= "":
            pass
        else:
            curcounty = request.POST['county']
            curcalchospital = request.POST['calchospital']

    if curcalchospital == "": #查询已经出院，但是没有核结的人员
        cur_re = ApprovalModel.objects.filter(enterfiledate__isnull=True, outdate__isnull=False, mental__county__icontains=curcounty)
    else:
        cur_re  = ApprovalModel.objects.filter(enterfiledate__isnull=True,outdate__isnull=False, dateclose__isnull = bool(int(curcalchospital)), mental__county__icontains=curcounty)

    if len(cur_re) != 0:
        curpp = []
        for ipp in cur_re:
            if ipp.approvalsn:
                print ipp.dateclose
                if not ipp.dateclose: #对没有结算的人员显示结算按钮，以便进行结算
                    curpp.append([[ipp.mental.name, ipp.mental.county, ipp.period, ipp.outdate, ipp.moneytotal,],  "",ipp.id,])
                else:
                    if not ipp.enterfiledate:
                        curpp.append([[ipp.mental.name, ipp.mental.county, ipp.period, ipp.outdate, ipp.moneytotal,], ipp.id, "", ])
                    else:
                        curpp.append([[ipp.mental.name, ipp.mental.county, ipp.period, ipp.outdate, ipp.moneytotal,], '', "over", ])
    else:
        curpp[0][0][0] = "没有记录"

    return render_to_response('hospitallistcalc.html', {'curpp': curpp, 'curppname':curppname})

def calchospital(request, curid="1"):
    '''医院结算视图'''
    if curid == "":
        return HttpResponseRedirect('/hospitallistcalc/')

    # 如果已经结算，则跳转
    try:
        ApprovalModel.objects.get(dateclose__isnull=False, id=curid)
        return HttpResponseRedirect('/hospitallistcalc/')
    except ApprovalModel.DoesNotExist:
        pass

    # 如果信息总表中不存在,即可能用户手动输入urls使得id不存在，则跳转
    try:
        curpp = ApprovalModel.objects.get(dateclose__isnull=True, id=curid)
    except MentalModel.DoesNotExist:
        return HttpResponseRedirect('/hospitallistcalc/')

    nomodifyinfo = [u"审批号：%s"  % curpp.approvalsn,u"姓名：%s"  % curpp.mental.name, \
        u"区县：%s" % curpp.mental.county, u"入院时间：%s" % curpp.indate]

    today   = datetime.date.today()
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))
    jscal_min = int(today.isoformat().replace('-', ''))

    curpp.dayshosp = (curpp.outdate-curpp.indate).days  # 实际住院天数
    if curpp.period == u"急性":
        totallimit = 60
        savelevel = 64 #急性64/天，慢性57/天
    else:
        totallimit = 90
        savelevel = 57 #急性64/天，慢性57/天

    curpp.savelevel = savelevel #设定救助标准
    curpp.foodlevel = 14        #设定伙食标准
    if curpp.dayshosp < totallimit:
        curpp.dayssave = curpp.dayshosp                     # 救助天数
        curpp.daysfood = curpp.dayshosp + 1                 # 伙食天数
    else:
        curpp.dayssave = totallimit
        curpp.daysfood = totallimit

    # 计算部分费用
    curpp.moneyhospital  = D(curpp.savelevel * curpp.dayssave).quantize(D('.01'))  #医疗救助费用
    curpp.moneyfood      = D(curpp.daysfood * curpp.foodlevel).quantize(D('.01')) #伙食费用
    if curpp.moneyhospital >= 1000:
        curpp.moneyfrom = D(1000).quantize(D('.01')) #民政补助费用
    else:
        curpp.moneyfrom = D(0).quantize(D('.01')) #民政补助费用

    curpp.dateclose = today
    form = CalcHospitalForm(instance=curpp)  
    # print form
    if request.method == "POST":
        form = CalcHospitalForm(request.POST, instance=curpp)        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hospitallistcalc/') # Redirect
    return render_to_response('hospitalcalc.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max})

def calmodifychospital(request, curid="1"):
    '''医院结算修改视图'''
    if curid == "":
        return HttpResponseRedirect('/hospitallistcalc/')

    # 如果已经核结，则跳转
    try:
        ApprovalModel.objects.get(enterfiledate__isnull=False, id=curid)
        return HttpResponseRedirect('/hospitallistcalc/')
    except ApprovalModel.DoesNotExist:
        pass

    # 如果信息总表中不存在，查询表中id存在并且未结算的人员, 不存在，则跳转
    try:
        curpp = ApprovalModel.objects.get(enterfiledate__isnull=True, id=curid)
    except MentalModel.DoesNotExist:
        return HttpResponseRedirect('/hospitallistcalc/')

    nomodifyinfo = [u"审批号：%s"  % curpp.approvalsn,u"姓名：%s"  % curpp.mental.name, \
        u"区县：%s" % curpp.mental.county, u"结算时间：%s" % curpp.dateclose]

    today   = datetime.date.today()
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))
    jscal_min = int(today.isoformat().replace('-', ''))

    curpp.dayshosp = (curpp.outdate-curpp.indate).days  # 实际住院天数
    if curpp.period == u"急性":
        totallimit = 60
        savelevel = 64 #急性64/天，慢性57/天
    else:
        totallimit = 90
        savelevel = 57 #急性64/天，慢性57/天

    curpp.savelevel = savelevel #设定救助标准
    curpp.foodlevel = 14        #设定伙食标准
    if curpp.dayshosp < totallimit:
        curpp.dayssave = curpp.dayshosp                     # 救助天数
        curpp.daysfood = curpp.dayshosp + 1                 # 伙食天数
    else:
        curpp.dayssave = totallimit
        curpp.daysfood = totallimit

    # 计算部分费用
    curpp.moneyhospital  = D(curpp.savelevel * curpp.dayssave).quantize(D('.01'))  #医疗救助费用
    curpp.moneyfood      = D(curpp.daysfood * curpp.foodlevel).quantize(D('.01')) #伙食费用
    if curpp.moneyhospital >= 1000:
        curpp.moneyfrom = D(1000).quantize(D('.01')) #民政补助费用

    curpp.dateclose = today
    form = CalcHospitalForm(instance=curpp)  
    # print form
    if request.method == "POST":
        form = CalcHospitalForm(request.POST, instance=curpp)        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hospitallistcalc/') # Redirect
    return render_to_response('hospitalcalcmodify.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max})
