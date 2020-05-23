import pandas as pd
from openpyxl import load_workbook

lists = load_workbook('data_fesitival.xlsx')
year = ['2017년']
#year = ['2007년', '2008년', '2009년', '2010년', '2011년', '2012년', '2013년', '2014년', '2015년', '2016년', '2017년']
문제 = []
fes = []
for y in year:
    p=[]
    n=[]
    sheet = lists[y]
    count = 0
    for i in sheet:
        count += 1
        if(count > 2):
            fes.append(i[2].value)
    for fes_name in fes:
        if(fes_name != None):
            file = fes_name+'.csv'
        else:
            break
        축제 = []
        print(file)
        try:
            read = pd.read_csv("new_sentiment/"+file)
            read.columns = ["축제", "content", "해시태그", "year", "polarity", "a", "b", "c"]
            read1 = read[read.year == 2017]
            a = read1["polarity"].value_counts()
            check = True
            try:
                positive = a.positive
                negative = a.negative
                neutral = a.neutral
                positive_percentage = positive/(positive+negative+neutral)
                negative_percentage = negative/(positive+negative+neutral)
                print(positive_percentage)
                print(negative_percentage)
                p.append(positive_percentage)
                n.append(negative_percentage)
            except AttributeError:
                print("Attrubute")
                문제.append(fes_name)
                p.append("0")
                n.append("0")    
        except FileNotFoundError:
            print("실패")
            p.append("0")
            n.append("0")
        except pd.errors.EmptyDataError:
            p.append("0")
            n.append("0")
            
            
    print("========",y,"==============")
    for pos in p:
        print(pos)
    print("========Negative==============")   
    for neg in n:
        print(neg)
print(문제)