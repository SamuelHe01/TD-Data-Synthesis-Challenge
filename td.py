import requests
from bs4 import BeautifulSoup
from time import sleep
import xlrd
import xlwt
from xlwt import Workbook

links = set()

def url_to_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup

def find_all_tr(soup):
    data = soup.find_all('tr')
    return data

def find_all_td(soup):
    data = soup.find_all('td')
    return data

def search_links(soup, count, base):
    if(count == 0 or len(links)>500):
        return
    #print(soup.find_all('a', href=True))
    for a in soup.find_all('a', href=True):
        if(a['href'].find(base) == -1):
            continue
        links.add(a['href'])
        print(a['href'])
        try:
            search_links(url_to_soup(a['href']), count-1, base)
        except:
            continue
    #print(len(links))
    return links

def search_lots():
    link = 'https://transport.tamu.edu/Parking/faqpermit/info-offcampus.aspx'
    soup = url_to_soup(link)
    table = soup.find(class_='card-deck')
    rows = table.findAll('a')
    names = set()
    for p in rows:
            names.add(p.text)
    return (names)

def get_garage_rates():
    link = 'https://transport.tamu.edu/Parking/visitor.aspx'
    soup = url_to_soup(link)
    sssoup = find_all_td(soup)
    souplist = [td.text for td in sssoup]
    finallist = []
    for n in souplist:
        if (n.find('\n') >= 0):
            break
        finallist.append(n)
    return finallist

def readfromxl():
    loc =r'C:\Users\ericlee2\Downloads\lotlist.xls'
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    lotnames = []
    goodrows = []
    for i in range(sheet.nrows-3):
       # print(type(sheet.cell_value(i+3,2)))
        if(type(sheet.cell_value(i+2,2)) == float and sheet.cell_value(i+2,2)>0):
            lotnames.append(sheet.cell_value(i+2, 0))
            goodrows.append(i+3)
    return lotnames

def writedata_xl(lotnames):
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    weekday = True
    linecounter = 1
    hour = 0
    ticker = 1
    sheet1.write(0, 0, 'Lot/Garage')
    sheet1.write(0, 1, 'Day')
    sheet1.write(0, 2, 'Hour')
    for name in lotnames:
        for i in range(96):
            sheet1.write(linecounter, 0, name)
            if (ticker == 3):
                sheet1.write(linecounter, 1, 'break')
            if (ticker == 4):
                sheet1.write(linecounter, 1, 'summer')
            if (ticker == 1):
                sheet1.write(linecounter, 1, 'weekday')
            if (ticker == 2):
                sheet1.write(linecounter, 1, 'weekend')
            if ((i + 1) % 24 == 0):
                ticker += 1
                if(ticker == 5):
                    ticker = 1
            if(hour == 24):
                hour = 0
            sheet1.write(linecounter, 2, hour)
            hour += 1
            linecounter += 1

    wb.save('examples.xls')

def get_permits():
    link = 'https://transport.tamu.edu/Parking/faqpermit/info.aspx'
    soup = url_to_soup(link)
    table = soup.find(lambda  tag: tag.name=='table')
    rows = table.findAll(lambda  tag: tag.name == 'tr')
    names = []
    for tr in rows:
        td_list = tr.findAll('td')
        if(len(td_list)>0):
            names.append(td_list[0].text)
    return(names)

def not_avail_parking_words(sentence):
    checkwords = ['unavailable','reserved', 'restricted', 'not available', 'not permitted', 'not open']
    for word in checkwords:
        if(sentence.find(word)>=0):
            return True
    return False

def avail_parking_words(sentence):
    checkwords = ['available', 'permitted', 'open']
    for word in checkwords:
        if(sentence.find(word)>=0):
            return True
    return False

def ambiguous_sentence_determiner(sentence):
    if(not_avail_parking_words(sentence)):
        return 'not available'
    elif(avail_parking_words(sentence)):
        return 'available'
    else:
        return

def event_parking_lots():
    link = 'https://transport.tamu.edu/Parking/events/annual.aspx'
    soup = url_to_soup(link)
    cards = soup.find_all(class_ = 'card-body')
    sentences = []
    headers = soup.find_all(class_ = 'card-header pt-4"')
    for card in cards:
        words = card.find_all('p')
        #headers.append(card.find_all(class_='card-link'))
        for word in words:
            sentences.append(word.text)
    ret = []
    for header in headers:
        ret.append(header.find_all(class_ = 'card-link'))
    print(ret)
    #print(sentences)

def search_lots_and_garage(site):
    checkwords = ['lot', 'Lot', 'Lots', 'lots', 'Garage', 'garage']
    soup = url_to_soup(site)
    texts = soup.find_all('p')
    sentences = []
    for text in texts:
        sentences.append(text.text)

    print(sentences)

if __name__ == '__main__':
    #garagedata = get_garage_rates()
    #print(garagedata)
    #readfromxl()
    #print(get_permits())
    #event_parking_lots()
    #print(len(search_lots()))
    #event_parking_lots()
    lots = []
    f = open(r'C:\Users\ericlee2\Downloads\data.txt', 'r')
    for line in f:
        lots.append(line)
    writedata_xl(lots)