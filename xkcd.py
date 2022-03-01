import bs4
import os
import requests


APP_NAME = 'xkcd Downloader'
SITE_URL = 'https://xkcd.com/'

def xkcd():
    site = SITE_URL
    while not site.endswith('#'):

        res = requests.get(site)
        res.raise_for_status
        soup = bs4.BeautifulSoup(res.text,'html.parser')

        comic_url = soup.select_one('#comic img')
        if comic_url.get('srcset') != []:
            link = 'https:' + comic_url.get('srcset').split()[0]
        elif comic_url.get('src') != []:
            link = 'https:' + comic_url.get('src').split()[0]
        else:
            print(comic_url + ' could not be downloaded')

        comic = requests.get(link)
        comic.raise_for_status

        os.makedirs('./xkcd', exist_ok = True)

        prev = soup.select('a[rel="prev"]')[0]
        site = 'https://xkcd.com' + prev.get('href')

        if prev.get('href') == '#':
            current_comic_no = 1
        else:
            current_comic_no = int(prev.get('href').replace('/','')) + 1

        f = open(os.path.join('xkcd',str(current_comic_no) + " " + os.path.basename(link).replace("_2x","")),'wb')
        for chunk in comic.iter_content(100000):
            f.write(chunk)

        #f.write(comic.content)
        f.close

        print('downloaded xkcd comic ' + str(current_comic_no))





if __name__ == '__main__':
    xkcd()