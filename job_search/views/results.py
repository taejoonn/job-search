from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from bs4 import BeautifulSoup
import requests
import urllib.request

def results(request):
    sites = request.POST.getlist('sites')
    location = request.POST.get('location')
    role = request.POST.get('position')
    index = int(request.POST.get("Indeed_page"))
    print(sites)

    for x in sites:
        if (x == "indeed"):
            indeed(role, location, index)

    context = {
        "sites": sites,
        "Indeed_page": index,
        "position": role,
        "location": location
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
