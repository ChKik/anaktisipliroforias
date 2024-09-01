#START OF INVERT INDEX
from genericpath import exists
from collections import defaultdict
import os
from math import log2
import numpy as np
from math import sqrt
from numpy.linalg import norm

true=True
false=False
null=None

#Flag for tf=Fi     change the flag to 1 for tf=1+logFi ||| for idf= log(N/Ni) and idf=log(1+N/Ni)
tf_choice=False  #for tf
idf_choice=False


inv_dict = defaultdict(list) #global so that the functions and the main code can have access to it
query_dict=defaultdict(list)
tf_idf_dict=defaultdict(list)
query_tf_idf=defaultdict(list)
vector_query=[]



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
            if tf_choice==False:
                values[x][1]= float(int(values[x][1])/total_words)     #Fi
            else:
                values[x][1]= float(log2(int(values[x][1])/total_words)+1)  #1+logFi


                
def find_idf(NoDocuments):
    idf_val=0.0
    for key,values in inv_dict.items():
            term_occurance=len(values)
            if idf_choice==False:
                idf_val=float(log2(NoDocuments/term_occurance))  #works,--note its log 2 not loge or log10
            else:
                idf_val=float(log2(1+(NoDocuments/term_occurance)))
            inv_dict[key].append(idf_val)


def query_idf(NoDocuments):
    idf_val=0.0
    for key,values in inv_dict.items():
            term_occurance=len(values)
            idf_val=float(log2(NoDocuments/term_occurance))  #works,--note its log 2 not loge or log10
            query_dict[key].append(idf_val)


def add_query_to_inv_doc(query,query_id):  #den prepei na epireazei ta ypoloipa alla h diadikasia einai h idia me ta ypoloipa documents.
    query_total_words=0 
    for word in query.split():
        query_total_words += 1
        word_is_unique(word,most_common_words,str(query_id),1,inv_dict)
    find_query_tf(query_total_words,str(query_id)) #isws edw thelei allagh
    find_query_idf(query_id)
    
 
def find_query_tf(total_words,doc_id):      #doulevei to tf gia to query.
    for key,values in  inv_dict.items():
        for x in range(0,len(values)):
            if values[x][0] == doc_id:
                if tf_choice==False:
                    values[x][1]= float(int(values[x][1])/total_words)     #Fi
                    temp=values[x][1]
                else:
                    values[x][1]= float(log2(int(values[x][1])/total_words)+1)  #1+logFi
                    temp=values[x][1]

                query_dict[key].append([doc_id, temp])  #afou vrei to query tf tha to valei se ksexwristo dictionary gia na kanw dot product meta


def find_query_idf(query_id):  #doulevei kai to idf. Einai oi lekseis toy query ws pros oles tis lekseis genika. dokimastike  me 3 documents gia log2(5/3) kai ebgaze swsta.
    idf_val=0.0
    for query_key,query_values in query_dict.items():
        for dict_key,dict_values in inv_dict.items():
            if query_key == dict_key:
                term_occurance=len(dict_values)
                if idf_choice==False:
                    idf_val=float(log2(query_id/term_occurance))  #works,--note its log 2 not loge or log10 . Total number of docs is the id of the query since its the last doc.
                else:
                    idf_val=float(log2(1+(query_id/term_occurance)))
                query_dict[query_key].append(idf_val)
                

#creates the dictionaries that will have the document id and the tfidf next to it.  
def create_tf_idf_dictionaries():  
    for key, values in inv_dict.items():  # for dictionary
        for x in range(len(values)):
            multiplied_values = [values[x][1] * values[len(values)-1] for x in range(len(values)-1)]    #tf(doc,term) * idf (term)
            tf_idf_dict[key] =  multiplied_values
            
    for key, values in query_dict.items(): #for query
   
            multiplied_values = [values[x][1] * values[len(values)-1] for x in range(len(values)-1)]   #tf(doc,term) * idf (term)
            query_tf_idf[key] = multiplied_values 
 
 
            
#Replaces the values before with document id and tfidf for that document to allow for creation of the vectors after that
def update_dict_values(dict1, dict2):
    results=[]
    for key in dict1:
        # Ensure the key exists in both dictionaries
        if key in dict2:
            # Iterate through the sublists in dict1
            for index, sublist in enumerate(dict1[key]):
                # Check if the sublist is a list with more than one element
                if isinstance(sublist, list) and len(sublist) > 1:
                    if index < len(dict2[key]):
                        sublist[1] = dict2[key][index]
            if isinstance(dict1[key], list) and not isinstance(dict1[key][-1], list):  #afairei ta stoixeia poy einai teleutaia kai den einai list me vash to key
                dict1[key].pop()
            
            results.append([key, dict1[key]])
    return results


