import string
from math import *


N = 4
def get_N():
    return N

k = 1
freq = {} #dict vide
listcar = {".", ",","'"}
stoplist = open('stopwords_fr.txt','r')
stoplist = stoplist.read()
stoplist = stoplist.lower()
stoplist = stoplist.split()

while(k <= N):
    #print("------------------------Indexe de fréquences du document",k,"-------------------")
    f = open('TPRI/D'+str(k)+'.txt','r')
    t =f.read()
    t =t.lower()
    i=0
    while(i<len(t)):
        if(t[i] in listcar):
            t=t.replace(t[i]," ")
        i += 1
    a=t.split()
    nb=len(a)
    for w in a:
        if( w not in stoplist and len(w)>1):
            if( (w,k) not in freq):
                freq[w,k] = a.count(w)
                #print(w,freq[w,k])
    k += 1
    f.close()

def get_freq():
    return freq
'''
print("Le fichier inverse de la collection ")
for word in freq :
    print(word, " => ", freq[word])
'''

def indexdoc(freq,d): # Recherche pour doc NON pondéré
    res = {}
    #print("l'index du Document ",d," est")
    for(a,b) in freq:
        if(b==d):
            res[a] = freq[a,d]
            #print(a,':',freq[a,d])
    return res

def indexmot(freq,w):  # Recherche pour terme NON pondérée
    res = {}
    #print("l'index du mot ",w," est")
    for(a,b) in freq:
        if(a==w):
            res[b] = freq[w,b]
            #print(b,':',freq[w,b])
    return res
"""
#appel des fonctions
d=int(input("Donner le numéro du document "))
indexdoc(freq,d)

w=input("Donner un mot ")
w=w.lower()
indexmot(freq,w)
"""

## Calcul de ni(nbr docs ou il apparait) pour chaque mot dans freq
ni={}
for(w,d) in freq:
    if(w not in ni):
        ni[w]=1
    else: ni[w]=ni[w]+1

## Calcul de la fréquence max de chaque docs (max colonne)
max={}
for(w,d) in freq:
    if(d not in max):
        max[d]=freq[w,d]
    else:
        if(freq[w,d]>max[d]): max[d]=freq[w,d]

## Calcul du fichier inverse avec poids TF*IDF
poids={}
for(w,d) in freq:
    poids[w,d]=(float(freq[w,d])/max[d]) *log10((float(N)/ni[w])+1)
    
def get_poids():
    return poids

'''
print("------------Le fichier des poids TF*IDF---------")
for (w,d) in poids :
    print("( ",w," , ",d," )","==>",poids[w,d])
'''

# input= indexe(num docs) / Output: mot(w), poids(poids[w,d]
def indexdocPoids(poids,d): # Recherche pour doc pondérée
    res = {}
    #print("L'index pondere du document ",d," est")
    for(a,b) in poids:
        if(b == d):
            res[a] = poids[a,d]
            #print(a," : ",poids[a,d])
    return res

# input= mot / Output: index des docs ou il apparait(d), poids(poids[w,d]
def indexmotPoids(poids,w): # Recherche pour terme pondérée
    res = {}
    #print("Les poids du mot ",w," sont")
    for(a,b) in poids:
        if(a == w):
            res[b] = poids[w,b]
            #print(b," : ",poids[w,b])
    return res

"""
#appel des fonctions
d=int(input("Donner le numéro du document "))
indexdocPoids(poids,d)

w=input("Donner un mot pour afficher ses poids ")
w=w.lower()
indexmotPoids(poids,w)
"""

#MODELE BOOLEEN
def modele_booleen(requete):
    # modèle booleèn
    requete=requete.lower()
    separateur=['and','or','not','(',')']
    listreq=requete.split()
    print(listreq)
    boolreq=""
    autorizeddoc=[]
    bool=0
    for doc in range(1,N+1):
        boolreq=""
        for terme in listreq:
            if terme not in separateur:
                for (a,b) in freq:
                    if(a == terme and b== doc):
                        boolreq += "\t1"
                        bool=1
                if bool==0:
                    boolreq += "\t0"
                else: bool=0
            else:  boolreq += "\t"+terme
        print(boolreq)
        #result=eval(boolreq)
        
        try:
            res = eval(boolreq)
            if(res==1):    
                autorizeddoc.append(doc)
            print("Result is", res)
            b = True
         
        except SyntaxError:
            print("Wrong syntax")
            b = False
            res = 0
            break
        else:
            print("No exceptions")
         
        finally:
            print("This will execute no matter what")
        print("doc= ",doc,"resultat= ",res)
    print("docs autorisés",autorizeddoc)
    return autorizeddoc,b

"""
requete=input("Entrer requete")
modele_booleen(requete)
"""

def nettoyer_requete(req):
    i=0
    result=[]
    while (i < len(req)):
        if (req[i] in listcar): # caractère spéciale
            req = req.replace(req[i], " ")
        i += 1
    a = req.split()
    nb = len(a)
    for w in a:
        if (w not in stoplist and len(w) > 1):
            result.append(w)
    return result

