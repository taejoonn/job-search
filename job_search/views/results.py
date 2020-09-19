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
    
    return HttpResponse(prit)
    
def indeed(position):
    temp = position.split()
    role = ""
    companies=[] # list of companies from search results
    addresses=[] # list of company addresses
    job_links=[] # list of job link to indeed
    descriptions=[] # list of job descriptions
    roles=[] # list of job roles from search results

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
    
    for x in allResults:
        # tag with job link and role info
        title = x.find(class_="jobtitle turnstileLink")
        # role
        roles.append(title.text.strip())
        # job link
        job_link = title.get('href')
        job_links.append("indeed.com"+job_link.strip())

        # tag with company, address
        sjcl_class = x.find(class_="sjcl")
        # company
        company = sjcl_class.find(class_="company")
        companies.append(company.text.strip())
        # address
        address = sjcl_class.find(class_="location accessible-contrast-color-location")
        addresses.append(address.text.strip())

        # description
        description = x.find(class_="summary")
        if description is None:
            descriptions.append("")
        else:
            descriptions.append(description.text)

    print(descriptions)
    return allResults
