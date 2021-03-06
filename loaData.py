import requests
import json
import yaml


#prend un objet json et l'ecrit dans le dossier data, nom = fileName.geojson
def writeData(data,fileName):
    with open('data/'+fileName+'.geojson','w') as f:
            json.dump(data,f)


#recupere depuis l\API de healthsites une donnee se touvant sur pageNum
def getDataByPage(pageNum,url):
    parametres = {'page':pageNum,'format':'json'}
    data = []
    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)

    except Exception as e:
        print(e)
    return data

#recupere depuis des coord lat,long,min,max
def getBboxData(left,bottom,rigth,top,url):
    parametres ={'extent':str(left)+','+str(rigth)+','+str(top)+','+str(bottom),'format':'geojson'}
    data=[]
    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)
    except Exception as e:
        print(e)

    return data

def getDataByLoc(loc, url):
    parametres = {'extent':loc,'format':'geojson'}
    data=[]
    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)
    except Exception as e:
        print(e)

    return data

def merge(json1,json2):
    for dt in json2:
        json1.append(dt)
    print('page appended to!')

def getAllHealthSitePageData(lien):
    pn = {}
    allData = []

    with open('config/pagenumber.json') as d:
        pn = json.load(d)

    pageNumber = pn['hsPageNumber']

    with open('data/healthsites.json') as ad:
        allData = json.load(ad)

    if pageNumber == 0:
        nbPage = 1
        dataPage = getDataByPage(1,lien)
        while dataPage!= []:
            for dt in dataPage:
                allData.append(str(dt))
            nbPage +=1
            dataPage = getDataByPage(nbPage,lien)

        pageNumber = nbPage+1

    else:
        print('file exists')
        print(pageNumber)
        dataPageElse = getDataByPage(pageNumber,lien)
        while dataPageElse != []:
            for dt in dataPageElse:
                allData.append(dt)
            pageNumber+=1
            dataPageElse = getDataByPage(pageNumber,lien)


    #ecriture
    pn['hsPageNumber'] = pageNumber
    with open('config/pagenumber.json','w') as f:
        json.dump(pn,f)

    with open('data/healthsites.json','w') as fd:
        json.dump(allData,fd)

    writeData(allData,"healthsites")
    print('------ done ----')
