#coding=utf8
from django import forms
from models import MentalModel

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
