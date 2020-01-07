import re
import os
import pandas as pd

"""Surface certain sections from SEC 10-K"""


#----Helper Functions----#

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_brackets(text):
    """Remove brackets from a string"""
    text = re.sub('<','',text)
    text = re.sub('>','',text)
    return text

def extract_toc(text, 
    start_tag = 'href=(.*?)><(.*?)>(.*?)risk factors(.*?)</font>', 
                end_tag = '<a name="' + '(.*?)' + '>'):
    """Extract TOC from imported file btw first href and 
    first bookmark (by default)"""

    match = re.search(start_tag + '(.*?)' + end_tag, lower, re.DOTALL)
    toc = match.group(0)
    
    return toc
    
def extract_toc_links(toc):
    """Stratify table of contents into list of chapters 
    by extracted hyperlinks"""

    item_cnt = len(re.findall('href=(.*?)>\d.*?<', toc, re.DOTALL))

    chapters = []
    # Loop thru TOC
    for s in range(item_cnt):

        # Extract chapter
        match = re.search('href=(.*?)>\d.*?<', toc, re.DOTALL)
        chapter = match.group(0)

        # Get chapter end index
        end = toc.find(chapter) + len(chapter)

        # Update chapter list
        chapters.append(chapter)

        # Reset toc starting point
        toc = toc[end:]
        s += 1
    
    return chapters

def get_bookmark(chapters, chapter):
    """Return bookmark for given chapter based on 
    extracted chapter hyperlinks"""
    
    for c in range(len(chapters)):
        try:
            sec = chapters[c]
            rev = sec[::-1]
            
            # Get title
            match = re.search('>(.*?)' + chapter + '(.*?)</font>', sec, re.DOTALL)
            title_match = match.group(0)
            title_clean = remove_html_tags(title_match)
            title_clean = ''.join([l for l in title_clean if l not in ['#','&',';','<','>']])
            title_final = title_clean.strip()

            # Get page link
            match = re.search('<(\s*?)\d+?(\s*?)>(.*?)=ferh', rev, re.DOTALL)
            pg_link_rev = match.group(0)
            pg_link = pg_link_rev[::-1]
            pg_link_final = pg_link[pg_link.find("#")+1:pg_link.find(">")]
            
            break
            
        except:
            continue
            
    return '<a name="' + pg_link_final
    
def extract_section(bookmark, end_tag, text):
    """Extract relevant section based on bookmarks"""
    
    match = re.search(bookmark + '(.*?)' + end_tag, text, re.DOTALL)
    return match.group(0)
    
def get_latest_files(directory):
    """Pull latest file from each sub-directory"""

    files = []
    
    it = iter(os.walk(directory))
    next(it, None)  # skip first item.
    for x in it:
        org_folder = x[0]
        list_of_files = os.listdir(org_folder)
        list_of_files.sort(reverse = True) 
        latest_file = list_of_files[0]
        files.append(org_folder + '/' + latest_file)

    return files
    

#----Driver Script----#

directory = "~/Documents/Kaggle/data_challenge/10K"

chap_start = 'business'
chap_end = 'risk factors'

# Gather latest rpts from each org
reports = get_latest_files(directory)

org = []
file_name = []
text = []

# Loop thru reports
for report in reports:
    
    # Read file and lower-case its text
    raw = open(report).read()
    lower = raw.lower()

    try:
        # Extract TOC from text
        toc = extract_toc(lower)

        # List TOC chapters according to hyperlinks 
        chapters = extract_toc_links(toc)

        # Extract bookmarks for given chapters
        bookmark_1 = get_bookmark(chapters, chap_start)
        bookmark_2 = get_bookmark(chapters, chap_end)

        # Extract relevant text
        results = extract_section(bookmark_1, bookmark_2, lower)
        results = remove_html_tags(results)

        org.append(os.path.split(report)[0].split('/')[7])
        file_name.append(report)
        text.append(results)
    except:
        print('Failed on ' + report)
        continue

df = pd.DataFrame({'org_name':org, 'file':file_name, 'text':text})
