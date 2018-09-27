import bs4 as bs
import urllib2 as urll
import numpy as np
import cv2
import time
import codecs
import pandas as pd
from multiprocessing import Pool as ThreadPool
import os

def href_getter(url):
    hrefs = []

    req = urll.Request(url, headers={'User-Agent': "Magic Browser"})
    sauce = urll.urlopen(req)
    soup = bs.BeautifulSoup(sauce, 'lxml')

    divs = soup.find_all('div', class_='infocard')

    # Name extraction finished ---------------------------

    for s in divs:
        span = s.find('span')

        # Pokemon individual website

        for a in span:
            hrefs.append('https://pokemondb.net' + a.get('href'))

    return hrefs
def info_parser(href):
    name = []
    images = []
    req = urll.Request(href, headers={'User-Agent': 'Magic Browser'})
    sauce = urll.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')

    # Attaining image urls
    div = soup.find_all('div',class_='grid-col span-md-6 span-lg-4 text-center')
    for img in div:
        im = img.find('img').get('src')
        images.append(im)


    # Names Retrieval------------------------------------------------------

    div1 = soup.find_all('div', class_='grid-col span-md-6 span-lg-8')
    for d in div1:
        div2 = d.find('em')
        for e in div2:
            name.append(e)

    # Open pokemon documents

    pokemon = codecs.open(r'C:/Users/teriq/OneDrive/Documents/Scraping Practice/Pokemon/Pokedex/%s.csv' % name[0],'w+', encoding='utf8')

    # Attain Pokemon Info

    try:
        dfs = pd.read_html(sauce, header=0, encoding='UTF-8')
        df = dfs[0]
        df = df.fillna(' ')
        df.to_csv('Pokedex/%s.csv' % name[0], header=True, index=False, encoding='UTF-8')

    except ValueError:
        pass
    finally:
        pokemon.close()

    # Image parsing
    try:
        for i in images:
            url = i
            pos = images.index(i)
            req = urll.Request(url,headers={'User-Agent': 'Magic Browser'})
            binary_str = urll.urlopen(req).read()
            byte_array = bytearray(binary_str)
            numpy_array = np.asarray(byte_array,dtype='uint8')
            image = cv2.imdecode(numpy_array,cv2.IMREAD_UNCHANGED)
            if os.path.exists('Images/' + name[0] + ' 1.png') == False:
                cv2.imwrite('Images/' + name[0] + ' 1.png', image)
            elif os.path.exists('Images/' + name[0] + ' 1.png') == True:
                cv2.imwrite('Images/' + name[0] + ' 2.png', image)
            elif os.path.exists('Images/' + name[0] + ' 1.png') == True and os.path.exists('Images/' + name[0] + ' 2.png') == True:
                cv2.imwrite('Images/' + name[0] + ' 3.png', image)
            else:
                pass

            print name[0] + '.png' + ' Is Saved'
    except Exception as e:
        print e


def main():
    beg_time = time.time()
    print 'Running.....'
    hrefs = href_getter('https://pokemondb.net/pokedex/national')
    pool = ThreadPool(4)
    results = pool.map(info_parser,hrefs)
    pool.close()
    pool.join()
    print 'Time elapsed-------',time.time()-beg_time,'seconds---------'
if __name__ == '__main__':
    main()