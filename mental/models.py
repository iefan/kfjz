#coding=utf8
from django.db import models
import resources as jzr
from datetime import date

class MentalModel(models.Model):
    name            = models.CharField(max_length=30, verbose_name="姓名")
    sex             = models.CharField(choices=jzr.SEX_CHOICES, max_length=2, verbose_name="性别", default="男")
    county          = models.CharField(choices=jzr.COUNTY_CHOICES, max_length=30, verbose_name="区县", default="金平区")
    ppid            = models.CharField(unique=True, max_length=30, verbose_name="身份证号")
    dislevel        = models.CharField(choices=jzr.DISLEVEL_CHOICES, max_length=30, verbose_name="残疾类别", default="61")
    certtime        = models.DateField(verbose_name="办证时间", blank=True, null=True, )
    economic        = models.CharField(choices=jzr.ECON_CHOICES, max_length=10, verbose_name="经济状况", default="低保")
    iscity          = models.CharField(choices=jzr.CITY_CHOICE, max_length=10, verbose_name="户口类别", default="非农")
    address         = models.CharField(max_length=100, verbose_name="住址", blank=True, null=True, )
    guardian        = models.CharField(max_length=20, verbose_name="监护人")
    guardrelation   = models.CharField(choices=jzr.RELASHIP_CHOICES, max_length=10, verbose_name="监护关系",default="其他")
    phone           = models.CharField(max_length=20, verbose_name="固定电话",blank=True, null=True,)
    phone2          = models.CharField(max_length=20, verbose_name="手机",blank=True, null=True,)
    regtime         = models.DateField(verbose_name="建档时间",blank=True, null=True,)
    operatorname    = models.CharField(max_length=30, verbose_name='录入人员', blank=True, null=True,)

    class Meta:
        ordering = ['county',]
        verbose_name = "精神病人信息"  
        verbose_name_plural = "精神病人信息"  
        # app_label = u"信息管理"

    def __unicode__(self):
        return u"%s %s %s %s %s %s" % (self.county, self.name, self.dislevel, \
            self.economic, self.iscity, self.certtime,)

class ApprovalModel(models.Model):
    approvalsn      = models.CharField(max_length=30, verbose_name="审批编号", unique=True,blank=True, null=True,) # NEED AUTO GENERATE
    mental          = models.ForeignKey('MentalModel', verbose_name="病人信息")    
    cert1_ppid      = models.CharField(max_length=30,verbose_name="身份证明", choices=jzr.CERT1_CHOICES,default="身份证")       
    cert2_diag      = models.CharField(max_length=30,verbose_name="疾病证明", choices=jzr.CERT2_CHOICES, default="精神残疾证")
    cert3_poor      = models.CharField(max_length=30,verbose_name="贫困证明", choices=jzr.CERT3_CHOICES,default="低保证")
    applyman        = models.CharField(max_length=30, verbose_name="申请人员", blank=True, null=True,)

    hospital        = models.CharField(max_length=30,verbose_name="医疗机构", choices=jzr.HOSPITAL_CHOICES, default="市四本部",)
    period          = models.CharField(max_length=30,verbose_name="救助疗程", choices=jzr.PERIOD_CHOICES, default="急性",)
    foodallow       = models.CharField(max_length=30,verbose_name="伙食补助", choices=jzr.YESNO_CHOICE, default="否")
    savetimes       = models.IntegerField(verbose_name="救助次数", default=0)
    savecontinue    = models.CharField(max_length=30,verbose_name="续院类型", blank=True, null=True,choices=jzr.CONTINUE_CHOICES,)
    notifystart     = models.DateField(verbose_name="有效起始时间", blank=True, null=True,)
    notifyend       = models.DateField(verbose_name="有效终止时间", blank=True, null=True,)
    commitdate      = models.DateField(verbose_name="提交申核时间", blank=True, null=True, default=date.today)
    isapproval      = models.CharField(max_length=30,verbose_name="残联审核", choices=jzr.ISAPPROVAL_CHOICES, default="待审",)
    approvaldate    = models.DateField(verbose_name="审核时间", blank=True, null=True)
    approvalman     = models.CharField(max_length=30, verbose_name="审核人员", blank=True, null=True,)

    # 结算及归档
    # iscal           = models.CharField(max_length=30,verbose_name="是否结算", choices=jzr.ISCAL_CHOICES, blank=True,null=True,)
    enterfiledate   = models.DateField(verbose_name="核结日期", blank=True, null=True,)
    enterfileman    = models.CharField(max_length=30, verbose_name="核结管理员", blank=True, null=True,)

    # hospital write
    indate          = models.DateField(verbose_name="住院时间", blank=True, null=True,)
    saveok          = models.CharField(max_length=30,verbose_name="救助确认", choices=jzr.SAVEOK_CHOICES, blank=True,null=True,)
    inhospitalman   = models.CharField(max_length=30, verbose_name="入院确认人", blank=True, null=True,)

    outdate         = models.DateField(verbose_name="出院时间", blank=True, null=True,)
    outhospitalman  = models.CharField(max_length=30, verbose_name="出院确认人", blank=True, null=True,)
    
    dayshosp        = models.IntegerField(verbose_name="住院天数", blank=True, null=True,)  #auto calc
    dayssave        = models.IntegerField(verbose_name="救助天数", blank=True, null=True,)  #auto calc  
    daysfood        = models.IntegerField(verbose_name="伙食天数", blank=True, null=True,)  #auto calc
    moneytotal      = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="住院总费用", blank=True, null=True,)
    moneymedicineself= models.DecimalField(max_digits=6, decimal_places=2, verbose_name="自费药金额", blank=True, null=True,)
    moneyselfscale  = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="自付比例", blank=True, null=True,)
    moneyself       = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="个人支付", blank=True, null=True,)
    moneyinsurance  = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="医保支付", blank=True, null=True,) 
    insurance       = models.CharField(max_length=30,verbose_name="医保类别", choices=jzr.INSU_CHOICES, default="城乡医保",)

    # 在医院结算是自动根据设定标准进行计算
    moneyhospital   = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="医疗救助费用", blank=True, null=True,)  #经结算应救助的金额=救助天数*救助标准
    moneyfood       = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="伙食费用", blank=True, null=True,)    #=补助天数*补助标准
    moneyfrom       = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="民政补助", blank=True, null=True,)    #医疗费救助金额大于1000元的显示1000
   
    dateclose       = models.DateField(verbose_name="结算日期", blank=True, null=True,)
    datecloseman    = models.CharField(max_length=30, verbose_name="结算人", blank=True, null=True,)

    # level set
    daysfoodlimit   = models.IntegerField(verbose_name="救助上限", blank=True, null=True,)
    savelevel       = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="救助标准", blank=True, null=True,) #急性64/天，慢性57/天
    foodlevel       = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="伙食标准", blank=True, null=True,) #伙食14天
    startlevel      = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="起付标准", blank=True, null=True,)

    class Meta:
        # ordering = ['ppid',]
        verbose_name = "审批信息"  
        verbose_name_plural = "审批信息"  
        # app_label = u"信息管理"

    def __unicode__(self):
        return u"%s %s" % (self.approvalsn, self.mental, )