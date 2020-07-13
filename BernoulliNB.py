import re
import math as mt

def classProb(train):
        numMan = [train[1] for train in train].count("man")
        #print(numMan)
        numWoman = [train[1] for train in train].count("woman")
        #print(numWoman)
        return numMan, numWoman

def wordsDoc(train, vocab):
        manWords = {}
        womanWords = {}
        for sentence, cla in train:
            if cla == "man":
                for word in vocab:
                    if word in sentence:
                        if word not in manWords.keys():
                            manWords[word] = 1
                        else:
                            manWords[word] += 1
            if cla == "woman":
                for word in vocab:
                    if word in sentence:
                        if word.lower not in womanWords.keys():
                            womanWords[word] = 1
                        else:
                            womanWords[word] += 1
        #print(manWords, womanWords)
        #print(len(manWords), len(womanWords))
        #print(manWords, womanWords)                    
        return manWords, womanWords

def conditionalProb(manClasses, womanClasses, train, vocab):
        manProb = {}
        womanProb = {}
        manWords, womanWords = wordsDoc(train,vocab)
        for word in vocab:
            if word in manWords.keys():
                manProb[word] = (manWords[word] + 1.)/(manClasses + 2.)
            else:
                manProb[word] = 1 / (manClasses + 2.)
            if word in womanWords.keys():
                womanProb[word] = (womanWords[word] + 1.)/(womanClasses + 2.)
            else:
                womanProb[word] = 1 / (womanClasses + 2.)
        #print(manProb, womanProb)
        return manProb, womanProb

def main():
    file_1='manV2.txt'
    file_2='womanV2.txt'
    
    with open(file_1,'r',encoding='utf-8') as m, open(file_2,'r',encoding='utf-8') as w:
        texto_m=[line.strip() for line in m]
        texto_w=[line.strip() for line in w]
    
    #Descomentar para saber el numero de documentos.
    #print(len(texto_m))
    #print(len(texto_w))
    
    train=[(i,'man') for i in texto_m]+[(j,'woman') for j in texto_w]
    
    #test=[('Religiosidad instantánea: Ante la muerte de Dios, la gente busca sus preceptos morales en los memes y estados de su influencer favorito.','man'),]
    test=[('Tenía todo lo que me enseñaron que sería la felicidad, buenas calificaciones, amigos, amor, estabilidad mediocre. Te entregué mi amor y en la confianza de hacerlo te di mi cuerpo. Te mostré quién era en la oscuridad, en la luz y entre sombras. Te di lo mejor de mí y murmurabas hacer lo mismo.','woman'),]
    
    corpus=[]; longString = ''
    for words, cla in train:
        word_list = [word.lower() for word in re.findall(r'[A-Za-záéíóúñ]+', words) if len(word)>3]
        corpus.append((' '.join(word_list), cla))
    train=corpus
    
    for text in train:
        longString += text[0].lower() + ' '
    #print(longString)
    vocab = set(re.findall(r'[a-záéíóúñ]+', longString))
    
    manClasses, womanClasses = classProb(train)
    totalSentences = manClasses + womanClasses
    probabilityMan = manClasses / float(totalSentences)
    probabilitywoman = womanClasses / float(totalSentences)
    manProb, womanProb = conditionalProb(manClasses, womanClasses, train, vocab)
    
    testSet = [sentence[0] for sentence in test]
    for sentences in testSet:
        result = {}
        sentences = re.findall(r'[A-Za-záéíóúñ]+', sentences.lower())
        result["man"] = mt.log10(probabilityMan)
        result["woman"] = mt.log10(probabilitywoman)
        for word in vocab:
            #print(result)
            if word in sentences:
                result["man"] += mt.log10(manProb[word])
                result["woman"] += mt.log10(womanProb[word])
            else:
                result["man"] += mt.log10((1 - manProb[word]))
                result["woman"] += mt.log10((1 - womanProb[word]))
    
    return "MAN" if result["man"] > result["woman"] else "WOMAN"
    #print(classProb(train))
    #print(wordsDoc(train, vocab))

r = main()
print(r)


