#!/usr/bin/python
# -*- coding: utf-8 -*-

from  string import zfill as z
import MySQLdb
import xlrd, datetime

conn=MySQLdb.connect(host="127.0.0.1", user="root",passwd="stclbgs",db="kfjz", use_unicode=1, charset='utf8')

def readxlsex():
    path = r"/home/stcl/workdb/kfex2013.xls"
    print path

    bk = xlrd.open_workbook(path)
    sh = bk.sheets()[0]
    nrows =  sh.nrows
    lstppid = []

    cur = conn.cursor()
    cur.execute('select * from mental_mentalmodel')
    print cur.fetchall()
    sql1 = "insert into mental_mentalmodel(name,sex,county,ppid,dislevel,certtime,economic,iscity,address,guardian,guardrelation,phone,phone2,regtime,operatorname) values (%s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s)"

    num = 0
    numinsert = 0
    for indx in range(4, nrows):
        name        = sh.row(indx)[3].value
        sex         = sh.row(indx)[4].value
        county      = sh.row(indx)[2].value
        ppid        = sh.row(indx)[5].value
        dislevel    = sh.row(indx)[7].value
        if dislevel == u"有":
            dislevel = u"61"
        else:
            dislevel = u"其他"
        certtime        = datetime.date(1900,1,1)
        economic        = sh.row(indx)[6].value
        iscity          = sh.row(indx)[8].value
        address         = sh.row(indx)[2].value
        guardian        = sh.row(indx)[10].value
        guardrelation   = sh.row(indx)[11].value.strip()
        if guardrelation == "":
            guardrelation = u"其他"
        try:
            phone           = str(int(sh.row(indx)[12].value))
        except:
            pass
        try:
            phone2          = str(int(sh.row(indx)[13].value))
        except:
            pass
        regtime         = datetime.date.today()
        operatorname    = u"梁维忠"
       
        tmpinfo =[name,sex,county,ppid,dislevel,certtime,economic,iscity,address,guardian,guardrelation,phone,phone2,regtime,operatorname,]
        if ppid not in lstppid:
            lstppid.append(ppid)
            try:
                numinsert += 1
                print numinsert
                # n = cur.execute(sql1,tuple(tmpinfo))
                # conn.commit()
            except:
                print name, ppid
                pass
        else:
            num += 1

        # if len(ppid)>18:
        #     # print "--",ppid
        #     if ppid not in lstppid:
        #         lstppid.append(ppid)
        #         print ppid, "++++++++++++++++++++++"
        #         num += 1
        #     else:
        #         pass
                # num += 1
            # print ppid, "already exist!!!"
    print num

def readxlsex_approval():
    path = r"/home/stcl/workdb/kfex2013.xls"
    bk = xlrd.open_workbook(path)
    sh = bk.sheets()[0]
    nrows =  sh.nrows

    cur = conn.cursor()
    sql1 = "insert into mental_approvalmodel(approvalsn,mental_id,cert1_ppid,cert2_diag,cert3_poor,applyman,hospital,period,foodallow,savetimes,savecontinue,notifystart,notifyend,commitdate,isapproval,approvaldate,approvalman) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    numinsert = 0
    for indx in range(4, nrows):
        approvalsn = "20130101000000" + z(str(int(sh.row(indx)[1].value)), 6) #20bits, yyyymmddhhmmssffffff
        ppid        = sh.row(indx)[5].value
        strsqltmp = "select * from mental_mentalmodel where ppid='" + ppid + "'"
        cur.execute(strsqltmp)
        tmpmental =  cur.fetchall()
        mental_id = tmpmental[0][0]
        cert1_ppid = u"身份证"
        discard       = sh.row(indx)[7].value
        if discard == u"有":
            cert2_diag = u"精神残疾证"
        else:
            cert2_diag = u"精神障碍诊断证明"

        cert3_poor = sh.row(indx)[6].value
        if cert3_poor == u"困难":
            cert3_poor += u"证明"
        if cert3_poor == u"特困职工":
            cert3_poor = u"特困"

        applyman = u"梁维忠"
        hospital = sh.row(indx)[15].value
        if hospital == u"四院":
            hospital = u"市四本部"
        period = sh.row(indx)[16].value
        foodallow = sh.row(indx)[19].value.strip()
        if foodallow == "":
            foodallow = u"否"

        strsqltmp2 = "select count(*) from mental_mentalmodel as m1,mental_approvalmodel as m2 where m1.ppid='" + ppid + "' and m2.mental_id=m1.id "
        cur.execute(strsqltmp2)
        savetimes = cur.fetchall()[0][0]+1

        savecontinue = ""
        isapproval = u"同意"
        demoold = sh.row(indx)[26].value.strip()
        if demoold != "":
            # print demoold, demoold[0]
            if demoold[0] == u"作":
                isapproval = u"作废"
            elif demoold[0] == u"退":
                isapproval = u"退审"
            elif demoold[0] == u"续" or demoold[0] == u"接":
                strsqltmp3 = "select m2.id from mental_mentalmodel as m1,mental_approvalmodel as m2 where m1.ppid='" + ppid + "' and m2.mental_id=m1.id "
                savecontinue = u"续院救助"
            elif demoold[0] == u"间":
                savecontinue = u"间隔救助"

        approvaldate = datetime.date(1899,12,30) + datetime.timedelta(days=int(sh.row(indx)[14].value))
        notifystart = approvaldate
        notifyend = approvaldate + datetime.timedelta(60)
        commitdate = approvaldate - datetime.timedelta(10)
        approvalman = u"梁维忠"
        tmpinfo = [approvalsn,mental_id,cert1_ppid,cert2_diag,cert3_poor,applyman,hospital,period,foodallow,savetimes,savecontinue,notifystart,notifyend,commitdate,isapproval,approvaldate,approvalman,]

        try:
            numinsert += 1
            print numinsert
            # n = cur.execute(sql1,tuple(tmpinfo))
            # conn.commit()
        except:
            print approvalsn, "========================================"
            pass

        # asql = "%s " * len(tmpinfo)
        # print asql
        # for item in tmpinfo:
        #     print item,
        # break;


# approvalsn,mental_id,cert1_ppid,cert2_diag,cert3_poor,applyman,hospital,period,foodallow,savetimes,savecontinue,notifystart,notifyend,commitdate,isapproval,approvaldate,approvalman,enterfiledate,enterfileman,indate,saveok,inhospitalman,outdate,outhospitalman,dayshosp,dayssave,daysfood,moneytotal,moneymedicineself,
# moneyselfscale,moneyself,moneyinsurance,insurance,moneyhospital,moneyfood,moneyfrom,dateclose,datecloseman,daysfoodlimit,savelevel,foodlevel,startlevel,
if __name__ == '__main__':
    # readxlsex()
    readxlsex_approval()
#    DBCTLib()
#    testdb()
