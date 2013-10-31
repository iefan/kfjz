#coding=utf8
from django.db import models
import resources as jzr

class MentalModel(models.Model):
    name        = models.CharField(max_length=30, verbose_name="姓名")
    sex         = models.CharField(choices=jzr.SEX_CHOICES, max_length=2, verbose_name="性别", default="男")
    county      = models.CharField(choices=jzr.COUNTY_CHOICES, max_length=30, verbose_name="区县", default="金平区")
    ppid        = models.CharField(unique=True, max_length=30, verbose_name="身份证号")
    dislevel    = models.CharField(max_length=30, verbose_name="残疾类别", blank=True, null=True, )
    certtime    = models.DateField(verbose_name="办证时间", blank=True, null=True, )
    economic    = models.CharField(choices=jzr.ECON_CHOICES, max_length=10, verbose_name="经济状况", default="低保")
    iscity      = models.CharField(choices=jzr.CITY_CHOICE, max_length=10, verbose_name="户口类别", default="城镇")
    address     = models.CharField(max_length=100, verbose_name="住址", blank=True, null=True, )
    guardian    = models.CharField(max_length=20, verbose_name="监护人")
    guardrelation = models.CharField(choices=jzr.RELASHIP_CHOICES, blank=True, null=True,max_length=10, verbose_name="监护关系", default="父亲")
    phone       = models.CharField(max_length=20, verbose_name="联系电话",blank=True, null=True,)
    regtime     = models.DateField(verbose_name="建档时间",blank=True, null=True,)

    class Meta:
        ordering = ['county',]
        verbose_name = "精神病人信息"  
        verbose_name_plural = "精神病人信息"  
        # app_label = u"信息管理"

    def __unicode__(self):
        return u"%s %s %s %s %s %s" % (self.name, self.county, self.dislevel, \
            self.economic, self.iscity, self.certtime,)
