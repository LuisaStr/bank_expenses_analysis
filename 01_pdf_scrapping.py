import pdfplumber
import pandas as pd
import re
import os

# 1. fuction to read pdf files:
# texts = []  #list in which every element is a page
def read_pdf(file_path: str) -> str:
    with pdfplumber.open(file_path) as pdf:
        texts = []
        for page in pdf.pages: 
            texts.append(page.extract_text())
        return "\n".join(texts)

# 1.1 List files in directory
file_names = os.listdir("data")

# 1.2 iterate over file names
pdfs = []
for file_name in file_names:

    # 1.3 build file path
    file_path = os.path.join("data", file_name)
    print(file_name) #control to see tht I'm iterating well
    print(file_path)
    pdf = read_pdf(file_path)
    pdfs.append(pdf)


text = "\n".join(pdfs)

print(type(text))

# 2: store pdf as txt 
#    (in order to be able to try regex syntaxt in seperate file) 

filename = "santander.txt"
encoding = "utf-8"
with open(filename, "w", encoding=encoding) as f:
    f.write(text)


# 3: create a regular expression (re) to filter out the lines needed 
#    and store them in the list (lines)
lines = []
operation_re = re.compile(r'\d{1,2}\s\w+\s\d{4}\s\w.*')
for line in text.split('\n'):
    if operation_re.match(line):
        lines.append(line)  #saving all the lines into the list (lines)
print(lines)
print(len(lines))

#4: safe the list (lines) as string and create a text file (for regex syntax)
print(type(lines))
str_lines = "\n".join(lines)

filename = "lines.txt"
encoding = "utf-8"
with open(filename, "w", encoding=encoding) as f:
    f.write(str_lines)


#5: print the first line to see that it works
row = lines[0]
print(row)

#6: build a full regex with seperate groups that will then be stores into different lists
dates=[]
concepts=[]
quantities=[]
saldos=[]

full_regex = re.compile(r'(\d{1,2}\s\w+.?\s\d{2,4})\s([\w\s.,-:*&^]+)\s(.*)')

#7: function to create different columns
for a_line in lines:
    regex_result = full_regex.match(a_line)
    date = regex_result.group(1)
    concept = regex_result.group(2)
    amount = regex_result.group(3)

    quantity = amount.split(" ")[0]
    saldo = amount.split(" ")[1]

    dates.append(date)
    concepts.append(concept)
    quantities.append(quantity)
    saldos.append(saldo)
    
#8: create a dataframe with the four columns
#   8.1: first, the diccionary with key "date" and the values as the
#        list dates created before
data_dict = {
    "date": dates,
    "concept": concepts,
    "quantity": quantities,
    "saldo": saldos
}

#   8.2: creation of the data frame
df = pd.DataFrame(data_dict)

#9: safe the columns in an excel file

df.to_excel("results/full_bank_data.xlsx", index=False)
df.dtypes

