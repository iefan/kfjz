#coding=utf8
def _getOutCell(outSheet, colIndex, rowIndex):
    """ HACK: Extract the internal xlwt cell representation. """
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row: return None

    cell = row._Row__cells.get(colIndex)
    return cell

def setOutCell(outSheet, col, row, value):
    """ Change cell value without changing formatting. """
    # HACK to retain cell style.
    previousCell = _getOutCell(outSheet, col, row)
    # END HACK, PART I

    outSheet.write(row, col, value)

    # HACK, PART II
    if previousCell:
        newCell = _getOutCell(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx

# !!!===!!! MUST NEED ADD 'u' BEFORE IN UNICODE ! ===!!!
COUNTY_CHOICES = (\
    (u'金平区', u'金平区'),
    (u'龙湖区', u'龙湖区'),
    (u'濠江区', u'濠江区'),
    (u'澄海区', u'澄海区'),
    (u'潮阳区', u'潮阳区'),
    (u'潮南区', u'潮南区'),
    (u'南澳县', u'南澳县'),
    )
SEX_CHOICES = (\
    (u'男', u'男'),
    (u'女', u'女'),
    )
ECON_CHOICES = (\
    (u'低保', u'低保'),
    (u'五保', u'五保'),
    (u'特困', u'特困'),
    (u'困难', u'困难'),
    )
CITY_CHOICE = (\
    (u'非农', u'非农'), 
    (u'农村', u'农村'),
    )
RELASHIP_CHOICES = (\
    (u'配偶',u'配偶'),
    (u'子女',u'子女'),
    (u'孙子女',u'孙子女'),
    (u'父母',u'父母'),
    (u'祖父母',u'祖父母'),
    (u'兄弟姐妹',u'兄弟姐妹'),
    (u'其他',u'其他'),
    )
DISLEVEL_CHOICES = (\
    ("61", "61"),
    ("62", "62"),
    ("63", "63"),
    ("64", "64"),
    (u'其他',u'其他'),
    )
INSU_CHOICES = (\
    (u'职工医保',u'职工医保'),
    (u'城乡医保',u'城乡医保'),
    )

CERT1_CHOICES = (\
    (u'身份证',u'身份证'), 
    (u'户口本',u'户口本'),
    )
CERT2_CHOICES = (\
    (u'精神残疾证',u'精神残疾证'), 
    (u'精神障碍诊断证明',u'精神障碍诊断证明'),
    (u'非精神残疾证', u'非精神残疾证'),
    )
CERT3_CHOICES = (\
    (u'低保证',u'低保证'),
    (u'五保证',u'五保证'),
    (u'特困证',u'特困证'),
    (u'困难证明',u'困难证明'),
    )
HOSPITAL_CHOICES = (\
    (u'市四本部', u'市四本部'),
    (u'礐石', u'礐石'),
    (u'红莲池', u'红莲池'),
    (u'汕大', u'汕大'),
    )
PERIOD_CHOICES = (\
    (u'急性',u'急性'),
    (u'慢性',u'慢性'),
    )
CONTINUE_CHOICES = (\
    (u'间隔救助', u'间隔救助'),
    (u'续院救助', u'续院救助'),
    )
ISAPPROVAL_CHOICES = (\
    (u'待审', u'待审'),
    (u'退审', u'退审'),
    (u'同意', u'同意'),
    (u'作废', u'作废'),
    )
SAVEOK_CHOICES = (\
    (u'已确认', u'已确认'),
    (u'过期', u'过期'),
    )
ISCAL_CHOICES = (\
    (u'已结算',u'已结算'),
    (u'待结算',u'待结算'),
    )
YESNO_CHOICE = (\
    (u'是',u'是'),
    (u'否',u'否'),
    )
YESNO01_CHOICE = (\
    ('','--'),
    (u'0',u'是'),
    (u'1',u'否'),
    )