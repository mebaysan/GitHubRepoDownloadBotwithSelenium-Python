from selenium import webdriver # selenium'dan gerekli kütüphaneyi import ettik
import time
import subprocess # arkada otomatik cmd komutları için
import optparse # cmd komutlarına -s gibi optionlar vermek için
import os
driver = webdriver.Chrome() # driver oluşturduk
parse_object = optparse.OptionParser() # optionlar için obje oluşturduk
parse_object.add_option("-n", "--user_name", dest="user_name",help="user name") # -n --user_name değişkenlerini dest="user_name" diyerek user_name'e atadık
parse_object.add_option("-p", "--user_password", dest="user_password",help="user password")
(user_inputs, arguments) = parse_object.parse_args() # user_inputs diyerek terminalden gelen komutlarla bir tuple oluşturduk
driver.get("https://github.com/") # githuba git
login = driver.find_element_by_xpath("/html/body/div[1]/header/div/div[2]/div[2]/a[1]") # login butonu yakala
login.click() # tıkla
login_input = driver.find_element_by_id("login_field") # login input yakala
login_input.send_keys(user_inputs.user_name) # terminalden gelen -n "user_name" buraya yolladık
password_input = driver.find_element_by_id("password")
password_input.send_keys(user_inputs.user_password)  
login = driver.find_element_by_xpath("//*[@id='login']/form/div[3]/input[4]") # login butona tıkladık login olduk
login.click()
profile_logo = driver.find_element_by_xpath("/html/body/div[1]/header/div[8]/details/summary/span") # profil logosundan kendi repolarımıza gitmek için butonu açmaya çalışıyoruz
profile_logo.click() # profil logosuna tıklayıp kendi profilimize gittik
your_repos = driver.find_element_by_xpath('/html/body/div[1]/header/div[8]/details/details-menu/a[2]') # kendi repolarımızın olduğu elementi yakaladık
your_repos.click() # kendi repolarımıza tıkladık
sayac = 1
flag = True # kontrol noktası oluşturduk

while flag: # flag true olduğu sürece
    try:
        repo = "//*[@id='user-repositories-list']/ul/li[{}]/div[1]/div[1]/h3/a".format(sayac) # bu site yapısı gereği repo linkleri xpath'inde sadece format ile belirlenen alan değişiyor bunun için sayac ile orayı artırıyoruz
        repository = driver.find_element_by_xpath(repo) # oluşturduğumuz xpath stringi repository'e attık
        repository.click() # repository'e tıkladık
        subprocess.call(["git", "clone", driver.current_url + ".git"]) # github yapısı gereği clone olayı git clone repo_adresi.git olarak iner
                            # burada dedik ki cmd'de sırasıyla git clone o_anki_url_adresi.git(repoya gittiğimizde url al) -> python dosyasının çalıştığı dizine iner
        driver.back() # bir önceki sayfaya git bu sayede kalan repoları çek
        sayac +=1 # sayacı sürekli arttır ki diğer repoya ulaşabilelim
    except: # sayac mevcut repo sayımızı geçince hata verecek
        flag = False # flag kontrol noktamızı False yaparak döngüyü bitiriyoruz