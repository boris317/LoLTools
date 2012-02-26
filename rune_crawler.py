from lxml import html

runes_url = "http://leagueoflegends.wikia.com/wiki/List_of_Runes"

class StatName(str):
    is_per_level = False

def crawl_runes(rune_table):
    rows = (row for row in rune_table)
    #skip header row
    rows.next()
    
    runes = {}
    rune_name = None
    stat_name = None
    for i, row in enumerate(rows):
        row_num = i+1
        if row_num == 1 or (row_num - 1) % 4 == 0:
            rune_name = row[0].find("b").text.strip()
            stat_name = get_stat_name(row[0].find("p").text_content())
            rune_type = row[1].text.strip()
            runes[rune_name] = {"stat": stat_name, "runes": {}} 
        else:
            rune_type = row[0].text
        runes[rune_name]["runes"][rune_type] = row[-1].text.strip()
    return runes
        
    
def get_rune_table(tree):
    return tree.getroot().get_element_by_id("WikiaArticle").find("table")

def get_stat_name(text_content):
    if "per level" in text_content:
        # strip out the string "per level" as well as parens and the line break.
        is_per_level = True
        parts = text_content[1:-2].split()[0:-2]
    else:
        # strip out parens and the line break.
        parts = text_content[1:-2].split()
        is_per_level = False
    #normalize "stat / N sec" "into StatPerNSec"
    if "/" in parts:
        parts[-3] = "per"
    
    cammel_case = []
    cammel_case.append(parts[0].lower())
    for part in parts[1:]:
        cammel_case.append(part.capitalize())
        
    stat_name =  StatName("".join(cammel_case))
    stat_name.is_per_level = is_per_level
    return stat_name

runes = crawl_runes(get_rune_table(html.parse(runes_url)))