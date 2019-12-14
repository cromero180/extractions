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

# Extract sections
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
#     sub = remove_html_tags(sub)
#     sub = remove_line_breaks(sub)
#     sub = remove_trailing_chars(sub)    
    
#     header = remove_html_tags(header)
#     header = remove_line_breaks(header)
    # Remove trailing spaces
#     header = header.strip()
    
    return sub, header, end

# Extract sentences
def extract_sent(corpus = '', 
                    search_term = '', 
                    start_sent_tag = '', 
                    end_sent_tag = '', 
                    final_sent_tag = '',
                    final_sent_tag_1 = ''):
        
    # Extract start tag up to search term
    match = re.search(start_sent_tag + '(.*?)' + search_term, corpus, re.DOTALL)
    sent_start = match.group(0)

    # Get start tag index
    start = corpus.find(sent_start)

    # Extract search term up to end tag
    match = re.search(search_term + '(.*?)' + end_sent_tag, corpus, re.DOTALL)
    sent_end = match.group(0)

    # Get end tag index
    end = corpus.find(sent_end) + len(sent_end)

    # Isolate sentence
    sent = corpus[start:end]
    rev = sent[::-1]

    # Narrow down to last instance of start tag
    match = re.search(final_sent_tag + '(.*?)' + final_sent_tag_1, rev, re.DOTALL)
    sent = match.group(0)
    sent = sent[::-1]
        
    return sent, end

#----Driver Script----#

# Search parameters
search_term = 'replace'
start_tag = '\n<p><b>\d'
end_tag = '\n<p><b>\d'
final_tag = '\d>b<>p<\n'
start_sent_tag = '<p>'
end_sent_tag = '</p>'
final_sent_tag = '>p/<'
final_sent_tag_1 = '>p<'

# List to hold results
secs = []
headers = []
sents = []

# Tally relevant returns of section
sec_cnt = len(re.findall(search_term + '(.*?)' + end_tag, raw, re.DOTALL))

# Loop thru corpus to gather relevant sections
for s in range(sec_cnt):
    
    # Extract section
    sub, header, end = extract_sections(corpus = raw, 
                                        search_term = search_term, 
                                        start_tag = start_tag, 
                                        end_tag = end_tag, 
                                        final_tag = final_tag)
    
    # Update results
    secs.append(sub)
    headers.append(header)
    
    # Tally relevant returns of search term
    term_cnt = len(re.findall(search_term + '(.*?)' + end_sent_tag, sub, re.DOTALL))

    for t in range(term_cnt):
        
        # Extract sentence
        sentence, sent_end = extract_sent(corpus = sub, 
                                search_term = search_term, 
                                start_sent_tag = start_sent_tag,
                                end_sent_tag = end_sent_tag,
                                final_sent_tag = final_sent_tag,
                                final_sent_tag_1 = final_sent_tag_1)
        
        # Update sent results
        sents.append(sentence)
        
        # Reset starting point
        sub = sub[sent_end-5:]
        t += 1
    
    # Reset starting point
    raw = raw[end-9:]
    s += 1
