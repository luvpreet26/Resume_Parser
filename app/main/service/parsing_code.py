#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Luvpreet)s
"""

import docx2txt
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk import pos_tag
import nltk
from nltk.corpus import conll2000
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.chunk import ne_chunk
from nltk import pos_tag
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer 


## Extracting Text from Document as paragraph
def extract_text_from_doc(doc_path):
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)

## Extracting Text from document as lines
def extract_text_from_doc_lines(doc_path):
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return '\n '.join(text)

# Extracting phone no from string using regular expression
def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

# Extracting email from strings
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)


def parsing(file_name):  
    text = extract_text_from_doc(file_name)
    text_new = extract_text_from_doc_lines(file_name)    
    ne_tree = ne_chunk(pos_tag(word_tokenize(text)))
    first_name = ne_tree[0]
    last_name = ne_tree[1]        
    
    words = word_tokenize(text)
    words = [i.lower() for i in words]
    
    import pandas as pd
    from sqlalchemy import create_engine  
    #Reading from table
    engine = create_engine('postgresql+psycopg2://postgres:localhost:5432/resumeDB')
    dataset = pd.read_sql_table("skill_master",engine)
    
    skills = dataset.iloc[:,1].values
    skills = list(skills)
    
    
    x = [i for i in words for j in skills if i == j]
    
    x = pos_tag(x)
    y = []
    for i in x:
        if i[1] == 'NN':
            y.append(i[0])
    #print(y)
    y = list(set(y))
    #print(y)
    
    if type(first_name[0]) is tuple:
        first_name = first_name[0][0]
    else:
        first_name = first_name[0]
    if type(last_name[0]) is tuple:

       last_name = last_name[0][0]
    else:

       last_name = last_name[0]
   
       
    phone_no = extract_phone_numbers(text)
    email_id = extract_email_addresses(text)
    
    #print("skills",y)
    total_skills = [i for i in y if len(i) >2]
    #print(total_skills)
    
    ####Eductation

    
    sentence_list = nltk.sent_tokenize(text_new) 
    x =[el.strip() for el in text_new.split("\n") if len(el)>0]
    
    x = [i.lower() for i in x]
    found = False
    edu_forms = ['education', 'educational', 'educate', 'Education', 'educationist', 'educationalist','qualifier', 'qualification', 'quality', 'qualifying', 'qualify']
    edu_forms = [i.lower() for i in edu_forms]
    for i in x:
        l = word_tokenize(i)
        for j in edu_forms:
            if j in l:  
                index = x.index(i)
            
       
    m = x[index+1:]
    for i in m:
        l = word_tokenize(i)
        if len(l) > 2:
            new_index = x.index(i)

    education_data = x[index+1:new_index]
    
    education_data = education_data[0:20]
    
    tokenize_edu_data = []
    ##Tokenizing education_data
    for i in education_data:
        tokenize_edu_data.append(word_tokenize(i))
    #####DEGREE
    types_of_degree = ['Bachelor','Bachelor','Masters','Master','Undergraduate','Under-graduate','degree']
    types_of_degree = [i.lower() for i in types_of_degree]
    
    degree = []
    for i in education_data:   
        for j in types_of_degree:
            if j in i or j == i:    
                degree.append(j)
            else:
                pass
    
    
    
    #####Qualification 
    qual = []
    qualification_search =  [
                'M.TECH', 'MTECH', 
                'ME', 'M.E', 'M.E.', 'MS', 'M.S', 'MSC','M.SC','m.com','mcom','b. com',
                'BE','B.E.', 'B.E', 'BS', 'B.S','B.com','bcom',        
                'BTECH', 'B.TECH', 
                'SSC', 'HSC','X', 'XII','B.SC','BSC','10th','12th','puc','sslc','secondary'
            ]
    new_qual = []
    qualification_search = [i.lower() for i in qualification_search]
    for i in tokenize_edu_data:
        for j in qualification_search:
            if j in i or i == j:
                qual.append(j)
              
   # print(new_qual)
    #print(qual)
    import re
    if len(degree) == 0:
        for i in qual:
            res = len(re.findall(r'm+', i))
         #   print(i)
            if res == 1:
                degree.append('masters')
            res2 = len(re.findall(r'b+', i))
            if res2 == 1:
                degree.append('bachelors')
            else:
                degree.append('under-graduate')
    #print(degree)
    college =[]
    university= []
    start_date = []
    end_date = []
    line = []
    for i in education_data:
        l = word_tokenize(i)
       # print(l)
        if 'college' in i or 'school' in i or 'institute' in l:
            college.append(i)
        if 'university' in i:
            university.append(i)
        if re.search(r'\b[21][09][8901][0-9]',i.lower()):
            year = re.findall(r'\b[21][09][8901][0-9]',i.lower())
            line.append(' '.join(year))
        
    for i in line:
        if len(i) > 4:
            dates = i.split()
            start_date.append(dates[0])
            end_date.append(dates[1]) 
    if len(start_date) == 0 or len(end_date) == 0:
        pass
    if len(line)<=len(degree):
        end_date = line
    if len(line)>len(degree):
        k = len(degree)
        end_date = line[:k]
    
    school_type = []
    for i in college:
        if ',' in i:
            c_split = i.split(',')
            school_type.append(c_split[0])
        else:
            school_type = college
    """print(line)
    
    print("degree",list(set(degree)))        
    print("qualification",list(set(qual)))
    print("start_date",start_date)
    print("end_date",end_date)
    print("school-type",school_type)
    print("university",university)"""
    
    #employment 
    
    emp_forms = ["experience","employment", "carrer overview","WORK EXPERIENCE"]
    emp_forms = [i.lower() for i in emp_forms]
    for i in x:
        l = word_tokenize(i)
        for j in emp_forms:
            if j in l or j in i:  
                index_found = x.index(i)
             #   if len(i[index]) == 1 or len(i[index]) == 2:
                total_words = x[index_found].split(" ")
                #print(total_words)
                if len(total_words) == 1 or len(total_words) == 2:
                    index = index_found
                   # print(index)
                    
    m = x[index+1:]
    edu_forms = ['education','qualification','skills','personal information']
    
    n_index = 0
    edu_forms = [i.lower() for i in edu_forms]
    for i in m:
        l = word_tokenize(i)
        if len(l) > 2:
            new_index = x.index(i)
        else:
            for j in edu_forms:
                if j in l:  
                    n_index = x.index(i)
                break 
          #  print(new_index)
    employment_data = x[index:new_index]
    
    
    #print(n_index)
    if n_index == 0:
       emp_data = employment_data
    else:
       emp_data = x[index+1:n_index-1]
    
    if len(emp_data) == 0:
       emp_data = employment_data 
    #print(emp_data)
    company_forms = ['company','corporation','consulting','services','oranization','pvt','limited','college','organization','consultants','institute','state','india']
    position = ["developer","engineer","senior","professor","lecturer","consultant","associate","consultant."]
    certificate = ["certified","certification"]
    com = []
    dates = []
    positions = []
    certifications = []
    for i in emp_data:
        l = word_tokenize(i)
        for j in company_forms:
            if j in l:
                com.append(i)
        if re.search(r'\b[21][09][8901][0-9]',i.lower()):
            year = re.findall(r'\b[21][09][8901][0-9]',i.lower())
            dates.append(' '.join(year))
        for j in position:
            if j in l:
              #  print(i)
                l_spaces_removed = i.replace(" ", "")
                length = i.split(" ")
              #  print(length)
                if len(length) < 7:
                    positions.append(i)
                else:
                    ind = length.index(j)
                    #print(ind)
                   # print(ind)
                    p = length[ind-1] + " "+ length[ind]
                    #print(p)
                    positions.append(p)
        for j in certificate:
            if j in l:
                certifications.append(i)
        if 'till' in l or 'current' in l:
            found = 'yes'
        else:
            found = 'no'
    com = list(set(com))
    companies = []
     
    positions_occupied = []      
    for i in com:
        sp = i.split(",")
       # print(sp)
        if len(sp) <= 12:
            companies.append(i)
    
                    
    removable_companies = []
    for i in companies:
        sp = i.split(" ")
        if "handled" in sp or "worked" in sp:
           companies.remove(i)
       
    #print(companies)        
    
    #print(dates)
    #print(positions)
    
    #print(certifications)
    
    total = []
    currentYear = datetime.now().year
    for i in dates:
        t = i.split(' ')
        total.append(t)
        
    if len(total[0]) == 1:
        total[0].append(str(currentYear))
    
    if len(total[-1]) == 1:
        element = total[-1]
        if len(total[-2]) == 1:
            total[-2].append(' '.join(total[-1]))
            total.remove(element)
        else:
            total.remove(element)
    #print(total)
    
    for i in total:
        if len(i) == 1:
            ind = total.index(i)
            if len(total[ind]) == len(total[ind+1]):
                total[ind].append(' '.join(total[ind+1]))
                element = total[ind+1]
                total.remove(element)
    #print(total)        
    total_exp = 0
    #print(total)
    for i in total:
        if len(i) == 1:
            pass
        else:
            val = int(i[1]) - int(i[0])
            total_exp += val
    print(total)
    emp_start_date = []
    emp_end_date = []
    for i in total:
        if len(i) >=2:
            emp_start_date.append(i[0])
            emp_end_date.append(i[1]) 
        else:
            emp_end_date.append(i[0])
    
    if len(emp_start_date) == 0 or len(emp_end_date) == 0:
        pass
    for i in x:
        l = word_tokenize(i)
        for j in certificate:
            if j in l:
                certifications.append(i)
    
    #print(total)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    parsed_resume = {
            "first_name":first_name,
            "last_name":last_name,
            "phone_no": phone_no,
            "email_id":email_id,
            "skills":total_skills,
            "education": {
                    "degree":list(set(degree)),
                    "qualification":list(set(qual)),
                    "start_date":start_date,
                    "end_date":end_date,
                    "school-type":school_type,
                    "university":university
                    },
            "employment":{
                    "companies":companies,
                    "dates":total,
                    "start_date":emp_start_date,
                    "end_date":emp_end_date,
                    "positions":positions,
                    "total_exp":abs(total_exp)
                    },
            "certification":list(set(certifications))
                
            }
    
    
   # print(parsed_resume)
    return(parsed_resume)
    
#data = parsing("luvpreet_ml.docx")
#print(data)