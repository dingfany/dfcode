import requests
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_data(project):
    # Make an API call, and store the response.
    url = 'http://aww.sh.bel.alcatel.be/tools/dslam/cm/sqlrep/cgi-bin/csv.cgi?r=xls_fr_screening_25&p0='+project+'&p99=11&p41=FR'
    password=input('your password:')
    r = requests.get(url,auth=('dingfany',password))
    frfilepath='FR_table_'+project
    print('geting data from CQ....and save to file'+frfilepath)
    f=open(frfilepath, 'w')
    f.write(r.text)
    f.close()
    return frfilepath

def duidiebar(fdt_list,fdt_sv1_counter_list,fdt_sv2_counter_list,fdt_sv3_counter_list):
    x =list(range(len(fdt_list)))

    plt.bar(x, fdt_sv1_counter_list, width=0.5, color='red', label=1)
    plt.bar(x, fdt_sv2_counter_list, width=0.5, color='yellow', label=2, bottom=fdt_sv1_counter_list)
    plt.bar(x, fdt_sv3_counter_list, width=0.5, color='lightskyblue', label=3, bottom=fdt_sv2_counter_list)

    plt.title("FDT based FRs")
    #plt.xlabel("FDT")
    plt.ylabel('FR counter')
    plt.xticks(range(len(x)), fdt_list)
    plt.legend(title='Sev', loc='upper right')
    plt.xticks(rotation=90)    # 设置横坐标标签旋转角度。
    plt.tight_layout()
    plt.savefig("FDT vs sev FRs.svg",format='svg')
    plt.show()

def barbar(fdt_list,fdt_sv1_counter_list,fdt_sv2_counter_list,fdt_sv3_counter_list):
    x =list(range(len(fdt_list)))
    total_width, n = 0.8, 2
    width = total_width / n

    plt.bar(x, fdt_sv1_counter_list, width=width, label='Sv1',fc = 'r')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, fdt_sv2_counter_list, width=width, label='Sv2',tick_label =fdt_list,fc = 'y')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, fdt_sv3_counter_list, width=width, label='Sv3',tick_label = fdt_list,fc = 'b')
    plt.legend(loc='upper left')
    plt.show()

def clean_data(FRs):
    #what a fuck columns names, rename index and column    
    FRs.rename(columns={'Name                    ':'Name'}, inplace=True)
    FRs.rename(columns={'ONTType                 ':"ONTTYPE"},inplace=True)
    FRs.rename(columns={'Sv                      ':"Sv"},inplace=True)
    FRs.rename(columns={'FDT                     ':'FDT'},inplace=True)
    FRs.rename(columns={'Brief Description       ':"Desc"},inplace=True)
    FRs.rename(columns={'St                      ':"St"},inplace=True)
    FRs['FDT'].fillna('unknown',inplace=True)

def filter(FRs):
    print('filter according to product','ChinaONT.csv')
    aont=pd.read_csv('ChinaONT.csv')
    frstatus=['N','X']
    #filtered_by_onttype=(FRs[FRs['ONTTYPE']=='AONT_G-140W-TD_MTK_RG'])
    filtered_by_onttype = FRs[FRs.ONTTYPE.isin(list(aont.ONT_CHINA))]
    filtered_by_frstatus= filtered_by_onttype[filtered_by_onttype.St.isin(frstatus)]
    filtered=filtered_by_frstatus.loc[:,['Name','Desc','FDT','Sv']]
#    print(filtered)
    return filtered

def plot_simple(filtered):
    grouped_fdt=filtered.groupby(['FDT'])
    #直接用value_counts,plot pandas
    grouped_fdt['Sv'].value_counts().unstack().plot(kind='barh', figsize=(20, 4))
    plt.show()


####################################
#            main
####################################
default_project='hdr6301'
project_no=input("please input your project No. such as "+default_project+":")
if project_no:
    in_project=project_no.strip().lower()
else:
    in_project=default_project

from_remote=input("get from remote (Y/N):")
if from_remote=='Y' or from_remote=='y' or from_remote.strip()=='':
    remote = '1'
else:
    remote = '0'

if remote == '1':
    frfilepath=get_data(in_project)
else:  
    print('get from LOCAL!')
    frfilepath="FR_table_"+in_project


FRs = pd.read_table(frfilepath)

clean_data(FRs)

filtered=filter(FRs)
filtered.to_csv('aferfilter.csv')


#method1,pandos don't support plot complext directly, manually draw
grouped_fdt=filtered.groupby(['FDT'])
    
fdt_list=[]
sv_list=['1','2','3']
fdt_sv1_counter_list=[]
fdt_sv2_counter_list=[]
fdt_sv3_counter_list=[]

for fdtname, fdtsv in grouped_fdt:
    fdt_list.append(fdtname)
    fdt_sv1_counter_list.append(len(fdtsv['Sv'][fdtsv['Sv']==1]))
    fdt_sv2_counter_list.append(len(fdtsv['Sv'][fdtsv['Sv']==2]))
    fdt_sv3_counter_list.append(len(fdtsv['Sv'][fdtsv['Sv']==3]))

fdt_no_list=[]
for fdtfullname in fdt_list:
    fdt_no_list.append(fdtfullname.split(":")[0])

# #用堆叠的图显示
duidiebar(fdt_no_list,fdt_sv1_counter_list,fdt_sv2_counter_list,fdt_sv3_counter_list)

#method 2,using groupby and groupby again.
#plot_simple(filtered)

#method 3,using pivot table.
#print(pd.pivot_table(filtered, index=['FDT','Sv'],aggfunc='count'))






