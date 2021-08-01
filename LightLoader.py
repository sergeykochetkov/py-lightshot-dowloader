from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import random, string, os
import threading
import requests
import time

# - Output folder name.
DIRNAME = "Output"
DLCOUNT = 0
ERCOUNT = 0
LENGTH = 6

class LightLoader(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        while True:
            fileName = self.generateId(LENGTH)
            url = self.generateLink(fileName)
            print(url)
            self.generateImgur(url, fileName)

    # - Generates lightshot link using generateId() function
    def generateLink(self, fileName):
        return "https://prnt.sc/" + fileName


    # - Generates random string
    def generateId(self, size):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


    # - Downloads HTML File from link previously generated
    def generateHtml(self, fileName):
        url = self.generateLink(fileName)
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(request)
        page = urlopen(request).read()
  
        return page


    # - Looks for raw image link in HTML File
    def generateImgur(self, url, fileName):
        soup = BeautifulSoup(self.generateHtml(fileName), 'html.parser')
        imgUrl = soup.find('img', id='screenshot-image')

        if imgUrl is not None:
            imgUrl = imgUrl['src']
            # - Prevents "Error Image" From being downloaded
            if imgUrl != '//st.prntscr.com/2018/06/19/0614/img/0_173a7b_211be8ff.png':
                imgUrl = imgUrl.replace('//st.', 'http://st.') if imgUrl.startswith('//st.') else imgUrl

                global DLCOUNT
                DLCOUNT += 1

                print("Prepare to download: " + imgUrl)
                archive_path = DIRNAME + "/" + fileName + ".png"

                with open(archive_path, 'wb') as f:
                    f.write(requests.get(imgUrl, headers={'User-Agent': 'Mozilla/5.0'}).content)

                print("File: " + fileName + " - Saved to " + DIRNAME + " folder.  ")
                print("Total Downloads: " + str(DLCOUNT))

        else:
            global ERCOUNT
            ERCOUNT += 1
            print("The requested url is invalid. Trying a new combination... Error n. " + str(ERCOUNT))


def main():
    # - Creates "Output" folder if not present
    if not os.path.exists(DIRNAME):
        os.makedirs(DIRNAME)

    for _ in range(int(input("Input number of threads to be used: "))):
        thread = LightLoader()
        thread.start()
        time.sleep(0.25)

        print("Active threads: {}".format(threading.activeCount() - 1))


main()


