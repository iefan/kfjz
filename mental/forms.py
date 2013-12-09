#coding=utf8
import resources as jzr
from django import forms
from models import MentalModel, ApprovalModel
# from datetime import date

class MentalForm(forms.ModelForm):
    certtime   = forms.CharField(error_messages={'required':u'日期不能为空'}, label='办证时间', \
        widget= forms.TextInput())
    
    class Meta:
        model=MentalModel
        fields = ('name','sex','county','ppid','dislevel','certtime','economic','iscity',\
            'address','guardian','guardrelation','phone','regtime','operatorname',)
        # exclude=('isagree',)

    def clean(self):
        return self.cleaned_data

    def clean_ppid(self):
        ppid   = self.cleaned_data['ppid']
        curpp = MentalModel.objects.filter(ppid=ppid)
        if len(curpp) != 0:
            raise forms.ValidationError("该身份证号码已录入当前系统！")
        else:
            pass
        return ppid

    def clean_phone(self):
        phone  = self.cleaned_data['phone']

        if not phone.isdigit() or len(phone)<11 or len(phone) > 12:
            raise forms.ValidationError("请输入11或12位电话号码")

        curpp = MentalModel.objects.filter(phone=phone)
        if len(curpp) != 0:
            raise forms.ValidationError("该电话在当前系统已经存在！")
        else:
            pass

        return phone

class MentalForm2(forms.ModelForm):
    certtime   = forms.CharField(error_messages={'required':u'日期不能为空'}, label='办证时间', \
        widget= forms.TextInput())
    
    class Meta:
        model=MentalModel
        fields = ('name','sex','county','ppid','dislevel','certtime','economic','iscity',\
            'address','guardian','guardrelation','phone','regtime','operatorname',)
        # exclude=('name','ppid',)

    def clean(self):
        return self.cleaned_data

    def clean_ppid(self):
        ppid   = self.cleaned_data['ppid']        
        return ppid

    def clean_phone(self):
        phone  = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone)<11 or len(phone) > 12:
            raise forms.ValidationError("请输入11或12位电话号码")
        return phone

class ApprovalForm(forms.ModelForm):
    """申批表"""
    mental = forms.ModelChoiceField(queryset=MentalModel.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = ApprovalModel
        fields = ('approvalsn','mental',\
            'hospital','period','foodallow','savetimes','savecontinue','notifystart','notifyend',\
            'isapproval','approvaldate','approvalman',)
       
    def clean(self):
        return self.cleaned_data

    def clean_approvalsn(self):
        if 'approvalsn' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入申批编号")
        approvalsn = self.cleaned_data['approvalsn']
        try:
            ApprovalModel.objects.get(approvalsn=approvalsn)
            raise forms.ValidationError("所输入的申批编号已经存在")
        except ApprovalModel.DoesNotExist:
            pass

        if approvalsn == "":
            raise forms.ValidationError("请输入申批编号")
        return approvalsn

    def clean_notifystart(self):
        if 'notifystart' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入起始日期")
        notifystart = self.cleaned_data['notifystart']
        if notifystart is None:
            raise forms.ValidationError("请输入起始日期")
        return notifystart

    def clean_notifyend(self):
        if 'notifyend' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入起始日期")
        notifyend = self.cleaned_data['notifyend']
        if notifyend is None:
            raise forms.ValidationError("请输入起始日期")
        return notifyend

class ApprovalForm2(forms.ModelForm):
    """申批表"""
    mental = forms.ModelChoiceField(queryset=MentalModel.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = ApprovalModel
        fields = ('mental',\
            'hospital','period','foodallow','savetimes','savecontinue','notifystart','notifyend',\
            'isapproval','approvaldate','approvalman',)
      
    def clean(self):
        return self.cleaned_data

    def clean_approvalsn(self):
        if 'approvalsn' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入申批编号")
        approvalsn = self.cleaned_data['approvalsn']
        try:
            ApprovalModel.objects.get(approvalsn=approvalsn)
            raise forms.ValidationError("所输入的申批编号已经存在")
        except ApprovalModel.DoesNotExist:
            pass

        if approvalsn == "":
            raise forms.ValidationError("请输入申批编号")
        return approvalsn

    def clean_notifystart(self):
        if 'notifystart' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入起始日期")
        notifystart = self.cleaned_data['notifystart']
        if notifystart is None:
            raise forms.ValidationError("请输入起始日期")
        return notifystart

    def clean_notifyend(self):
        if 'notifyend' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入起始日期")
        notifyend = self.cleaned_data['notifyend']
        if notifyend is None:
            raise forms.ValidationError("请输入起始日期")
        return notifyend

class ApplyForm(forms.ModelForm):
    """申请表"""
    mental = forms.ModelChoiceField(queryset=MentalModel.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = ApprovalModel
        fields = ('mental','insurance','cert1_ppid','cert2_diag','cert3_poor','commitdate','applyman', )
       
    def clean(self):
        return self.cleaned_data

class InHospitalForm(forms.ModelForm):
    """入院表"""
    mental = forms.ModelChoiceField(queryset=MentalModel.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = ApprovalModel
        fields = ('mental',"indate","inhospitalman",)
        
    def clean(self):
        return self.cleaned_data

    def clean_indate(self):
        if 'indate' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入入院日期")
        indate = self.cleaned_data['indate']
        if indate is None:
            raise forms.ValidationError("请输入入院日期")
        return indate

class OutHospitalForm(forms.ModelForm):
    """出院表"""
    mental = forms.ModelChoiceField(queryset=MentalModel.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = ApprovalModel
        fields = ('mental',"outdate","outhospitalman",)
      
    def clean(self):
        return self.cleaned_data

    def clean_outdate(self):
        if 'outdate' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入出院日期")
        outdate = self.cleaned_data['outdate']
        if outdate is None:
            raise forms.ValidationError("请输入出院日期")
        return outdate

class CalcHospitalForm(forms.ModelForm):
    """出院结算表"""
    mental = forms.ModelChoiceField(queryset=MentalModel.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = ApprovalModel
        fields = ('mental',"moneyhospital","moneyfood","moneyfrom","dayshosp","dayssave","daysfood",\
            "moneytotal","moneymedicineself","moneyinsurance","moneyself","moneyselfscale","startlevel",\
            "dateclose","datecloseman",)

    def clean(self):
        return self.cleaned_data

    def clean_dateclose(self):
        if 'dateclose' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入结算日期")
        dateclose = self.cleaned_data['dateclose']
        if dateclose is None:
            raise forms.ValidationError("请输入结算日期")
        return dateclose

class ApprovalOverForm(forms.ModelForm):
    """出院结算表"""
    mental = forms.ModelChoiceField(queryset=MentalModel.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = ApprovalModel
        fields = ('mental',"enterfiledate","enterfileman",)

    def clean(self):
        return self.cleaned_data

    def clean_dateclose(self):
        if 'dateclose' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入结算日期")
        dateclose = self.cleaned_data['dateclose']
        if dateclose is None:
            raise forms.ValidationError("请输入结算日期")
        return dateclose

class SelectMentalForm(forms.ModelForm):
    '''精神病救助查询条件表单'''
    lstcounty = list(jzr.COUNTY_CHOICES)
    lstcounty.insert(0, ("", "--"))
    county = forms.ChoiceField(choices = tuple(lstcounty), label="区县名称",)
    class Meta:
        model = MentalModel
        fields = ('name', 'ppid', 'county',)

    def clean(self):
        return self.cleaned_data
