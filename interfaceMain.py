import math
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog,
			     QLabel, QMainWindow, QMenu, QMessageBox,
			     QScrollArea, QSizePolicy, QPushButton,
                  QTableWidget,QTableWidgetItem,
                             QWidget, QDateTimeEdit, qApp)


from Exos_project import * # fichier contenant les fonctions
from interface import * #--importation du fichier de description GUI---

N = get_N()

Collection=[]
Index=[] # liste de l'indexe des docs
IndexPond=[] # liste de l'indexe pondéré des docs 
IndexBymots=[] # liste de l'indexe des mots
IndexPondBymots=[] # liste de l'indexe pondéré des mots
freq=get_freq()
freqP=get_poids()

for i in range(N):
    Index.append(indexdoc(freq, i+1))
    IndexPond.append(indexdocPoids(freqP,i+1))

for element in freq:
    IndexBymots.append(indexmot(freq,element[0]))
for element in freqP:
    IndexPondBymots.append(indexmotPoids(freqP,element[0]))

for element in freq:
        Collection.append(element[0])
        
class RI_Projet(QWidget, Ui_Form):
    #self represente la classe qui est une portion fixe !
    def __init__(self, parent=None):
        super(RI_Projet,self).__init__(parent)
        #QWidget.__init__(self) #initialisation du QWidget principale
        self.setupUi(parent) #obligatoire
        self.setFixedSize(656, 572)
        self.center

        self.ok_terme.setToolTip("rechercher pour un terme")
        self.ok_terme.clicked.connect(self.chercher_terme)

        self.ok_doc.setToolTip("rechercher pour un document")
        self.ok_doc.clicked.connect(self.chercher_doc)

        self.pushButton_bool_chercher.setToolTip("recherche booleen sur la requete")
        self.pushButton_bool_chercher.clicked.connect(self.chercher_bool)

        self.pushButton_chercher_vec.setToolTip("recherche vectoriel sur la requete")
        self.pushButton_chercher_vec.clicked.connect(self.chercher_vectoriel)

        self.pushButton_cherche_proba.setToolTip("recherche vectoriel sur la requete")
        self.pushButton_cherche_proba.clicked.connect(self.chercher_proba)

        self.pushButton.clicked.connect(lambda: self.ChoixAffichage("Index",Index,IndexPond)) # bouton Indexe
        self.pushButton_2.clicked.connect(lambda: self.ChoixAffichage("IndexP",Index,IndexPond)) # bouton Indexe pondéré

        self.pB_proba.clicked.connect(self.chercher_proba2)

        # Fonction pour ajuster les tableau à la taille de leurs containers
        header = self.tableWidget_rech_terme_res.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch) # .ResizeToContents

        header = self.tableWidget_rech_doc_res.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        header = self.tableWidget_bool_resultat.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        header = self.tableWidget_resultat_vectoriel.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        header = self.tableWidget_probab_echantillon.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        header = self.tableWidget_proba_resultat.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
	

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def chercher_terme(self):
        terme = self.textEdit_terme.toPlainText()
        if terme == "":
            QMessageBox.warning(self,  "Avertissement","Aucun terme n'est spécifié.")
            return
        # sinon appel de la fonction appropriée et remlir de lableau
        # verifier le type d'indexation
        res = {}
        terme = terme.lower()
        if self.cB_info_index.currentText() == "Indexe non pondéré":
            res = indexmot(freq,terme)
        else : # ie: self.cB_info_index.currentText() == "Indexe pondéré"
            res = indexmotPoids(freqP,terme)
        #remplir le tableau
        self.tableWidget_rech_terme_res.setRowCount(len(res))
        i = 0
        for nb_doc in res:
            self.tableWidget_rech_terme_res.setItem(i,0, QTableWidgetItem("Doc "+str(nb_doc)))
            self.tableWidget_rech_terme_res.setItem(i,1, QTableWidgetItem(str(round(res[nb_doc],5))))
            self.tableWidget_rech_terme_res.item(i, 0).setBackground(QtGui.QColor(203, 255, 187))
            self.tableWidget_rech_terme_res.item(i, 1).setBackground(QtGui.QColor(203, 255, 187))
            i += 1


    def chercher_doc(self):
        doc = self.textEdit_doc.toPlainText()
        if doc == "":
            QMessageBox.warning(self,  "Avertissement","Aucun document n'est spécifié.")
            return  
        if not doc.isdigit():
            QMessageBox.warning(self,  "Avertissement",doc+" n'est pas un numéro de document\nEntrer un numéro de document valide.")
            return  
        # sinon appel de la fonction appropriée et remplir le tableau
        # verifier le type d'indexation
        res = {}
        d=int(doc)
        print(d)
        if self.cB_info_index.currentText() == "Indexe non pondéré":  
            res = indexdoc(freq,d)
        else : # ie: self.cB_info_index.currentText() == "Indexe pondéré"
            res = indexdocPoids(freqP,d)
        self.tableWidget_rech_doc_res.setRowCount(len(res))
        i = 0
        for terme in res:
            self.tableWidget_rech_doc_res.setItem(i,0, QTableWidgetItem(terme))
            val = round(res[terme], 5)
            self.tableWidget_rech_doc_res.setItem(i,1, QTableWidgetItem(str(val)))
            self.tableWidget_rech_doc_res.item(i, 0).setBackground(QtGui.QColor(203, 255, 187))
            self.tableWidget_rech_doc_res.item(i, 1).setBackground(QtGui.QColor(203, 255, 187))
            i += 1
        

    def chercher_bool(self):
        req = self.textEdit.toPlainText()
        if req == "":
            self.tableWidget_bool_resultat.setRowCount(0)
            QMessageBox.warning(self,  "Avertissement","Aucun document n'est spécifié.")
            return

        liste, b = modele_booleen(req)
        if(b==False):
            self.tableWidget_bool_resultat.setRowCount(0)
            QMessageBox.warning(self, "Erreur", "Requête erronée ! \nRevoir la syntaxe")
            return 
        #sinon on appel la fonction
        if(len(liste) == 0):
            self.tableWidget_bool_resultat.setRowCount(0)
            QMessageBox.information(self, "Information", "Aucun document ne répond à la requête")
            return 
        else:
            #remplir le tableau
            self.tableWidget_bool_resultat.setRowCount(len(liste))
            i = 0
            for nb_doc in liste:
                self.tableWidget_bool_resultat.setItem(i,0, QTableWidgetItem("Document "+str(nb_doc)))
                i += 1
        

    def chercher_vectoriel(self):
        req = self.textEdit_2.toPlainText()
        if req == "":
            self.tableWidget_resultat_vectoriel.setRowCount(0)
            QMessageBox.warning(self,  "Avertissement","Aucun document n'est spécifié.")
            return
        choix = self.comboBox_choix_vectoriel.currentText()
        req = nettoyer_requete(req)
        res = {}
        if choix == "Produit interne":
            res = produit_interne(req)
        if choix == "Coef de Dice":
            res = coef_de_dice(req)
        if choix == "Cosinus":
            res = cosinus(req)
        if choix == "Jaccard":
            res = jaccord(req)
        print(res)
        self.tableWidget_resultat_vectoriel.setRowCount(len(res))
        if(len(res) == 0):
            QMessageBox.information(self, "Information", "Aucun document ne répond à la requête")
            return 
        i = 0
        for doc in res:
            self.tableWidget_resultat_vectoriel.setItem(i,0, QTableWidgetItem("Document "+str(doc)))
            val = round(res[doc], 5)
            self.tableWidget_resultat_vectoriel.setItem(i,1, QTableWidgetItem(str(val)))
            self.tableWidget_resultat_vectoriel.item(i, 0).setBackground(QtGui.QColor(203, 255, 187))
            self.tableWidget_resultat_vectoriel.item(i, 1).setBackground(QtGui.QColor(203, 255, 187))
            i += 1


    def chercher_proba(self):
        req = self.textEdit_proba.toPlainText()
        if req == "":
            self.tableWidget_probab_echantillon.setRowCount(0)
            QMessageBox.warning(self,  "Avertissement","Aucun document n'est spécifié.")
            return
        req = nettoyer_requete(req)
        choix = self.comboBox_choix_proba.currentText()
        res = {}
        if choix == "Produit interne":
            res = produit_interne(req)
        if choix == "Coef de Dice":
            res = coef_de_dice(req)
        if choix == "Cosinus":
            res = cosinus(req)
        if choix == "Coef de Jaccard":
            res = jaccord(req)
        print(res)
        self.tableWidget_probab_echantillon.setRowCount(len(res))
        if(len(res) == 0):
            QMessageBox.information(self, "Information", "Aucun document ne répond à la requête")
            return 
        i = 0
        for doc in res:
            chkBoxItem = QTableWidgetItem("Document "+str(doc))
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked) 
            self.tableWidget_probab_echantillon.setItem(i,0, chkBoxItem)
            val = round(res[doc], 5)
            self.tableWidget_probab_echantillon.setItem(i,1, QTableWidgetItem(str(val)))
            self.tableWidget_probab_echantillon.item(i, 0).setBackground(QtGui.QColor(203, 255, 187))
            self.tableWidget_probab_echantillon.item(i, 1).setBackground(QtGui.QColor(203, 255, 187))
            i += 1


    def chercher_proba2(self):
        if self.tableWidget_probab_echantillon.item(0,0).text() == "" :
            QMessageBox.information(self, "Information", "Lancer la recherche vectoriel d'abord")
            return 
        listeDec = [] # contiendra les docs de l'echantillon avec leurs similarité
        checked_items=[]
        print("coucou")
        nb = 0
        allRows = self.tableWidget_probab_echantillon.rowCount()
        for row in range(0,allRows):
            sim = self.tableWidget_probab_echantillon.item(row,1).text()
            if float(sim) > 0.0:
                listeDec.append([row+1, float(sim)])

            tw = self.tableWidget_probab_echantillon.item(row,0)
            if tw.checkState() == QtCore.Qt.Checked:
                checked_items.append(row+1)
                print("checked at row ",row+1, ", content is :" ,tw.text())
                nb += 1

        # ordonner la liste des docs selon la similarité dans un ordre décroissant 
        listeDec.sort(key=lambda x: x[1])
        listeDec= listeDec[::-1]
        print(listeDec)


        if nb > 0: # c.a.d qu'il existe des docs selectionné
            if len(listeDec) > 0:
                req = self.textEdit_proba.toPlainText()
                res_eval = evaluation(req, listeDec, checked_items)
                self.tableWidget_proba_resultat.setRowCount(len(res_eval))
                if(len(res_eval) == 0):
                    QMessageBox.information(self, "Information", "Aucun document résulatat trouvé")
                    return 
                i=0
                for doc in res_eval:
                    nom = "Document " + str(doc)
                    self.tableWidget_proba_resultat.setItem(i,0, QTableWidgetItem(str(nom)))
                    val_sim = round(res_eval[doc],5)
                    self.tableWidget_proba_resultat.setItem(i,1, QTableWidgetItem(str(val_sim)))
                    self.tableWidget_proba_resultat.item(i, 0).setBackground(QtGui.QColor(203, 255, 187))
                    self.tableWidget_proba_resultat.item(i, 1).setBackground(QtGui.QColor(203, 255, 187))
                    i+=1


                resultat = evaluation_rappel_precision(listeDec, checked_items)
                print("Rappel = "+str(round(resultat[0], 2))+"\nPrécision= "+str(round(resultat[1], 2)))
                rappel = str(round(resultat[0], 2))
                precision = str(round(resultat[1], 2))
                self.textEdit_Rappel.setPlainText(rappel)
                self.textEdit_Precision.setText(precision)

                '''
                self.tableWidget_proba_resultat.setItem(0,0, QTableWidgetItem(rappel))
                self.tableWidget_proba_resultat.setItem(0,1, QTableWidgetItem(precision))
                self.tableWidget_proba_resultat.item(0, 0).setBackground(QtGui.QColor(203, 255, 187))
                self.tableWidget_proba_resultat.item(0, 1).setBackground(QtGui.QColor(203, 255, 187))
                '''
        else :# if nb==0:
            QMessageBox.warning(self,  "Avertissement","Aucun document n'est selectionné.")
            return


    def LectureItemDocs(self,Index):
        #self.listWidget_2.clear()
        self.textBrowser.setText("")
        Doc=self.listWidget.currentItem().text()
        if(Doc.startswith('D')):
                num=(Doc[1:])
                print(num)
                res  = Index[int(num)-1]
                for word in res:
                    phrase = word + " : " + str(round(res[word], 5)) + "\n"
                    self.textBrowser.insertPlainText(phrase)
                

    def AfficherDocs(self, Index):
        self.listWidget.clear()
        self.listWidget_2.clear()
        i=1
        for element in Index:
            self.listWidget.addItem("D"+str(i))
            i=i+1
        #print(listeDec)


    def AfficherMots(self, collection):
        self.listWidget.clear()
        self.listWidget_2.clear()
        for element in collection:
            self.listWidget.addItem(str(element))


    def LectureWords(self,IndexMots,typeIndex):
        self.textBrowser.setText("")
        liste=[]
        self.listWidget_2.clear()
        word=self.listWidget.currentItem().text()
        print(word)
        if(typeIndex=="Index"):
            Liste=indexmot(freq,word)
        elif(typeIndex=="IndexP"):
            Liste=indexmotPoids(freqP,word)
        #print(Liste)
        
        for element in Liste:
            print (element , Liste[element])
            val = round(Liste[element], 5)
            phrase = "D" + str(element) + " : " + str(val)+"\n"
            self.textBrowser.insertPlainText(phrase)
        

    def ChoixAffichage(self, typeIndex,Index,IndexPond): 
        self.listWidget.clear()
        self.listWidget_2.clear()
        # Affichage par documents
        if(self.radioButton.isChecked()):
            if typeIndex=="Index" :
                self.AfficherDocs(Index)
                self.listWidget.itemDoubleClicked.connect(lambda: self.LectureItemDocs(Index))
            elif typeIndex=="IndexP":
                self.AfficherDocs(IndexPond)
                self.listWidget.itemDoubleClicked.connect(lambda: self.LectureItemDocs(IndexPond))
        # Affichage par mots
        elif(self.radioButton_2.isChecked()):
            if typeIndex=="Index" :
                self.AfficherMots(sorted(set(Collection)))
                self.listWidget.itemDoubleClicked.connect(lambda: self.LectureWords(Index,"Index"))
            elif typeIndex=="IndexP":
                self.AfficherMots(sorted(set(Collection)))
                self.listWidget.itemDoubleClicked.connect(lambda: self.LectureWords(IndexPond,"IndexP"))
        else:
            error=QtWidgets.QErrorMessage()
            error.showMessage("Veuillez choisir un mode d'affichage.")
            error.exec_() 
        return 0; 


#fonctopn principale executant l'application Qt
def main(args):
    a = QApplication(args)
    f = QWidget()
    c = RI_Projet(f)
    f.show()
    r = a.exec_()
    return r

if __name__=="__main__":
    main(sys.argv)
