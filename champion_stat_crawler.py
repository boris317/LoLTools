import json
import urllib2
from lxml import html

base_url = "http://leagueoflegends.wikia.com"
champs_url = "%s/wiki/List_of_champions" % base_url
champs_file = "LOLChamps.info"

def champ_url(uri):
    return ''.join((base_url, uri))

def parse_champ_info(url):
    stats = {}
    print url
    info_table = html.parse(url).getroot().find_class('infobox')[0]
    stats_table = info_table.getchildren()[4].find("th").find("table")
    
    for tr in stats_table.getchildren():
        for skill, value in zip(tr.findall("td"), tr.findall("th")):
            stats[skill.find("*/a").text.lower()] = value.text.strip()
    if 'energy' in stats:
        #strip the hanging " (" from the energy value
        stats['energy'] = stats['energy'].split()[0]
    return stats

def crawl_champs(champ_file):
    
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
        <b><a href="/wiki/Akali" title="Akali" class="mw-redirect">Akali</a></b>
      </span>
    </td>
    """
    
    champ_stats = {}
    for row in champ_rows:
        link = row.getchildren()[0].findall("span/b/a")[0]
        champ_name = link.text.strip()
        print "Getting stats for %s" % champ_name
        try:
            champ_stats[champ_name] = parse_champ_info(champ_url(link.attrib['href']))
        except Exception, e:
            raise
            print "skipping %s..." % champ_name
            
    stream = open(champ_file, 'w')
    stream.write(json.dumps(champ_stats, indent=2))
    stream.close()
    
if __name__ == "__main__":
    crawl_champs(champs_file)
        
