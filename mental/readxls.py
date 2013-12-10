#!/usr/bin/python
# -*- coding: utf-8 -*-

from  string import zfill as z
import MySQLdb
import xlrd

conn=MySQLdb.connect(host="127.0.0.1", user="root",passwd="stclbgs",db="kfjz", use_unicode=1, charset='utf8')

def readxlsex():
    path = r"/home/stcl/workdb/kfex.xls"
    print path

    bk = xlrd.open_workbook(path)
    sh = bk.sheets()[0]
    nrows =  sh.nrows
    lstrelation = []
    for indx in range(3, nrows):
        # name        = sh.row(indx)[0].value
        # ppid        = sh.row(indx)[1].value
        relation      = sh.row(indx)[11].value
        if relation not in lstrelation:
            lstrelation.append(relation)
    
    for item in lstrelation:
        print item, ',',
       
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

    #         sql1 = "insert into zcbt_info(name, ppid, sex, cardtime, addrsn, address, phone, years, demo, demotime) values(%s,%s, %s,%s, %s,%s, %s,%s,%s, %s)"
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
