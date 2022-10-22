from xml.dom.minidom import Element
from selenium import webdriver
from time import time,sleep
from textrank import textrank
import os

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

vid = 'jfKfPfyJRdk'
driver.get(f'https://www.youtube.com/watch?v={vid}')


import re
clean = lambda datas:[re.sub('<.*?>','',data).strip() for data in datas]

def getElementXpath(value,timeout=1):
    global driver
    start = time()
    diff = 0
    while(diff<timeout*100):
        try:
            element = driver.find_element(by='xpath',value=value)
            break;
        except:
            end = time()
            pass
        diff = end-start
    return element,round(diff,2)

def getElementsXpath(value,timeout=1):
    global driver
    start = time()
    diff = 0
    while(diff<timeout*100):
        try:
            elements = driver.find_elements(by='xpath',value=value)
            break;
        except:
            end = time()
            pass
        diff = end-start
    return elements,round(diff,2)

def getSrc():
    start = time()
    global driver
    element,timetaken = getElementXpath('//*[@id="chatframe"]')
    src = element.get_attribute("src")
    end = time()
    return src,end-start

#getting the chat link
def getChats():
    global clean
    id = '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/div[1]/div[3]/div[1]/yt-live-chat-item-list-renderer/div/div[1]/div/div/yt-live-chat-text-message-renderer'
    elements,_ = getElementsXpath(id)
    msgs = []
    for element in elements:
        msgs.append(element.find_element(by='xpath',value='./div[1]/span[2]').get_attribute("innerHTML"))
    return clean(msgs)

src,timetaken = getSrc()

print(f"Loaded in {timetaken:2f} s")


driver.get(src)






# while(True):
#     msgs = getChats()
#     if(len(msgs)>0):
#         os.system('cls||clear')
#         print(textrank(msgs)[0])
#     sleep(10)
#     driver.refresh()
    

from http.server import HTTPServer, BaseHTTPRequestHandler
class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # get the page
        path = self.path
        if path == '/':
            msgs = textrank(getChats())[0]
            driver.refresh()
            string ='<head><title>Chat</title><meta http-equiv="refresh" content="5"></head>'
            string += "<ul>"
            for msg in msgs:
                if(msg.strip()!=""):
                    string+="<li>"
                    string+=msg
                    string+="</li>"
            string+="</ul>"
            self.wfile.write(bytes(string,"utf-8"))


try:
    server = HTTPServer(('localhost', 8080), Server)
    server.serve_forever()
except:
    pass

server.server_close()

driver.close()
    

