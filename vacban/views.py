from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect

from selenium import webdriver
from PIL import Image
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import os, time

js_payload = """
var div = document.createElement('div');
div.className = 'profile_ban_status';
div.innerHTML='<div class="profile_ban">1 VAC ban on record <span class="profile_ban_info">| <a class="whiteLink" href="https://support.steampowered.com/kb_article.php?ref=7849-Radz-6869&amp;l=english" target="_blank" rel="noreferrer">Info</a></span></div>0 day(s) since last ban';
document.getElementsByClassName("responsive_status_info")[0].appendChild(div);
"""
@csrf_protect
def home(request):
    if request.method != 'POST':
        return render(request,'home.html',{})
    if ("steamcommunity.com/id/" in request.POST.get('url')) or ("steamcommunity.com/profiles/" in request.POST.get('url')) and request.POST.get('language'):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1366x768")
        chrome_driver = os.getcwd() +"/chromedriver"
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        driver.get(request.POST.get("url"))
        driver.execute_script(js_payload)
        filename = str(datetime.now().microsecond)+"capture.png"
        filepath = "static/res/img/"+filename
        newfilepath = "static/res/img/"+filename.rsplit(".",1)[0]+".jpg"
        if driver.get_screenshot_as_file(filepath):
            image_data=Image.open(filepath)
            image_data=image_data.convert("RGB")
            image_data.save(newfilepath)
            image_data=open(newfilepath,"rb").read()
            driver.close()
            response = HttpResponse(image_data, content_type="image/jpg")
            response['Content-Disposition'] = "attachment; filename=capture.jpg"
            return response
    raise Http404
