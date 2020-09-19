from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
import time
import json

def results(request):
    sites = request.POST.getlist('sites')
    role = request.POST.get('position')
    prit = ""

    for x in sites:
        if (x == "indeed"):
            prit = indeed(role)
    
    print(prit)
    return HttpResponse(prit)
    
def indeed(position):
    temp = position.split()
    role = ""
    company=[] # list of companies from search results
    job_link=[] # list of job link to indeed
    description=[] # list of job descriptions

    for space in temp:
        role += space+"%20"

    url = 'https://www.indeed.com/jobs?q=' + role + '&l=New%20York%2C%20NY&ts=1600003327916&rq=1&rsIdx=0&fromage=last&newcount=190&vjk=56afb9750841d452'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ###### for examining the requested html ######
    # temp = soup.prettify().replace(u'\xa0', u' ')
    # temp  = temp.replace(u'\u2022', u'-')
    # temp = temp.replace(u'\u2013', u'-')
    # temp = temp.replace(u'\xa9', u' ')
    # writer = open("soup.html", "w")
    # writer.write(temp)
    # writer.close()
    allResults = soup.find_all(class_="jobsearch-SerpJobCard unifiedRow row result")
    res_contents = allResults[0].contents[0]
    res_json = json.loads(res_contents)
    type(res_json)
    print(res_json)

    # writer = open("soup.html", "w")
    # writer.write(textt)
    # writer.close()
    return allResults
