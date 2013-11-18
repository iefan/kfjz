#coding=utf8
from django import forms
from models import MentalModel, ApprovalModel
from datetime import date

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
        exclude=('name','ppid',)

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
        fields = ('approvalsn','mental','insurance','cert1_ppid','cert2_diag','cert3_poor',\
            'hospital','period','foodallow','savetimes','savecontinue','notifystart','notifyend',\
            'isapproval','approvaldate','approvalman','saveok','iscal','moneyhospital', \
            'moneyfood','moneyfrom',)
        exclude = ('indate','outdate','dayshosp','dayssave','daysfood','moneytotal','moneymedicineself',\
            'moneyselfscale','moneyself','moneyinsurance','dateclose','daysfoodlimit','savelevel','foodlevel','startlevel','commitdate','isenterfile','enterfileman',)

    def clean(self):
        return self.cleaned_data

    def clean_approvalsn(self):
        if 'approvalsn' not in self.cleaned_data.keys():
            raise forms.ValidationError("请输入申批编号")
        approvalsn = self.cleaned_data['approvalsn']
        if approvalsn == "":
            raise forms.ValidationError("请输入申批编号")

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
        fields = ('mental','insurance','cert1_ppid','cert2_diag','cert3_poor','commitdate',)
        exclude = ('hospital','period','foodallow','savetimes','savecontinue','notifystart','notifyend',\
            'isapproval','approvaldate','approvalman','saveok','iscal','moneyhospital', \
            'moneyfood','moneyfrom','isenterfile','enterfileman','approvalsn','indate','outdate','dayshosp','dayssave','daysfood','moneytotal','moneymedicineself',\
            'moneyselfscale','moneyself','moneyinsurance','dateclose','daysfoodlimit','savelevel','foodlevel','startlevel',)

    def clean(self):
        return self.cleaned_data