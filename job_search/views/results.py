from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from bs4 import BeautifulSoup
from . import states_abb
import requests
import urllib.request

def results(request):
    sites = request.POST.getlist('sites')
    location = request.POST.get('location')
    role = request.POST.get('position')
    ind_index = int(request.POST.get("Indeed_page"))
    gd_index = int(request.POST.get("GlassDoor_page"))

    for x in sites:
        if x == "indeed":
            indeed(role, location, ind_index)
        elif x == "glassdoor":
            glassDoor(role, location, gd_index)
        elif x == "linkedin":
            print("linkedin")

    context = {
        "sites": sites,
        "Indeed_page": ind_index,
        "position": role,
        "location": location,
        "GlassDoor_page": gd_index
    }
    
    return render(request, 'results.html', context=context)
    
def indeed(position, location, index):
    position = position.replace(" ", "%20")
    result = ""
    location = location.replace(" ", "%20")
    location = location.replace(",", "%2C")
    page = ""

    # determine the webpage number
    if index > 0:
        page = "&start=" + str(index*10)

    # obtain ResultSet for job listings
    url = 'https://www.indeed.com/jobs?q=' + position + '&l=' + location + page
    print(url)
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
        result += "target=" + y[0] + "_blank" + y[0] +" href=" + y[0] + "https://www.indeed.com" + y[1:]
    
    # write ResultSet to html file which will be imported in frontend
    with open("job_search/templates/indeed.html", "w", encoding="utf-8") as file:
        file.write(result)
    file.close()


def glassDoor(position, location, index):
    result = ""

    # create url string
    url = "https://www.glassdoor.com/Job/"
    position = position.replace(" ", "-")
    location = location.split(", ")[1]
    location = states_abb.states[location]
    location = location.replace(" ", "-")
    location = location.lower()
    url += location + "-" + position + "-jobs-SRCH_IL.0,8_IC1132348_KO9,26.htm"
    # determine page number
    page = ".htm"
    if index > 0:
        page = "_IP" + str(index+1) + ".htm"
    url = url.replace(".htm", page)
    
    # obtain ResultSet for job listings
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    allResults = soup.find_all(class_="jl react-job-listing gdGrid")

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
        result += "target=" + y[0] + "_blank" + y[0] +" href=" + y[0] + "https://www.glassdoor.com" + y[1:]
    
    # write ResultSet to html file which will be imported in frontend
    with open("job_search/templates/glassdoor.html", "w", encoding="utf-8") as file:
        file.write(result)
    file.close()
    
