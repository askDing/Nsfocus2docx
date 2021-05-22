#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Mr.Frame
# Blog: https://askding.github.io/
# Dependence:
#           BeautifulSoup
#           docxtpl

import sys
import time
from bs4 import BeautifulSoup
from docxtpl import DocxTemplate

# 定义漏洞类
class Vulner:
    def __init__(self,vulnName,ipList,details,threatLevel,solutions):
        self.vulnName=vulnName
        self.ipList=ipList
        self.detail=details
        self.threatLevel=threatLevel
        self.solution=solutions


def banner():
    if len(sys.argv) !=2:
        print(" Usage: python3 main.py  <path/to/index.html>  ")
        #sys.exit()

def generate_docx(path):
    data = {"vulners": []}        # 漏洞数据
    soup=BeautifulSoup(open(path),"lxml")
    data['title']=soup.h1.string  # 文档标题
    generated_dox=data['title']+time.strftime("%Y-%m-%d",time.localtime())+".docx"   # 生成文档名

    vuln_table=soup.find('table',attrs={"id": "vuln_distribution",
                                       "class": "report_table"})

    # 获取漏洞名列表
    vuln_name_list=vuln_table.find_all('span')

    # 获取每个漏洞名字下展开信息
    report_table_list = vuln_table.find_all('table', attrs={"class": "report_table"})

    print("\n梳理漏洞如下: ")
    for vul in vuln_name_list:
        vuln_name=vul.get_text().strip()  # 漏洞名列表
        print(vuln_name)

        for report_table in report_table_list:
            vuln_hosts=report_table.find_all("td")[0].get_text()  # 风险来源
            details=report_table.find_all("td")[1].get_text()     # 风险分析
            solution=report_table.find_all("td")[2].get_text().strip()    # 处置建议
            threatLevel=report_table.find_all("td")[3].get_text() # 风险级别

            vuln_hosts=vuln_hosts.replace("&nbsp","").replace("点击查看详情;","")
            data['vulners'].append(
                Vulner(vuln_name,vuln_hosts,details,threatLevel,solution)
                )
            break

    print("文档原始数据生成中...")
    doc = DocxTemplate("template.docx")
    print("正在渲染文档数据....")
    doc.render(data)
    doc.save(generated_dox)
    print("生成完毕，文档名: {}".format(generated_dox))



if __name__ == '__main__':
    banner()
    generate_docx(sys.argv[1])





