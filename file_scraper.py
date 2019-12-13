import os
import itertools
import pandas as pd

"""Parse text files and write to csv"""

# Parse text file
def parser(file, sep, skip_header = True, strip = ''): 
    
    with open(file) as file:
        file_contents = file.read()

        # split the string
        rows = file_contents.split(sep)

        texts = []

        iterrows = iter(rows)
        
        # skip first row (headers)
        if skip_header == True:
                next(iterrows)
                
        # strip out any trailing text
        for row in iterrows:
            # strip out trailing chars
            row = row.rstrip(strip)
            # append to new array
            texts.append(row)

        return texts
        
# Write to csv
def create_csv(array, new_path, field_names):
    
    # creating a csv writer object 
    with open(new_path, 'w') as csvfile: 
        writer = csv.writer(csvfile)
        
        # insert new headers
        writer.writerow(field_names)
        
        # extracting each data row one by one 
        idx = 0
        for element in array: 
            # writing to new csv
            writer.writerow([idx, element])
            idx += 1
            
# Scrape data from files
def scrape_files(directory = '', file_type = '.txt'):
    
    ID = []
    rating = []
    review = []
    sentiment = []

    for filename in os.listdir(directory):
        if filename.endswith(file_type): 
            ID.append(os.path.split(filename)[1].split('_')[0])
            rating.append(os.path.split(filename)[1].split('_')[1].split('.')[0])
            sentiment.append(os.path.split(directory)[0].split('/')[8])
            with open(directory + '/' + filename) as file:
                file_contents = file.read()
                review.append(file_contents)
            continue
        else:
            continue
    
    df = DataFrame({'ID':ID, 'rating':rating, 'review':review, 'sentiment':sentiment})
    
    return df
    
# Merge csv files
def merge_csv(directory = '', csv_header = '', csv_out = ''):
    
    csv_list = []
    csv_header = csv_header
    csv_out = directory + csv_out

    for filename in os.listdir(directory):
        if filename.endswith('.csv'): 
            csv_list.append(directory + filename)
    
    csv_merge = open(csv_out, 'w')
    csv_merge.write(csv_header)
    csv_merge.write('\n')
    
    for file in csv_list:
        csv_in = open(file)
    
        csv_in = iter(csv_in)
        
        # skip first row (headers)
        next(csv_in)
        for line in csv_in:
            csv_merge.write(line)
        csv_in.close()
       
    csv_merge.close()

# Convert the dataset from files to a python DataFrame
folder = 'aclImdb'
labels = {'pos': 1, 'neg': 0}
df = pd.DataFrame()
for f in ('test', 'train'):    
    for l in ('pos', 'neg'):
        path = os.path.join(folder, f, l)
        for file in os.listdir (path) :
            with open(os.path.join(path, file),'r', encoding='utf-8') as infile:
                txt = infile.read()
            df = df.append([[txt, labels[l]]],ignore_index=True)
df.columns = ['review', 'sentiment']

