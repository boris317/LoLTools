import json
import os
import re
import urllib2
import traceback
from lxml import html

base_url = "http://leagueoflegends.wikia.com"
champs_url = "%s/wiki/List_of_champions" % base_url
champs_file = "champs.js"
champ_portrait_dir = "./champPortraits"

def champ_url(uri):
    return ''.join((base_url, uri))

def nullify_if_na(value):
    if value.startswith("N/A"):
        return None
    return value

def download_champ_portrait(url, champ_name):
    res = urllib2.urlopen(url)
    filename = "/".join((champ_portrait_dir, "".join((normalize(champ_name), os.path.splitext(url)[1]))))
    image = open(filename, "wb")
    image.write(res.read())
    image.close()
    res.close()

normal_re = re.compile("[\s\'\.]")
def normalize(value):    
    return normal_re.sub("", value).lower()

def parse_champ_info(url, champ_name):
    stats = {}
    print url
    info_table = html.parse(url).getroot().find_class('infobox')[0]
    stats_table = info_table.getchildren()[4].find("th").find("table")

    for tr in stats_table.getchildren():
        for skill, value in zip(tr.findall("td"), tr.findall("th")):
            stats[skill.find("*/a").text.lower()] = nullify_if_na(value.text.strip())
    if "energy" in stats:
        #Strip hanging " (" from champions with energy.
        stats["energy"] = stats["energy"].strip(" (")
    download_champ_portrait(info_table.find_class("thumbborder")[0].attrib["src"], champ_name)
    return stats

def crawl_champs(champ_file):
    if not os.path.exists(champ_portrait_dir):
        os.mkdir(champ_portrait_dir)
    print "Crawling %s" % champs_url
    champs_table = html.parse(champs_url).getroot().find_class("stdt sortable")[0]
    champ_rows = (tr for tr in champs_table.getchildren())
    #Skip header row
    champ_rows.next()
    """
    <td>
       <span style="white-space: nowrap;">
         <a href="/wiki/Akali" title="Akali">
             <img alt="AkaliSquare.png" src="http://images3.wikia.nocookie.net/__cb20100509144937/leagueoflegends/images/thumb/a/a5/AkaliSquare.png/20px-AkaliSquare.png" height="20" width="20">
         </a> 
        <span><a href="/wiki/Akali" title="Akali" class="mw-redirect">Akali</a></span>
      </span>
    </td>
    """

    champ_stats = {}
    error_log = open("crawl_champs.log", "w")

    for row in champ_rows:
        #print html.tostring(row)
        link = row.getchildren()[0].find("./span/span/a")
        champ_name = link.text.strip()
        print "Getting stats for %s" % champ_name
        try:
            champ_stats[champ_name] = parse_champ_info(champ_url(link.attrib['href']), champ_name)
        except Exception, e:
            error_log.write("Error getting %s" % champ_name)
            error_log.write(traceback.format_exc())
            print "skipping %s..." % champ_name

    print "Creating %s" % champs_file
    error_log.close()
    stream = open(champ_file, 'w')
    stream.write("championStats = " + json.dumps(champ_stats, indent=2))
    stream.close()

if __name__ == "__main__":
    crawl_champs(champs_file)
