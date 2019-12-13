import re

"""Extract searched keywords with surrounding context"""


#----Helper Functions----#

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_line_breaks(text):
    """Remove line terminators from a string"""
    clean = re.compile('\n')
    return re.sub(clean, '', text)

def remove_trailing_chars(text):
    """Remove trailing_chars from a string"""
    rev = text[::-1]
    new = rev[rev.find('.'):len(rev)]
    return new[::-1]

#------------------------#

# Driver script
def extract_sections(corpus = '', search_term = '', start_tag = '', end_tag = '', final_tag = ''):
        
    # Extract start tag up to search term
    match = re.search(start_tag + '(.*?)' + search_term, corpus, re.DOTALL)
    text_start = match.group(0)
        
    # Get start tag index
    start = corpus.find(text_start)

    # Extract search term up to end tag
    match = re.search(search_term + '(.*?)' + end_tag, corpus, re.DOTALL)
    text_end = match.group(0)
        
    # Get end tag index
    end = corpus.find(text_end) + len(text_end)

    # Isolate section
    sub = corpus[start:end]
    rev = sub[::-1]

    # Narrow down to last instance of start tag
    match = re.search(final_tag + '(.*?)' + final_tag, rev, re.DOTALL)
    sub = match.group(0)
    sub = sub[::-1]

    # Pull header
    match = re.search('<b>(.*?)\n', sub, re.DOTALL)
    header = match.group(0)

    # Clean up text
    sub = remove_html_tags(sub)
    sub = remove_line_breaks(sub)
    sub = remove_trailing_chars(sub)    
    
    header = remove_html_tags(header)
    header = remove_line_breaks(header)
    # Remove trailing spaces
#     header = header.strip()
    
    return sub, header, end
