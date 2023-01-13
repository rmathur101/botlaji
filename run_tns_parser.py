from PyPDF2 import PdfReader
import csv
import sys
import re
import json

all_chunks = []
new_chunk_parts = []
fonts_sizes = []
should_print_metadata = False 

# we use this as one piece of evidence to determine if a line of text is a header; just checks if the line of text starts with a number
def match_header(text):
  return re.match(r'\d.*', text)

# for more info on the visitor_body func see https://pypdf2.readthedocs.io/en/latest/user/extract-text.html
def visitor_body(text, cm, tm, fontDict, fontSize):
  # NOTE: i played around with this range in order to exlcude the header and footer of each page; leaving here for now but not using it
  # tm is a 5 element matrix that represent the vertical transaltion of the text
  # y = tm[5]
  # if y > 110 and y < 731:

    # prints out metadata of about each line of text; we use the fontSize to determine chunks of text that are likely to be headers
    if (should_print_metadata):
      print('-----------------')
      print(text) 
      print(cm)
      print(tm)
      print(fontDict)
      print(fontSize)
      print('-----------------')

    # NOTE: was using the print statement to figure out how to parse the footnotes separately according to font size, leaving this task alone for now
    # if (not(fontSize == 17.2154 or fontSize == 14.3462 or fontSize == 11.9552)):
    #   print('-----------------')
    #   print(text) 
    #   print(cm)
    #   print(tm)
    #   print(fontDict)
    #   print(fontSize)
    #   print('-----------------')

    # just storing these font sizes for inspection 
    fonts_sizes.append(fontSize)

    # these font sizes map to the big headers (e.g. "2 History as Trajectory") and small headers (e.g. "2.1 Prologue", "2.1.1 Why Hisotry is Crucial")
    if (match_header(text) and (fontSize == 17.2154 or fontSize == 14.3462)):
      # if we find a header, we want to take all subsequent text parts as one chunk; so first we add the current chunk to the all_chunks list, then we reset the new_chunk_parts list
      if (len(new_chunk_parts) > 0):
        all_chunks.append("".join(new_chunk_parts))

      new_chunk_parts.clear()  
      new_chunk_parts.append(text)
    elif (fontSize == 11.9552):
      # in this case, this is not a header, so we just add the text to the new_chunk_parts list; this particular font size excludes footnotes, and from what I can tell is generally the font sized used for text in the book
      new_chunk_parts.append(text)
      
# NOTE: leaving this code here for testing code on a single page 
# page = reader.pages[150]
# page.extract_text(visitor_text=visitor_body)
# text = "".join(visitor_body_parts)
# print(text)
# sys.exit()

# NOTE: we're starting at page 8 because the first 7 pages are just the table of contents, but if the pdf changes we'll have to check to make sure this is still the case
reader = PdfReader('tns.pdf')
for page in reader.pages[8:]:
  page.extract_text(visitor_text=visitor_body)

# convert all_chunks to a dict
all_chunks_dict = {index: chunk for index, chunk in enumerate(all_chunks)}

# write the all_chunks_dict to a json file
with open('all_chunks.json', 'w') as f:
  json.dump(all_chunks_dict, f)

# output to csv 
with open('all_chunks.csv', 'w', encoding='utf-8') as f:
    # Create a CSV writer object
    writer = csv.writer(f, escapechar='\\')
    for index, row in enumerate(all_chunks):
      writer.writerow([index, row, len(row.split(' '))])