#Filter out any sublist where the first element is the query id and if sublist is empty remove it
def remove_queryval_list(data, target_id):
    result = []
    for item in data:
        key = item[0]
        sublists = item[1]
        
        
        filtered_sublists = [sublist for sublist in sublists if sublist[0] != target_id and str(sublist[0]) != str(target_id)]
        
        
        if filtered_sublists:
            result.append([key, filtered_sublists])
    
    return result


def accumulate_values(query_tf_idf, updated_list):
    final_list = {}
    zero=0.0


        
    for key, values in query_tf_idf.items():
        for x in range(len(updated_list)):            
                if key == updated_list[x][0]:  # match the word if it exists
                    vector_query.append(values[0])
                    for i in range(len(updated_list[x][1])):
                        doc_id = updated_list[x][1][i][0]  #pws tha lysw na mporei na exei idio size me to  vector toy query>?? 
                        
                        val2 = float(updated_list[x][1][i][1])

                       
                        
                        if doc_id in final_list:  # if id already exists, append the value to the list
                            final_list[doc_id].append(val2)
                        else:
                            final_list[doc_id] = [val2]  # initialize with the first value
            
                    
          #   einai to 3,val kai 4,val oxi to 3 me 2 vals       
                
    
    # Convert the dictionary to a list of [doc_id, [val1, val2, ...]] pairs
    result_list = [[doc_id, values] for doc_id, values in final_list.items()]

    return result_list
            

def cosine_similarity(vector_doc,vector_query):
     # Pad vector_doc with zeros to match the length of the query vector
    padded_vector_doc = vector_doc + [0] * (len(vector_query) - len(vector_doc))

    dot_product = np.dot(padded_vector_doc, vector_query)
    
   
    norm_doc = np.linalg.norm(padded_vector_doc)
    norm_query = np.linalg.norm(vector_query)
    
   
    if norm_doc == 0 or norm_query == 0:
        return 0.0  #in the denominator case it is 0 handle the exception so that we dont get DBZ
    cosine_sim = dot_product / (norm_doc * norm_query)
    return cosine_sim


def inverted_index_printer(inv_dict):
    # #Inverted Index printer with tf values
    for key, value in inv_dict.items():
        print(f"{key}: {value}")  #Key-Word  |   DocumentNum  |   tf     |     idf
    print("Key-Word  |   DocumentNum  |   tf ")    
    inp=input("Press the enter key to continue")
    os.system('cls')
    if inp is not null:
        return 0
    
  

def VSM():
    path = "docs"
    query="Is cf mucus abnormal"
    query=query.upper()

    os.chdir(path)      #changes the path file that this code will be executed on. Redirects into the drive file of the docs or your hard drive with the docs. SET IT RIGHT
    NoDocuments=0

    for doc_num in os.listdir():  #takes one doc at a time from the doc file   
        
        total_words = 0
        file_path = f"{doc_num}"
        file_num=int(doc_num)
        with open(file_path, 'r') as f:  
                for line in f:  #takes one line at a time and split it using split() in words. Here we have one word at each line only.
                    for word in line.split(): 
                        total_words += 1
                        word_is_unique(word, most_common_words, file_num,1,inv_dict)

        #After the assignining of all the words is done we divide with the total words
        find_tf(total_words,file_num)
        NoDocuments+=1
     
        
    LastDoc=NoDocuments+1
    
    test=inverted_index_printer(inv_dict) 
    if test != 0:
        exit(0)
      
    
    add_query_to_inv_doc(query,(LastDoc))  #the last document which is the query is passed as argument

    #after all documents and terms are added we calculate idf
    find_idf(NoDocuments)


    create_tf_idf_dictionaries()
    
    
    updated_list = update_dict_values(inv_dict, tf_idf_dict)  #allazw ta float values poy itan tf twn doc me to tfidf toys.

    
    target_id = LastDoc
    updated_list = remove_queryval_list(updated_list, target_id)
    
    
    vector_doc = accumulate_values(query_tf_idf, updated_list)

   
    cosine_similarities = []

    for doc_id, doc_vector in vector_doc:
        similarity = cosine_similarity(doc_vector, vector_query)
        cosine_similarities.append((doc_id, similarity))

    # Sort the results by cosine similarity in descending order
    cosine_similarities_sorted = sorted(cosine_similarities, key=lambda x: x[1], reverse=True) #the lamba function will sort by the second argument for each tuple which is the cosine value

     # Get the top 10 results and Output the top 10 results,change the variable if you want more.
    top_results_num=10
    top__results = cosine_similarities_sorted[:top_results_num]

    print(query)
    for doc_id, similarity in top_ten_results:
        if doc_id == LastDoc:
            continue
        else:
            print(f"Cosine Similarity of document with ID {doc_id} and query: {similarity}")
                
   
if __name__ == "__main__":
    VSM()
