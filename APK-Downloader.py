# Coded by: Hamidreza Moradi
# www.github.com/hamidrezamoradi

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

################# Configurations #################
store_path = '/Volumes/TOSHIBA EXT/apks/Google/'
app_list_file = 'applist.txt'
# 1 for apkdl; 2 for apkplz; 3 for apktada; 4 for apkpure.
service_number = '2'
################# colors #################
BLUE = '\033[1;34m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
RED = '\033[1;31m'

RED_BG = '\033[1;77m\033[41m'

CLOSE_COLOR = '\033[m'
##########################################

print(f'''{GREEN}
     ___    ____  __ __ ____                      __                __         
    /   |  / __ \/ //_// __ \____ _      ______  / /___  ____ _____/ /__  _____
   / /| | / /_/ / ,<  / / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/
  / ___ |/ ____/ /| |/ /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    
 /_/  |_/_/   /_/ |_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     

 {RED_BG}      Google Play  Downloader  v2.0,  Author:  @Han0nly & HamidrezaMoradi     {CLOSE_COLOR}\n
''')

try:
    def details(GP_input):
        if 'https://' in GP_input or 'http://' in GP_input:
            pakage_id = BeautifulSoup(requests.get(GP_input).text, 'html.parser').find("meta", attrs={'name': 'appstore:bundle_id'})['content']
            return pakage_id
        elif '.' in GP_input:
            return GP_input
        else:
            print(f'\n{RED} [!] Your input not true.{CLOSE_COLOR}')
            return None

    def downloader(downloadURL, name):
        try:
            r_downloadURL = requests.get(downloadURL, stream=True)

            with open(store_path + name + '.apk', "wb") as handle:
                for data in tqdm(r_downloadURL.iter_content()):
                    handle.write(data)
            return name + '.apk'
        except Exception:
            return False

    def continue_statement():
        statement = input(f'{GREEN} [*] Have you any other requests?([Y]es or [N]):\n {YELLOW}> {CLOSE_COLOR}')
        if statement.lower() == 'yes' or statement.lower() == 'y':
            return True
        elif statement.lower() == 'no' or statement.lower() == 'n':
            return False
        else:
            return continue_statement()

    class Services:
        @staticmethod
        def apkdl_in(pakage_id):
            apkdl = 'https://apkdl.in/app/details?id=%s' % pakage_id
            r = requests.get(apkdl)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("a", itemprop='downloadUrl')

            downloadUrl = 'https://apkdl.in'+downloadUrl['href']
            r = requests.get(downloadUrl)
            DownloadPage = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = DownloadPage.find("a", rel='nofollow')
            return downloadUrl

        @staticmethod
        def apkplz_net(pakage_id):
            url = 'https://apkplz.net/app/%s' % pakage_id
            r = requests.get(url)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("div", attrs={'class':'col-sm-12 col-md-12 text-center'})

            downloadUrl = downloadUrl.find("a", rel='nofollow')['href']
            r = requests.get(downloadUrl)
            DownloadPage = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = DownloadPage.find("a", string='click here')
            return downloadUrl['href']

        @staticmethod
        def apktada_com(pakage_id):
            url = 'https://apktada.com/download-apk/%s' % pakage_id
            r = requests.get(url)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("a", string='click here')
            return downloadUrl['href']

        @staticmethod
        def m_apkpure_com(pakage_id):
            url = 'https://m.apkpure.com/android/%s/download?from=details' % pakage_id
            r = requests.get(url)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("a", string='click here')
            return downloadUrl['href']

        @staticmethod
        def apkcombo_com(pakage_id):
            url = 'https://apkcombo.com/apk-downloader/?package=%s' % pakage_id
            r = requests.get(url)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("ul", attrs={"class": "file-list"}).find('a')
            # downloadUrl = a_item['href']
            # #variants-tab > div > ul > li:nth-child(1) > ul > li > a
            # /html/body/section/div/div/div[1]/div[4]/div[2]/div/ul/li[1]/ul/li/a
            return downloadUrl['href']

    if __name__ == "__main__":
        app_IDList = []
        with open(app_list_file,'r') as f:
            for app_id in f.readlines():
                app_IDList.append(app_id.strip())
        for pakage_id in app_IDList:
            # service_number = input(f'\n{GREEN} [*] Select one among the following sites:\n 1. apkdl.in\n 2. apkplz.net\n 3. apktada.com\n 4. m.apkpure.com\n {YELLOW}> {CLOSE_COLOR}')
            try:
                if service_number == '1':
                    download_URL = Services.apkdl_in(pakage_id)
                elif service_number == '2':
                    download_URL = Services.apkplz_net(pakage_id)
                elif service_number == '3':
                    download_URL = Services.apktada_com(pakage_id)
                elif service_number == '4':
                    download_URL = Services.m_apkpure_com(pakage_id)
                else:
                    print(f'\n{RED} [!] The service_number is not correct.\n Now use apkplz as download source!{CLOSE_COLOR}')
                    download_URL = Services.apkplz_net(pakage_id)
            # statement = continue_statement()
            # if statement: continue
                # else: break
            # download_URL = Services.apktada_com(pakage_id)
            # print(download_URL)

                filename = downloader(download_URL, pakage_id)
                if filename:
                    print(f'\n{GREEN} [*] %s successfully downloaded in the "%s" folder. Enjoy :){CLOSE_COLOR}' % (
                    filename, store_path))
                else:
                    print(f'\n{GREEN} [!] There is a problem for download.{CLOSE_COLOR}')
                    continue
            except requests.exceptions.ConnectionError:
                print(f'\n{RED} [!] No Connection.{CLOSE_COLOR}')
                with open('error.log','a') as log:
                    log.write(pakage_id+'\n')
            except TypeError:
                print(f'\n{RED} [!] App/Game not found.\n [!] Trying again later.{CLOSE_COLOR}')
                with open('notfound.log','a') as log:
                    log.write(pakage_id+'\n')
            except:
                print(f'\n{RED} [!] There\'s a problem.\n [!] Trying another website.{CLOSE_COLOR}')
                with open('notfound.log','a') as log:
                    log.write(pakage_id+'\n')
            finally:
                continue

except requests.exceptions.ConnectionError:
    print(f'\n{RED} [!] No Connection.{CLOSE_COLOR}')
except TypeError:
    print(f'\n{RED} [!] App/Game not found.\n [!] Try again later.{CLOSE_COLOR}')
except:
    print(f'\n{RED} [!] There\'s a problem.\n [!] Try another website.{CLOSE_COLOR}')


