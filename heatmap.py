from os import lseek
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import sys
import operator

TOP = 10 #es el numero de palabras que se mostrarán al final
corpus = open('Corpus-Med500.txt','r').read().split(".I") #se abre el archivo
corpus.pop(0) #se elimina el  primer elemento que esta vacio
# print(len(corpus)) #num de documentos en el corpus

added_words = [',','.',';',':','(',')','%','.W']#se agregan estos simbolos a las stopwords
stop_words = stopwords.words('english') #se eleige el idioma ingles para las stopwords

stop_words.extend(added_words)    #lista final de stopwords

bag_of_words = {} #diccionario que lleva la palabra como key y su numero de apariciones como value
clean_corpus = [] #lista que contiene los documentos preprocesados sirven para la parte del mapa de calor

print('working on it...')
for doc in corpus:

    word_tokens = word_tokenize(doc) #se tokeniza el doc del corpus

    # filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words] #ELIMINA MAYUSCULAS #PERO EL CORPUS YA ESTABA SIN MAYUSCULAS XD

    filtered_sentence = []

    documento_id = word_tokens[0] #se guarda el id del documento 
    word_tokens.pop(2)
    for w in word_tokens:
        if w not in stop_words:
            try: int(w)
            except: filtered_sentence.append(w)
    #se agregan las palabras que no sean stopword y que no sean enteros        


    #print(f'id: {documento_id}')
    #print(filtered_sentence[1::])

    stemmer = SnowballStemmer("english") #se selecciona el idioma para el stemm
    stemmed_words = [stemmer.stem(word) for word in filtered_sentence] #se hace el stemm
    #print(stemmed_words)
    clean_corpus.append(stemmed_words)
    for w in stemmed_words:
        if w in bag_of_words:
            bag_of_words[w] += 1 #si ya existe el conteo aumenta en uno
        else: 
            bag_of_words[w] = 1 #si no esta en la bolsa se palabras (i.e es nueva) se inicia su conteo

    #total_words = len(bag_of_words)

    # print(total_words)

sorted_bag_of_words = sorted(bag_of_words.items(), key=lambda x: x[1], reverse=True)

final_list = sorted_bag_of_words[0:TOP]
#print(final_list)

h_word = [x[0] for x in final_list] #las TOP palabras mas comunes 
# print(h_word) 
h_docs = list(range(400, 400+len(clean_corpus))) #los documentos
h_value = []

for w in h_word:
    values = []
    for doc in clean_corpus:
        c = Counter(doc)
        values.append(c[w])
    h_value.append(values)
h_value = np.array(h_value)
print(h_value)


fig, ax = plt.subplots()

im = ax.imshow(h_value)

# We want to show all ticks...
ax.set_xticks(np.arange(len(h_docs)))
ax.set_yticks(np.arange(len(h_word)))
# ... and label them with the respective list entries
ax.set_xticklabels(h_docs)
ax.set_yticklabels(h_word)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(h_word)):
    for j in range(len(h_docs)):
        text = ax.text(j, i, h_value[i, j],
                       ha="center", va="center", color="w")


fig.set_size_inches(200,30)
fig.tight_layout()
plt.savefig("./heat-maps/heat-map.png", dpi = 200)
