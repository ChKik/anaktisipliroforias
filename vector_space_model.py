#START OF INVERT INDEX
from genericpath import exists
from collections import defaultdict
import os
from math import log2
import numpy as np

true=True
false=False
null=None

#Flag for tf=Fi     change the flag to 1 for tf=1+logFi.
tf_flag=False


inv_dict = defaultdict(list) #global so that the functions and the main code can have access to it
query_dict=defaultdict(list)

#According to WikiPedia the 50 most common words in english are :
most_common_words = [
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I',
    'IT', 'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT',
    'THIS', 'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE',
    'OR', 'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT',
    'SO', 'UP', 'OUT', 'IF', 'ABOUT', 'WHO', 'IS'
]


#it removes the top 50 most common words in english according to WikiPedia that would add no value,
#so that the inverted index for 1209 docs consumes less space overall.

#words are placed in the dictionary as key->word,value->docs,num of times seen
def word_is_unique(word, checklist, doc_id, count,dict_arg):
    if word not in checklist:
        # Check if the word is already in the dictionary using the next iterator that returns true if it finds the word in the dict,else None
        word_update = next((entry for entry in inv_dict[word] if entry[0] == doc_id), None)

        if word_update:
            word_update[1] += count
        else:
            inv_dict[word].append([doc_id, count])  



def find_tf(total_words,doc_id):
  for key,values in  inv_dict.items():
    for x in range(0,len(values)):
      if values[x][0] == doc_id:
            if tf_flag==False:
                values[x][1]= float(int(values[x][1])/total_words)     #Fi
            else:
                values[x][1]= float(log2(int(values[x][1])/total_words)+1)  #1+logFi

def find_query_tf(total_words,doc_id):
  for key,values in  inv_dict.items():
    for x in range(0,len(values)):
        if values[x][0] == doc_id:
            if tf_flag==False:
                values[x][1]= float(int(values[x][1])/total_words)     #Fi
                temp=values[x][1]
            else:
                values[x][1]= float(log2(int(values[x][1])/total_words)+1)  #1+logFi
                temp=values[x][1]

            query_dict[key].append([doc_id, temp])  #afou vrei to query tf tha to valei se ksexwristo dictionary gia na kanw dot product meta

                
def find_idf(NoDocuments):
    idf_val=0.0
    for key,values in inv_dict.items():
            term_occurance=len(values)
            idf_val=float(log2(NoDocuments/term_occurance))  #works,--note its log 2 not loge or log10
            inv_dict[key].append(idf_val)

def query_idf(NoDocuments):
    idf_val=0.0
    for key,values in inv_dict.items():
            term_occurance=len(values)
            idf_val=float(log2(NoDocuments/term_occurance))  #works,--note its log 2 not loge or log10
            query_dict[key].append(idf_val)


def add_query_to_inv_doc(query,query_id):  #den prepei na epireazei ta ypoloipa alla h diadikasia einai h idia me ta ypoloipa documents.
    query_total_words=0 
    print(type(query_id))
    for word in query.split():
        query_total_words += 1
        print(word)
        word_is_unique(word,most_common_words,str(query_id),1,inv_dict)
        find_query_tf(query_total_words,str(query_id))
 


    


def VSM():
    path = "docs"
    query="Is CF mucus abnormal"
    query=query.upper()

    os.chdir(path)      #changes the path file that this code will be executed on. Redirects into the drive file of the docs
    NoDocuments=0

    for file_num in os.listdir():  #takes one doc at a time from the doc file   
        
        total_words = 0
        file_path = f"{file_num}"
        with open(file_path, 'r') as f:  
                for line in f:  #takes one line at a time and split it using split() in words. Here we have one word at each line only.
                    for word in line.split(): 
                        total_words += 1
                        word_is_unique(word, most_common_words, file_num,1,inv_dict)

        #After the assignining of all the words is done we divide with the total words
        find_tf(total_words,file_num)
        NoDocuments+=1
        if NoDocuments==4: #FOR TESTING ONLY 4 DOCUMENTS
            break
        
    LastDoc=NoDocuments+1
    add_query_to_inv_doc(query,(LastDoc))  #the last document which is the query is passed as argument


    #after all documents and terms are added we calculate idf
    find_idf(NoDocuments)


    #Inverted Index printer with tf values
    for key, value in inv_dict.items():
        print(f"{key}: {value}")  #Key-Word  |   DocumentNum  |   tf     |     idf
    
    
    

    for key, value in query_dict.items():
        print("Dictionary")
        print(f"{key}: {value}")  #Key-Word  |   DocumentNum  |   tf     |     idf


if __name__ == "__main__":
    VSM()
    