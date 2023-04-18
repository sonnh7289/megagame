from flask import Flask, request
from flask_restful import Resource, Api
import requests
from json import dumps
from bs4 import BeautifulSoup

app = Flask(__name__)



@app.route("/home", methods=["GET"])
def get_home():
    
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soup = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonBunny =[]
    for itemBunny in soup.findAll('header', class_="entry-header"):
        ItemJsonBunny = dict()
        ItemJsonBunny['name_Bunny'] = itemBunny.a.text.strip()
        ItemJsonBunny['full_Bunny'] = itemBunny.a['href']
        for itemSpan in itemBunny.findAll('span', class_= 'entry-time'):
            ItemJsonBunny['time_update'] = itemSpan.text.strip()
            break
        for itemSpan in itemBunny.findAll('span', class_= 'entry-date'):
            ItemJsonBunny['ngay_update'] = itemSpan.text.strip()
            break
        for itemSpan in itemBunny.findAll('span', class_= 'author vcard'):
            ItemJsonBunny['ten tac gia'] = itemSpan.text.strip()
            break
        listJsonBunny.append(ItemJsonBunny)
    return listJsonBunny
@app.route('/recents', methods=["GET"])
def get_recents():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soup = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonRecent = []
    b = soup.find('li',class_="widget-container widget_recent_entries")
    for itemRecent in b.findAll('a') :
        ItemJsonRecent = dict()
        ItemJsonRecent['full_Recent'] = itemRecent.get('href')
        ItemJsonRecent['titleRecent'] = itemRecent.text.strip()
        listJsonRecent.append(ItemJsonRecent)
    return listJsonRecent
@app.route('/novels', methods=["GET"])
def get_novels():
    listJsonNovels = []
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soup = BeautifulSoup(rManga_base.content, 'html.parser')
    a = soup.find('div',class_="entry-content")
    for itemNovels in a.findAll('a') :
        ItemJsonNovels = dict()
        ItemJsonNovels['full_Novels'] = itemNovels.get('href')
        ItemJsonNovels['name_Novels'] = itemNovels.text.strip()
        listJsonNovels.append(ItemJsonNovels)
    return listJsonNovels
@app.route('/status', methods=["GET"])
def get_status():
    listJsonstatus = []
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soup = BeautifulSoup(rManga_base.content, 'html.parser')
    status = dict()
    d = soup.findAll('div', class_="textwidget")[1]
    print(d)
    status['status']= d.find('p').text.strip()
    listJsonstatus.append(status)
    return  listJsonstatus
@app.route('/pur', methods=["GET"])
def get_purs():
    listJsonPurgatory = []
    pur =dict()
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soup = BeautifulSoup(rManga_base.content, 'html.parser')
    # status = dict()
    # d = soup.findAll('div', class_="textwidget")[1]
    # print(d)
    # status['status']= d.find('p').text.strip()
    # listJsonPurgatory.append(status)
    c = soup.find('div',class_= "main")
    b = c.find('div',class_="post-4881 page type-page status-publish hentry")
    pur['loi_dan'] = b.find('p').text
    listJsonPurgatory.append(pur)
    for itemPurgatory in b.findAll('a') :
        ItemJsonPurgatory = dict()
        ItemJsonPurgatory['full_Purgatory'] = itemPurgatory.get('href')
        ItemJsonPurgatory['titlePurgatory'] = itemPurgatory.text.strip()
        listJsonPurgatory.append(ItemJsonPurgatory)
    for itemPurgatory in soup.findAll('div',class_='comment-body'):
        CMT = dict()
        CMT["comment"] = itemPurgatory.find('p').text.strip()
        listJsonPurgatory.append(CMT)
    return listJsonPurgatory
@app.route('/cmt', methods=["GET"])
def get_cmt():
    listJsoncmt = []
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soup = BeautifulSoup(rManga_base.content, 'html.parser')
    for itemcmt in soup.findAll('div',class_='comment-body'):
        cmt = dict()
        cmt["comment"] = itemcmt.find('p').text.strip()
        listJsoncmt.append(cmt)
    return listJsoncmt

if __name__ == '__main__':
     app.run(host='0.0.0.0', port = 1000)