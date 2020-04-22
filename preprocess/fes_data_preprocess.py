import openpyxl
import pandas as pd

# 1) 엑셀에 저장되어있는 축제 이름 통일
def fes_name():
    xlsxFile = 'data_문화관광축제(2000-2018).xlsx'
    sheetList = []

    #openpxl을 이용해 시트명 가져오기
    wb = openpyxl.load_workbook(xlsxFile)
    for i in wb.get_sheet_names():
        sheetList.append(i)
    
    xlsx = pd.ExcelFile(xlsxFile)
    year = []
        
    #pandas를 이용해 각 시트별 데이터 가져오기
    for i in sheetList:
        df = pd.read_excel(xlsx, i)
        if(i != '2000년' and i != '2001년' and i != '2002년' and i != '2003년' and i != '2004년' and i != '2005년' and i != '2006년' and i != '2018년'):
            year.append(i)
            globals()['fes_name{}'.format(i)]=df['축제명']
        if (i == '2017년'):
            standard  = df['축제명']
    
    for y in year:
        sheet = wb[str(y)]
        print(y)
        count = 0
        for i in sheet:
            #제일 첫 열이 None이라서 넘어가는 것
            if(count > 1):
                break
            elif(i[2].value == None):
                count += 1
            # 2017년도 자료와 비교하기
            for fes in standard:
                if(type(fes) == float or i[2].value == None):
                    pass
                elif(len(i[2].value)>len(fes)):
                    if(fes in i[2].value):
                        print("원래", i[2].value)
                        print("standard", fes)
                        i[2].value = fes
                        print("changed")
                        print("바뀐것", i[2].value)
                else:
                    if(i[2].value in fes):
                        print("원래", i[2].value)
                        print("standard", fes)                    
                        i[2].value = fes
                        print("changed")
                        print("바뀐것", i[2].value)


def KTX(fes_data, ktx_file, year):
    stations = []
    station= open(ktx_file, 'r', encoding = 'utf-8')
    lines = station.readlines()
    for line in lines:
        line = line.replace('\n', '')
        stations.append(line)
        
    print(stations)
    import openpyxl

    check = []
    #엑셀파일 불러오기
    wb = openpyxl.load_workbook(fes_data)

    for y in year:
        sheet = wb[str(y)]
        print(y)
        c = 0 
        for i in sheet:
            #제일 첫 열이 None이라서 넘어가는 것
            if(i[1].value == None):
                if(i[0].value in stations):
                    i[11].value = 1
                    print ("지역: ", i[0].value)
                    print("KTX역: ", "yes")
                    c += 1
                else:
                    i[11].value = 0
                    print ("지역: ", i[0].value)
                    print("KTX역: ", "no")
                    c += 1

            else:
                if(i[1].value in stations):
                    i[11].value = 1
                    print ("지역: ", i[1].value)
                    print("KTX역: ", "yes")
                    c += 1
                else:
                    i[11].value = 0
                    print ("지역: ", i[1].value)
                    print("KTX역: ", "no")
                    check.append(0)
                    c  += 1
            if (c > 50):
                break
