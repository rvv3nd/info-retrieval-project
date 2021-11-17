from os import lseek
import math
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

def getClean(corpus):
    #stopwords
    new_corpus = []
    for doc in corpus:
        doc_tokenize = word_tokenize(doc)
        doc_filtere = []
        for w in doc_tokenize:
            if w not in stop_words:
                try: int(w)
                except: doc_filtere.append(w)
                    
        doc_stemme = [stemmer.stem(word) for word in doc_filtere] #se hace el stemm

        new_corpus.append(doc_stemme)
    return new_corpus

def sim(dv,qv):
    s1 = 0
    s2 = 0
    s3 = 0
    for idx in range(len(qv)):            
        s1 += dv[idx]*qv[idx]
        s2 += dv[idx]*dv[idx]
        s3 += qv[idx]*qv[idx]  
    sim_val = s1/(math.sqrt(s2)*math.sqrt(s3))
    return sim_val
#stopwords
stop_words = stopwords.words('english')                             #se eleige el idioma ingles para las stopwords
stop_words.extend([',','.',';',':','(',')','%','.W','i.e'])         #se agregan elemenots a las stopwords

#stemm
stemmer = SnowballStemmer("english") #se selecciona el idioma para el stemm

corpus = open('/Users/ruben/Desktop/RI/final/src/public/Corpus-Med500.txt','r').read().split(".I") #se abre el archivo del corpus
corpus.pop(0) #el primer elemento sale vacio así que se elimina

#query = sys.stdin.readline() #se obtiene la query
n = int(sys.argv[1])-1
query = ""
for i in range(2,2+n):
    query += sys.argv[i] + " "
# print(query)

#-----PRE-PROCESAMIENTO DE LA QUERY
#se tokeniza la query
query_tokenize = word_tokenize(query)
query_filter = []
for w in query_tokenize:#elimina stopwords
    if w not in stop_words:
        try: int(w)
        except: query_filter.append(w)
        query_filter.append(w)
query_stemme = [stemmer.stem(word) for word in query_filter] #se hace el stemm
query_ready = list(set(query_stemme)) #elimina palabras repetidas de la query

#----Se calcula el tf-idf de cada documento del corpus y de la query
corpus_cleaned = getClean(corpus) #se obtiene el corpus prepocesado
indexes = set() #set de los indices
for doc in corpus_cleaned:
    indexes.update(set(doc))

#tf-doc

tf_of_ = {w:[] for w in indexes}

for index in indexes:
    for doc in corpus_cleaned:
        apariciones = 0
        if index in doc:
            for w in doc:
                if w == index: apariciones += 1
        tf_of_[index].append(apariciones/len(doc))

#tf-query
query_tf = {w:0 for w in indexes}
for w in query_tf:
    maxi = 1
    if w in query_ready:
        apariciones = 0
        for q in query_ready:
            if q == w:
                apariciones += 1
        if apariciones > maxi : maxi = apariciones
        f = apariciones/len(query_ready)
        query_tf[w] = 0.5 + 0.5 * (f/(maxi*f))

#--idf--doc
idf_of_ = {w:[] for w in indexes}                                       #es de la forma {w:[d1,d2,d3...dn]}
for index in indexes:                                                   #obtiene las apariciones de cada index en todos los documentos
    for doc in corpus_cleaned:#
        apariciones = 0 
        if index in doc:                                                #si definitivamente no contiene la palabra queda en 0 
            for k in doc:                                               #si la incluye entonces recorre el documento para contar las apariciones
                if k == index: apariciones += 1
        idf_of_[index].append(apariciones)                              #cada indice representa un documento
                                                                        # #este for entonces se hace n_indexes * n_numero_de_documentos

N = len(corpus_cleaned)

for word in indexes:
    for i in range(len(idf_of_[word])):
        if idf_of_[word][i] != 0:
            idf_of_[word][i] = math.log(N/float(idf_of_[word][i]))

#-idf-query
query_idf = {w:0 for w in indexes}
for word in query_idf:
    if word in query_ready:
        ni = 0
        for q in query_ready:
            if q == word:
                ni += 1
        query_idf[word] = math.log(len(query_ready)/ni)
        


#---tf_idf-doc
tf_idf = {w:[] for w in indexes}
for word in tf_idf:
    for i in range (len(corpus_cleaned)):
        tf_idf[word].append(tf_of_[word][i]*idf_of_[word][i])


#---tf-idf-query
query_tf_idf = {w:0 for w in indexes}
for word in query_tf_idf:
    if word in query_ready:
        query_tf_idf[word] = query_tf[word] * query_idf[word]
        
#print(query_tf_idf)

#RECUPERACIÖN DE DOCUMENTOS MAS RELEVANTES

sim_doc = { i+400:0 for i in range(len(tf_idf)) } #dicc con los indices y el valor de similitud 

doc_vector = []
query_vector = list(query_tf_idf.values())



for i in range(N-1):
    doc_aux = []
    for word in tf_idf:
        doc_aux.append(tf_idf[word][i])
    doc_vector.append(doc_aux)

i = 0

for doc in doc_vector:
    sim_doc[i+400] = sim (doc,query_vector)
    i += 1

all_rank = sorted(sim_doc.items(), key=lambda x: x[1], reverse=True)

print(all_rank[:5])

sys.stdout.flush()
    

# print(len(tf_idf))
# print(len(query_tf_idf))
# print(len(doc_vector[0]))
# print(len(query_tf_idf))