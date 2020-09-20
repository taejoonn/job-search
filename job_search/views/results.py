from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from bs4 import BeautifulSoup
import requests
import urllib.request

def results(request):
    page = 0
    sites = request.POST.getlist('sites')
    location = request.POST.get('location')
    role = request.POST.get('position')
    index = request.POST.get("index")
    

    for x in sites:
        if (x == "indeed"):
            indeed(role, location, index)
    
    return render(request, 'results.html')
    
def indeed(position, location, index):
    temp = position.split()
    result = ""
    role = ""
    # companies=[] # list of companies from search results
    # addresses=[] # list of company addresses
    # job_links=[] # list of job link to indeed
    # descriptions=[] # list of job descriptions
    # roles=[] # list of job roles from search results

    for space in temp:
        role += space+"%20"

    url = 'https://www.indeed.com/jobs?q=' + role + '&l=New%20York%2C%20NY&ts=1600003327916&rq=1&rsIdx=0&fromage=last&newcount=190&vjk=56afb9750841d452'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    allResults = soup.find_all(class_="jobsearch-SerpJobCard unifiedRow row result")
    
    # convert ResultSet to string
    for x in allResults:
        result += str(x)
    # split string at 'href'
    resultList = result.split("href=")
    result = ""
    # loop and insert 'indeed.com' at href tags
    for x, y in enumerate(resultList):
        if x == 0:
            result += y
            continue
        result += "href=" + y[0] + "indeed.com" + y[1:]

    # write ResultSet to html file which will be imported in frontend
    with open("indeed.html", "w", encoding="utf-8") as file:
        file.write(result)
    file.close()

    # if we want to pass info as objects
    # for x in allResults:
    #     # tag with job link and role info
    #     title = x.find(class_="jobtitle turnstileLink")
    #     # role
    #     roles.append(title.text.strip())
    #     # job link
    #     job_link = title.get('href')
    #     job_links.append("indeed.com"+job_link.strip())

    #     # tag with company, address
    #     sjcl_class = x.find(class_="sjcl")
    #     # company
    #     company = sjcl_class.find(class_="company")
    #     companies.append(company.text.strip())
    #     # address
    #     address = sjcl_class.find(class_="location accessible-contrast-color-location")
    #     addresses.append(address.text.strip())

    #     # description
    #     description = x.find(class_="summary")
    #     if description is None:
    #         descriptions.append("")
    #     else:
    #         descriptions.append(description.text)