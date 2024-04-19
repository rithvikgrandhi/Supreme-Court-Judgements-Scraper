import requests
import re
from bs4 import BeautifulSoup
import time
import json

for year in range(1949,2024):
    time.sleep(5)
    for month in range(1,13):
        # time.sleep(3)
        print(year,month)
        for cnt in range(40):
            time.sleep(0.25)
            URL = f"https://indiankanoon.org/search/?formInput=doctypes%3A%supremecourt%20fromdate%3A%201-{month}-{year}%20todate%3A%2028-{month}-{year}&pagenum={cnt}"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            if not str(soup):
                break
            print(year, month, cnt)
            print(URL)
            results = soup.find_all(class_="results_content")

            soup2 = BeautifulSoup(str(results), 'html.parser')
            results2 = soup2.find_all(class_="results_middle")

            soup3 = BeautifulSoup(str(results2), 'html.parser')
            results3 = soup3.find_all(class_="result")

            soup4 = BeautifulSoup(str(results3), 'html.parser')
            results4 = soup4.find_all(class_="result_title")

            soup5 = BeautifulSoup(str(results4), 'html.parser')
            results5 = soup5.find_all('a', href=True)

            lis2 = []

            for link in results5:
                href = link.get('href')
                if href:
                    lis2.append("https://indiankanoon.org" + href)
            print(len(lis2))
            if len(lis2)==0:
                break
            for URL2 in lis2:
                page2 = requests.get(URL2)
                soup6 = BeautifulSoup(page2.content, 'html.parser')

                soup7 = BeautifulSoup(str(soup6), 'html.parser')

                dict1 = {
                    "Issue": "Issue",
                    "Facts": "Facts",
                    "PetArg": "Petitioner's Arguments",
                    "RespArg": "Respondant's Arguments",
                    "Section": "Analysis of the law",
                    "Precedent": "Precedent",
                    "CDiscource": "Court's Reasoning",
                    "Conclusion": "Conclusion"
                }

                allouts = {}
                conclusion_text = ""
                paragraph_tags = soup7.find_all(['p', 'blockquote'])
                soup8 = BeautifulSoup(str(paragraph_tags), 'html.parser')

                for j in dict1:
                    if j in ["Conclusion", "CDiscource"]:
                        continue

                    tags2 = soup8.find_all('p', attrs={'data-structure': {j}})
                    data1 = ""
                    for i in tags2:
                        data1 += i.text.strip()
                        smolis = i.find_next_siblings('blockquote')
                        for k in smolis:
                            data1 += k.text.strip()

                    data1 = data1.replace("\n", " ")
                    data1 = re.sub("\s{2,}", " ", data1)
                    data1 = data1.replace('"', ' ')
                    data1 = data1.replace("\t", " ")
                    allouts[j] = data1

                # Separate extraction for Conclusion and Court's Reasoning
                for conclusion_key in ["CDiscource","Conclusion"]:
                    conclusion_tags = soup8.find_all('p', attrs={'data-structure': {conclusion_key}})
                    for tag in conclusion_tags:
                        conclusion_text += tag.text.strip() + " "
                        smolis = tag.find_next_siblings('blockquote')
                        for k in smolis:
                            conclusion_text += k.text.strip() + " "


                conclusion_text = re.sub("\s{2,}", " ", conclusion_text)
                conclusion_text = conclusion_text.replace('"', '')

                finstr = ""
                # print(dict1)
                for key, value in allouts.items():
                    finstr += f'{dict1[key]} : {value}'
                finstr=finstr.replace("\n"," ")
                finstr=finstr.replace("\t"," ")
                finstr=finstr.replace("\u00a0"," ")
                if finstr=="" or conclusion_text=="":
                    continue
                json_structure = {
                    "instruction": "This document contains summarized details of a legal case as processed from public records. Each section provides insight into different aspects of the case, including the core issue at hand, factual background, arguments presented by both sides, legal analysis, precedent considered, and the courts reasoning leading to the conclusion.Identify the relevant legal issues, List applicable laws and statutes, and Predict possible legal outcomes based on the given scenario.",
                    "input": finstr,
                    "output": conclusion_text
                }

                with open("output.jsonl", "a") as f1:
                    json.dump(json_structure, f1)
                    # json.dump("\n",f1)
                    f1.write(',\n')
