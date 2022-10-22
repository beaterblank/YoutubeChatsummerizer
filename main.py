#author : G Mohan Teja
#last edited : 22/10/2022

"""
this module is responsible for navingating into webpage and getting the chat msgs
then use them in text rank algorithim to give most relavent msgs
"""

#imports
from selenium import webdriver
from time import time
from textrank import textrank
from http.server import HTTPServer, BaseHTTPRequestHandler
import re

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


#tell the vid link here or give as input?
vid = 'jfKfPfyJRdk'
driver.get(f'https://www.youtube.com/watch?v={vid}')

#remove html tags from a text
clean = lambda datas:[re.sub('<.*?>','',data).strip() for data in datas]


#wait until element is provided with a time out of 1 sec
def getElementXpath(value,multiple=False,timeout=1):
    global driver
    start = time()
    diff = 0
    while(diff<timeout):
        try:
            if(multiple):
                element = driver.find_elements(by='xpath',value=value)
            else:
                element = driver.find_element(by='xpath',value=value)
            break;
        except:
            end = time()
            pass
        diff = end-start
    return element,round(diff,2)

#get chat element src
def getSrc():
    start = time()
    global driver
    element,timetaken = getElementXpath('//*[@id="chatframe"]')
    src = element.get_attribute("src")
    end = time()
    return src,end-start

#getting the chats from src
def getChats():
    global clean
    id = '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/div[1]/div[3]/div[1]/yt-live-chat-item-list-renderer/div/div[1]/div/div/yt-live-chat-text-message-renderer'
    elements,_ = getElementXpath(id,True)
    msgs = []
    for element in elements:
        msgs.append(element.find_element(by='xpath',value='./div[1]/span[2]').get_attribute("innerHTML"))
    return clean(msgs)

#basic http hosting server
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



if __name__ == "__main__":
    #load the chat box
    src,timetaken = getSrc()
    print(f"Loaded in {timetaken:2f} s")
    driver.get(src)
    #turn on the server if any error print the error and close the server and driver
    try:
        server = HTTPServer(('localhost', 8080), Server)
        server.serve_forever()
    except Exception as e:
        print(e)
        server.server_close()
        driver.close()
    

