# Program that writes codeset values to a table in Microsoft Excel
# Used for some analysis work for CalcGuard Technologies, Inc.
# Figured it might be an example in accessing the repository.
# Jim Northey
# import pytest
from pyfixorchestra import FixDictionary
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo
fd = FixDictionary()
fd.read_xml("resource_dir/OrchestraFIXLatest.xml")

wb=openpyxl.Workbook()
ws=wb.active
ws.title="Codesets"
ws.append(["CodeSetName","CodeSetExternalID","Code","Value","Mneumonic","Description","Mapping","CodeSetSource","CodeSetVersion"])
rows=1
codesets=fd.generateDictionary("codeSets")
for codeset in codesets:
    #print(codeset)
    for codes in codeset['codes']:
        elaboration=''
        desc=''
        for text in codes['documentation']:
            if(text['purpose']=="SYNOPSIS"):
                desc=text['text']
            elif(text['purpose']=='ELABORATION'):
                elaboration=text['text']
        ws.append([codeset['name'],codeset['id'],codes['value'],desc,codes['name'],elaboration,"","FIX Trading Community","FIXLatest"])
        rows+=1
        print (codes)
codetable=Table(displayName=f"CodeSetTable", ref=f"A1:I{rows}")
style = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False,
                  showLastColumn=False, showRowStripes=True, showColumnStripes=False)
codetable.tableStyleInfo = style
ws.add_table(codetable)
wb.save("codesets.xlsx")