from medicinequiry.models import Ilaclar, Hastalik, Alerji
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.shortcuts import render
import time


def fill_Database(request):
    file_path = "C:\\Users\\hypyn\\Desktop\\VTYS Proje\\medicinequirysite\\medicinequiry\\managment\\İlaçlar.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    ilaclar = text.split('/*,*/')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    for ilac in ilaclar:
        ilac_adi = ""
        firma_adi = ""
        recete_turu = ""
        ithal_imal = ""
        fiyat = ""
        etkin_madde_adi = ""
        kullanimi_durumu = ""
        nasil_kullanilir = ""
        yas_araligi = ""
        cinsiyet = ""
        dozu = ""
        turu = ""
        kullanim_periyodu = ""

        driver.get("https://farmalog.info/")
        search_box = driver.find_element("id", "searchbox")
        search_box.send_keys(ilac.strip().lower())
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            first_element = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[1]/div[1]")
            first_element.click()
            time.sleep(2)
            ilac_adi = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div[1]/div[1]/div[2]/div[1]/b").text
            firma_adi = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div[1]/div[1]/div[2]/div[3]").text[7:]
            recete_turu = driver.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div[1]/div[1]/div[2]/div[5]/small[1]").text[8:]
            ithal_imal = driver.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div[1]/div[1]/div[2]/div[5]/img").get_attribute('src')[-6:]
            fiyat = driver.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div[1]/div[1]/div[2]/div[4]/small[1]").text[7:]
            etkin_madde_adi = driver.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div[1]/div[1]/div[2]/div[2]/small").text[13:]

            try:
                what_used_for = driver.find_element(By.XPATH, "/html/body/div[2]/aside/ul/li[2]/a")
                what_used_for.click()
                time.sleep(1)
                kullanimi_durumu = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div[1]/div[2]/section/p").text
            except:
                pass

            try:
                how_to_use = driver.find_element(By.XPATH, "/html/body/div[2]/aside/ul/li[3]/a")
                how_to_use.click()
                time.sleep(1)
                nasil_kullanilir = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div[1]/div[2]/section/p").text
            except:
                pass

            try:
                information = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div[1]/div[2]/div/button[1]")
                information.click()
                time.sleep(1)
                yas_araligi = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/table[1]/tbody/tr[7]/td[2]").text
                cinsiyet = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/table[1]/tbody/tr[6]/td[2]").text
                dozu = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/table[1]/tbody/tr[4]/td[2]").text.split('/')[1]
                turu = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/table[1]/tbody/tr[3]/td[2]").text
                kullanim_periyodu = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/table[1]/tbody/tr[13]/td[2]").text
            except:
                pass

            ilac = Ilaclar(
                ilac_adi=ilac_adi.strip(),
                firma_adi=firma_adi.strip(),
                recete_turu=recete_turu.strip(),
                ithal_imal=ithal_imal.strip(),
                fiyat=fiyat.strip(),
                yas_araligi=yas_araligi.strip(),
                cinsiyet=cinsiyet.strip(),
                dozu=dozu.strip(),
                turu=turu.strip(),
                kullanim_periyodu=kullanim_periyodu.strip(),
                kullanimi_durumu=kullanimi_durumu.strip(),
                nasil_kullanilir=nasil_kullanilir.strip(),
                etkin_madde_adi=etkin_madde_adi.strip(),
            )
            #ilac.save()
            print(ilac.ilac_adi + "Veritabanına kayıt edildi")
        except Exception:
            pass

    driver.quit()
    return render(request, '../templates/medicinequirysite/fill_database.html')

def fill_Database_Hastaliklar(request):
    file_path = "C:\\Users\\hypyn\\Desktop\\VTYS Proje\\medicinequirysite\\medicinequiry\\managment\\Hastalıklar.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    hastaliklar = text.split(',')

    for hastalik in hastaliklar:
        illness = Hastalik(
            hastalik_adi = hastalik.strip()
        )
        #illness.save()

    return render(request, '../templates/medicinequirysite/fill_database.html')

def fill_Database_Alerjiler(request):
    file_path = "C:\\Users\\hypyn\\Desktop\\VTYS Proje\\medicinequirysite\\medicinequiry\\managment\\Alerjiler.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    alerjiler = text.split(',')

    for alerji in alerjiler:
        allergy = Alerji(
            alerji_adi = alerji.strip()
        )
        #allergy.save()

    return render(request, '../templates/medicinequirysite/fill_database.html')

#Bu kod bloğu ilaç isimlerini çekmek için yazılmış bir scripttir.

#def fill_Database(request):
#    ilaclar = []
#    harfler = ['J','K','L','M','N','O','P','R','S','%DE','T','U','W','X','V','Y','Z']
#    xpath = ""
#    driver = webdriver.Chrome()
#    driver.maximize_window()
#    for i in harfler:
#        driver.get("https://www.ilacrehberi.com/ilac-fihrist//?h="+i)
#        time.sleep(1)
#        indis = 2
#        while True:
#            try:
#                xpath = "/html/body/div/div/div/div[5]/div[1]/div[3]/div/div[5]/table/tbody/tr[" + str(indis) + "]/td[2]/a"
#                ilaclar.append(driver.find_element(By.XPATH, xpath).text)
#                indis+=1
#            except:
#                break
#
#    driver.quit()
#
#    with open('ilaç isimleri.txt','w', encoding="UTF-8") as file:
#        for i in ilaclar:
#            file.write(str(i)+',')
#    return render(request, '../templates/medicinequirysite/fill_database.html')

#Bu kod bloğu ilaç isimlerini doğruluğunu sorgulamak için yazılmış bir scripttir.

#def fill_Database(request):
#    ilaclartext = []
#    ilaclarsite = []
#    with open('C:\\Users\\hypyn\\Desktop\\VTYS Proje\\medicinequirysite\\medicinequiry\\managment\\yeni.txt', 'r', encoding='utf-8') as file:
#        text = file.read()
#    text = text.split(',')
#
#    driver = webdriver.Chrome()
#    driver.maximize_window()
#    for i in text:
#        i = i.strip().capitalize()
#        driver.get("https://farmalog.info/")
#        search_box = driver.find_element("id", "searchbox")
#        search_box.send_keys(i.lower())
#        search_box.send_keys(Keys.RETURN)
#        time.sleep(1)
#        try:
#            first_element = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[1]/div[1]")
#            first_element.click()
#            time.sleep(1)
#            ilac_adi = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div[1]/div[1]/div[2]/div[1]/b").text
#            if i.lower() == ilac_adi.lower():
#                ilaclartext.append(i)
#            ilaclarsite.append(ilac_adi)
#        except:
#            pass
#
#    driver.quit()
#
#    with open('C:\\Users\\hypyn\\Desktop\\VTYS Proje\\medicinequirysite\\medicinequiry\\managment\\site text aynı ilaç isimleri.txt', 'w', encoding="UTF-8") as file:
#        for i in ilaclartext:
#            file.write(str(i)+',\n')
#
#    with open('C:\\Users\\hypyn\\Desktop\\VTYS Proje\\medicinequirysite\\medicinequiry\\managment\\site ilaç isimleri.txt', 'w', encoding="UTF-8") as file:
#        for i in ilaclarsite:
#            file.write(str(i)+',\n')
#    return render(request, '../templates/medicinequirysite/fill_database.html')
