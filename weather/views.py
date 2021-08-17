from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import lxml

# get weather information with Linux User Agent
def get_html_content_WA(request):   
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"      
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content

# get weather information with Windows User Agent
def get_html_content_LA(request):   
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    session = requests.Session()
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content

def home(request):
    result = None
    if 'city' in request.GET:

        html_content = get_html_content_LA(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        result = dict()        
        result['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
        result['temp_now'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        result['dayhour'], result['weather_now'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split(
            '\n')

    context = {'result': result}
    return render(request, 'weather/home.html', context)