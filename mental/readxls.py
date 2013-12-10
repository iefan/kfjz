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
        # try:
        #     n = cur.execute(sql1,tuple(tmpinfo))
        # except:
        #     print name, ppid
        #     pass

  # addr_dict = {}
    # strsql = "select addrsn,addrname from addr where right(addrsn,6)='000000'"
    # conn.query(strsql)
    # result = conn.store_result()
    # while True:
    #     record = result.fetch_row()
    #     if not record: break
    #     addr_dict[record[0][1][:2]] = record[0][0]

    # dictcou = {}
    # dictcou[1] = u"金平";
    # dictcou[2] = u"龙湖";
    # dictcou[3] = u"濠江";
    # cur = conn.cursor()
    # for years in range(2011,2014):
    #     for county in range(1,4):
    #         path = "D:\\workdb\\zulian\\" + str(years) + "\\" + str(county) + ".xls"
    #         print path, dictcou[county]

    #         bk = xlrd.open_workbook(path)
    #         sh = bk.sheets()[0]
    #         nrows =  sh.nrows
    #         for indx in range(2, nrows):
    #             name        = sh.row(indx)[0].value
    #             ppid        = sh.row(indx)[1].value
    #             sex         = sh.row(indx)[2].value
    #             cardtime    = sh.row(indx)[5].value
    #             addrsn      = addr_dict[dictcou[county]]
    #             address     = sh.row(indx)[6].value
    #             try:
    #                 phone       = sh.row(indx)[7].value
    #             except:
    #                 phone       = ''

    #             name = name.replace(' ', '')
    #             name = name.replace(u'　', '')

    #             tmpinfo = [name, ppid, sex, cardtime, addrsn, address, phone, years, '', '']
                # try:
                #     print name, ppid, sex, cardtime, addrsn, address, phone, years
                # except:
                #     print tmpinfo, '-------------------'
                #     return

                # try:
                #     n = cur.execute(sql1,tuple(tmpinfo))
                # except:
                #     print address, name
                    # pass


if __name__ == '__main__':
    readxlsex()
#    DBCTLib()
#    testdb()
