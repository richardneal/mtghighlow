import urllib
from bs4 import BeautifulSoup
import sqlite3
import os
import time
import ssl

base_url = "http://www.mtggoldfish.com/"

def connect_db():
    dir = os.path.dirname(__file__)
    print(str(dir))
    filename = os.path.join(dir, 'db', 'cards.db')
    print(filename)
    return sqlite3.connect(filename)


def archive_db():
    dir = os.path.dirname(__file__)
    print(str(dir))
    filename = os.path.join(dir, 'db', 'cards.db')
    if not os.path.isdir(os.path.join(dir, 'db', 'archive')):
        os.makedirs(os.path.join(dir, 'db', 'archive'))
    if os.path.isfile(filename):
        try:
            newfilename = os.path.join(dir, 'db', 'archive', 'cardsarchive' + time.strftime("%Y%m%d-%H%M%S") + '.db')
            print(newfilename)
            os.rename(filename, newfilename)
        except Exception as e:
            print(e)
            return False
    open(filename, 'a').close()
    return True


def site_to_db(cardlist):
    if archive_db():
        conn = connect_db()
        c = conn.cursor()
        c.executescript('drop table if exists cardlist')
        c.executescript('''create table cardlist
                (name text, fullsetname text, setname text, price real, rarity text, format text)''')
        for item in cardlist:
            c.execute('INSERT INTO cardlist VALUES (?,?,?,?,?,?)', item)
        conn.commit()
        for row in c.execute('SELECT * FROM cardlist'):
            print(row)
        conn.close()
    else:
        print('Could not refresh DB')


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def get_format_cards(format, paper):
    a = []
    goldfishURL = base_url + "index/" + format
    htmlFile = urllib.urlopen(goldfishURL)
    rawHTML = htmlFile.read()
    soup = BeautifulSoup(rawHTML, "lxml")
    if paper:
        category = soup.find("div", "index-price-table-paper")
    else:
        category = soup.find("div", "index-price-table-online")
    tablebody = category.find("tbody")

    for index, card in enumerate(tablebody.findAll("tr")):
        info = []
        values = card.findAll("td")
        for value in (values[0], values[1], values[3]):
            thetext = u''.join(value.findAll(text=True)).strip()
            if 'PRM-GPP' in thetext:
                thetext = thetext.replace('PRM-GPP', 'GPX')
            info.append(thetext)
        a.append(info)
        if index > 100:
            break
    return a


def get_cardlist_from_db(rarity=['Mythic', 'Rare', 'Uncommon', 'Common'],
                      format=['standard', 'modern', 'legacy', 'special']):
    conn = connect_db()
    c = conn.cursor()
    execute = 'select * from cardlist where ('
    if rarity is not None:
        execute += 'rarity is "' + rarity[0]
    for rar in rarity[1:]:
        execute += '" or rarity is "' + rar
    if format is not None:
        execute += '") and (format is "' + format[0]
    for form in format[1:]:
        execute += '" or format is "' + form
    execute += '") order by random() limit 100'
    cardlist = c.execute(execute).fetchall()
    for card in cardlist:
        print(card)
    conn.close()
    return cardlist


def convert_set_name(name):
    set_conversions = {u'PRM-CHP': 'CP', 'PRM-FNM': 'FNMP', 'PRM-GDP': 'MGDC', 'PRM-MSC': 'MGDC', 
                       'PRM-GWP': 'GRC', 'PRM-WPN': 'GRC', 'PRM-GPP': 'GPX', 'PRM-JSS': 'SUS', 
                       'PRM-JUD': 'JR', 'PRM-LPC': 'MLP', 'PRM-MPR': 'MPRP', 'PRM-MED': 'MBP', 
                       'PRM-PRE': 'PTC', 'PRM-PTP': 'PRO', 'PRM-REL': 'REP', 'PRM-SPO': 'UQC'}
    return set_conversions.get(name, name)


def get_total_cards(paper):
    all_info = []
    if paper:
        url = base_url + "prices/paper/"
    else:
        url = base_url + "prices/online/"

    for format in ('standard', 'modern_two', 'modern_one', 'legacy_two', 'legacy_one', 'special'):
        with urllib.request.urlopen(url + format) as html_file:
            raw_html = html_file.read()
        soup = BeautifulSoup(raw_html, "html.parser")
        sets = soup.findAll("div", {"class": "priceList-set"})
        print(len(sets))
        if format is 'standard':
            format_string = 'standard'
        elif format is 'modern_one' or format is 'modern_two':
            format_string = 'modern'
        elif format is 'legacy_one' or format is 'legacy_two':
            format_string = 'legacy'
        elif format is 'special':
            format_string = 'special'

        for set in sets:
            try:
                info = []
                rarities = []
                cards = []
                prices = []

                set_name_div = set.find('a', {"class": "priceList-set-header-link"}, href=True, text=True)
                if set_name_div:
                    set_name = convert_set_name(set_name_div['href'][7:])
                    full_set_name = set_name_div.contents[0]
                else:
                    continue
                print(set_name)

                for card in set.findAll('dt'):
                    cards.append(card.text.strip())
                    try:
                        rarities.append(card.parent.findPreviousSibling('h4').text)
                    except Exception as e:
                        print(e)
                        rarities.append('')

                for price in set.findAll("div", {"class": "priceList-price-price-wrapper"}):
                    prices.append(price.text.strip().replace(',', ''))

                if (len(cards) == len(prices) == len(rarities)):
                    set_list = [set_name] * len(cards)
                    full_set_list = [full_set_name] * len(cards)
                    format_list = [format_string] * len(cards)
                    info = zip(cards, full_set_list, set_list, prices, rarities, format_list)
                    all_info.extend(info)
                else:
                    print("There was an error with the card list not matching length of prices. There were " + str(len(cards)) + " cards and " + str(len(prices)) + " prices and " + str(len(rarities)) + " rarities.")

            except Exception as e:
                print(e)

    site_to_db(all_info)


def get_top_cards():
    url = "http://www.mtggoldfish.com/format-staples/standard/full/all"
    with urllib.request.urlopen(url) as html_file:
        raw_html = html_file.read()
    end_index = 1
    cards = []
    for i in range(50):
        first_index = raw_html.find('href="/price/', end_index)
        second_index = raw_html.find('/', first_index + 12)
        third_index = raw_html.find('/', second_index + 1)
        end_index = raw_html.find('"', third_index + 1)
        cards.append([raw_html[second_index + 1:third_index].replace('+', ' ')])
        cards[-1].append(raw_html[third_index + 1:end_index].replace('+', ' '))
    return cards


def get_image_url(card_name, card_set):
    context = ssl._create_unverified_context()
    magicInfoURL = "http://magiccards.info/query?q=" + urllib.parse.quote(card_name)
    if card_set:
        magicInfoURL += urllib.parse.quote(" e:" + card_set + "/en")
    with urllib.request.urlopen(magicInfoURL, context=context) as htmlFile:
        rawHTML = htmlFile.read()  # add error handling
        startURLIndex = rawHTML.find(b"/scans/")
        endURLIndex = rawHTML.find(b".jpg", startURLIndex)
        imageURL = "http://magiccards.info" + rawHTML[startURLIndex:endURLIndex].decode('ascii') + ".jpg"
    if imageURL == '':
        imageURL = ["../static/img/mtgback.jpg"]
    return imageURL

# getGoldfishTotalCards(True)