#requete: termes, lower, ponctuation, mots vides
#MODELE VECTORIEL
def produit_interne(listreq):
    print("PRODUIT INTERNE")
    autorizeddoc = {}
    for doc in range(1, N + 1):
        produit = 0.0
        for terme in listreq:
            for (a,b) in poids:
                if (a == terme and b == doc):
                   produit += poids[terme,doc]#poids(ti,dji)* poids(ti,Qk)==>poids(ti,dji)*1
        autorizeddoc[doc]=produit
    return autorizeddoc

def coef_de_dice(listreq):
    print("COEF DE DICE")
    autorizeddoc = {}
    for doc in range(1, N + 1):
        numerateur = 0.0
        denominateur = len(listreq)

        for (a,b) in poids:
            if (a in listreq and b == doc):
                numerateur += poids[a,doc]#poids(ti,dji)* poids(ti,Qk)==>poids(ti,dji)*1
                denominateur += pow(poids[a,doc],2)
            elif(b == doc):
                denominateur += pow(poids[a,doc],2)               
        if denominateur != 0:
            autorizeddoc[doc]= (2*numerateur)/denominateur
        else: autorizeddoc[doc]=0
    return autorizeddoc

def cosinus(listreq):
    print("COSINUS")
    autorizeddoc = {}
    for doc in range(1, N + 1):
        numerateur = 0.0
        denominateur1 = 0.0
        denominateur2 = len(listreq)          
        for (a, b) in poids:
            if (b == doc):
                if a in listreq:
                    numerateur += poids[a, doc]  # poids(ti,dji)* poids(ti,Qk)==>poids(ti,dji)*1
                denominateur1 += pow(poids[a, doc], 2)                    
        denominateur= sqrt(denominateur1*denominateur2)
        if denominateur != 0:
            autorizeddoc[doc] = numerateur/denominateur
        else:
            autorizeddoc[doc] = 0
    return autorizeddoc


def jaccord(listreq):
    print("JACCORD")
    autorizeddoc = {}
    for doc in range(1, N + 1):
        numerateur = 0.0
        denominateur1 = 0.0
        denominateur2 = len(listreq)
        for (a, b) in poids:
            if (a in listreq and b == doc):
                numerateur += poids[a, doc]  # poids(ti,dji)* poids(ti,Qk)==>poids(ti,dji)*1
                denominateur1 += pow(poids[a, doc], 2)
            elif(b==doc):
                denominateur1 += pow(poids[a, doc], 2)
        denominateur=  denominateur1+denominateur2 -numerateur
        if denominateur != 0:
            autorizeddoc[doc] = numerateur/denominateur
        else:
            autorizeddoc[doc] = 0
    return autorizeddoc

"""
print(produit_interne(nettoyer_requete(req_result)))
print(coef_de_dice(nettoyer_requete(req_result)))
print(cosinus(nettoyer_requete(req_result)))
print(jaccord(nettoyer_requete(req_result)))
"""

# evaluation: 
# resultat du model vectoriel pour la requete choisie + 
# docs selectionnés par user 
def evaluation_rappel_precision(vectResult, docsUser): 
    docsSys=[] 
    docsPerti=[]
    for element in vectResult:
        if (element != 0.0) : # if (element != 0.0) :
            print ("element : ", element)
            docsSys.append(element[0])
    for element in docsSys:
        if element in docsUser:
            docsPerti.append(element)
    #calcul du rappel et de la precision
    nbDocsSys= len(docsSys)
    nbDocsUser=  len(docsUser)
    nbDocsPerti= len(docsPerti)     
    #print(nbDocsSys,nbDocsUser,nbDocsPerti)
    #nb docs pertinants de sys  / nb docs pertinants de user
    rappel= nbDocsPerti/nbDocsUser
    #nb docs pertinants de sys / nb total docs retournés par sys
    précision = nbDocsPerti/nbDocsSys
    
    result=[]
    result.append(rappel)
    result.append(précision)
    
    return result


def evaluation(req, vectResult, docsUser):
    res = {}
    liste_req = nettoyer_requete(req)
    N = get_N() 
    R = len(docsUser)
    # chercher ni le nombre de docs de la collection contenant ti
    ni = {}
    for mot in liste_req:
        nb_doc = len(indexmot(freq, mot))
        ni[mot] = nb_doc
    
    # chercher le nb de docs pertinents contenants ti
    # les docs pertinents sont dans docsUser    
    freq_echantillon = {}
    for(a,b) in freq:
        if b in docsUser:
            freq_echantillon[a,b] = freq[a,b]
    
    ri = {}
    for mot in liste_req:
        nb_doc = len(indexmot(freq_echantillon, mot))
        ri[mot] = nb_doc
        
    print("ri est ",ri)
    print("ni est ",ni)
    # application de la formule 
    
    for doc in range (1,N+1):  
        somme = 0
        for mot in liste_req:
            res_poids = indexmotPoids(poids,mot)
            if doc in res_poids.keys():
                poid = res_poids[doc]
            else:
                poid = 0
            #print("doc ",doc, ", poid de ",mot,":",poid)
            num = (ri[mot] + 0.5) / (R - ri[mot] + 0.5)
            denomi = (ni[mot] - ri[mot] + 0.5) / (N - ni[mot] - R + ri[mot] + 0.5)
            somme  += poid*log10(num/denomi)
        res[doc] = somme
        print("doc ",doc, " : ", res[doc])
        
    return res
    
