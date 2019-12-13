import os
import subprocess

"""Will search for pdf files in provided directory (including sub-directories) 
    and convert to html"""
    
#----Helper Functions----#
    
# Call pdfbox jar
pdf_box = '/Users/cesar_romero/pdfbox/pdfbox-app-2.0.17.jar'

# Convert to html
def pdf_to_html(pdf_box = pdf_box, from_path = '', to_path = ''):
  subprocess.call(['java', '-jar', pdf_box, 'ExtractText', from_path, '-html', to_path])

# Get file size
def file_size(filePath):
  with open(filePath, 'r') as file:
    filename = file.read()
    len_chars = sum(len(word) for word in filename)
    return len_chars
            
#------------------------#

#---PDF conversion (using pdfbox)
def pdf_converter(dirName):
    
    # Set directory path and collect file names
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    # Loop thru files for conversion
    filCounter = 0
    failCounter = 0
    for elem in listOfFiles:
        try:
            name, file_extension = os.path.splitext(elem)
            if file_extension.lower() == '.pdf':
                new_file = name + '.html'
                pdf_to_html(from_path = elem, to_path = new_file)

                # check for conversion failure
                character_count = file_size(new_file)
                if character_count < 1:
                    failCounter += 1
                    print('conversion failure -->', new_file)
                    continue

                filCounter += 1
        except:
            print('issue converting-->', elem)
            failCounter += 1

    print(filCounter, " files converted")
    print(failCounter, " files failed to be converted")
