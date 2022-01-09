from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

startUrl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome(
    "C:/Users/Wyatt/Downloads/chromedriver_win32/chromedriver")

browser.get(startUrl)
holdBefore = "https://exoplanets.nasa.gov"
headers = ["name", "lightyears", "planet mass",
               "stellar magnitude", "discovery year", "hyperlink", "planet type", "planet radius", "orbital radius", "orbital period", "eccentricity"]

MorePlantData = []
planetdata = []
allPlanetData = []
def ScrapeData():
  
    for i in range(0, 5):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        allULtags = soup.find_all("ul",attrs = {"class","exoplanet"})
        for eachUl in allULtags:
            allLItags = eachUl.find_all("li")
            tempList = []
            for index,eachLi in enumerate(allLItags):
                if index == 0:
                    tempList.append(eachLi.find_all("a")[0].contents[0])
                else:
                    tempList.append(eachLi.contents[0])
            link = allLItags[0]
            tempList.append(holdBefore + str(link.find_all("a",href=True)[0]["href"]))
            planetdata.append(tempList)
            
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            

def ScrapeMoreData(hyper):
    page = requests.get(hyper)
    soup = BeautifulSoup(page.content,"html.parser")
    allTRtags = soup.find_all("tr",attrs=({"class","fact_row"}))
    tempList = []
    for indexTr,eachTr in enumerate(allTRtags):
        allTDtags = eachTr.find_all("td")
        for indexTd,eachTd in enumerate(allTRtags):
            if ((indexTr == 0 and indexTd == 1) or (indexTr == 1 and indexTd == 0) or (indexTr == 3 and indexTd == 1)):
                continue
            else:
                data = eachTd.find_all("div",attrs=({"class","value"}))[0].contents[0].get_text()
                tempList.append(data.replace("\n",''))
    MorePlantData.append(tempList)
  


ScrapeData()
for i in planetdata:
    ScrapeMoreData(i[5])

for index, row in enumerate(planetdata):
    allPlanetData.append(planetdata[index] + MorePlantData[index]) 
with open ("exoplanetScraping.csv","w",newline="") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(allPlanetData)






