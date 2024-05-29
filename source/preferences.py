# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.11 con libreria pyqt5
 Data..........: 29/11/2023
 Descrizione...: Gestione delle preferenze di MChat
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file preferences.py è ricavato partendo da preferences_ui.ui 

 Note..........: Questo programma ha due funzioni. La prima di gestire a video le preferenze e la seconda di restituire una classe
                 che contiene le preferenze (preferences_class)
"""

#Librerie sistema
import sys
import os
import json
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#Definizioni interfaccia
from preferences_ui import Ui_preferences_window
#Librerie aggiuntive interne
from utilita import message_info, message_question_yes_no

class preferences_class():
    """
        Classe che riporta tutte le preferenze
    """
    def __init__(self, p_nome_file_preferences):
        """
           Lettura del file delle preferenze e caricamento nella classe
        """
        # Se esiste il file delle preferenze...le carico nell'oggetto
        if os.path.isfile(p_nome_file_preferences):
            v_json = json.load(open(p_nome_file_preferences, 'r'))
            # posizione finestre        
            if v_json['remember_window_pos']==1:
                self.remember_window_pos = True
            else:
                self.remember_window_pos = False
            # il bordo delle finestre viene nascosto
            if v_json['hide_window_border']==1:
                self.hide_window_border = True
            else:
                self.hide_window_border = False
            # tema scuro
            if v_json['dark_theme']==1:
                self.dark_theme = True
            else:
                self.dark_theme = False            
            # splash screen
            if v_json['splash'] == 1:
                self.splash = True
            else:
                self.splash = False
            # server
            self.elenco_server = v_json['server']
            # users
            self.elenco_user = v_json['users']
            # messaggio attivo nella systray 
            # (si è fatta la try perché per alcune installazioni la preferenza potrebbe non esserci)
            try:
                if v_json['message_systray'] == 1:
                    self.message_systray = True
                else:
                    self.message_systray = False
            except:
                self.message_systray = False
            # toolbar nascosta
            # (si è fatta la try perché per alcune installazioni la preferenza potrebbe non esserci)
            try:
                if v_json['hide_toolbar'] == 1:
                    self.hide_toolbar = True
                else:
                    self.hide_toolbar = False
            except:
                self.hide_toolbar = False
            # loop quando ci si connette come client
            # (si è fatta la try perché per alcune installazioni la preferenza potrebbe non esserci)
            try:
                if v_json['loop_when_connect'] == 1:
                    self.loop_when_connect = True
                else:
                    self.loop_when_connect = False
            except:
                self.loop_when_connect = True

        # imposto valori di default senza presenza dello specifico file
        else:            
            # salvataggio posizione finestra
            self.remember_window_pos = True            
            # finestra senza bordo
            self.hide_window_border = True
            # tema scuro
            self.dark_theme = True            
            # titolo finestra lampeggiante
            self.splash = False            
            # elenco server è composto da Titolo, TNS e Colore
            self.elenco_server = [('SERVER ONE','1250','1'),
                                  ('SERVER TWO','1300','0')]
            # elenco users è composto da Titolo, User, Password
            self.elenco_user = [('PC-MVALAGUZ','Vala','10.0.47.9','1'),
                                ('pc-aberlend','Solo','10.0.47.1','0'),                                
                                ('PC-TRAINIM','Marco','10.0.47.17','0')]
            # messaggio attivo nella systray
            self.message_systray = False
            # toolbar nascosta
            self.hide_toolbar = False
            # loop quando ci si connette come client
            self.loop_when_connect = True
            # creo la dir dove andranno le preferenze              
            if not os.path.isdir(os.path.expanduser('~\\AppData\\Local\\MChat\\')):
                os.makedirs(os.path.expanduser('~\\AppData\\Local\\MChat\\'))
       
class win_preferences_class(QMainWindow, Ui_preferences_window):
    """
        Gestione delle preferenze di MChat
    """                
    def __init__(self, p_nome_dir_preferences):
        super(win_preferences_class, self).__init__()        
        self.setupUi(self)

        self.nome_dir_preferences = p_nome_dir_preferences
        self.nome_file_preferences = p_nome_dir_preferences + 'MChat.ini'

        # creo l'oggetto preferenze che automaticamente carica il file o le preferenze di default
        self.preferences = preferences_class(self.nome_file_preferences)        
        # le preferenze caricate vengono riportate a video
        self.e_remember_window_pos.setChecked(self.preferences.remember_window_pos)        
        self.e_hide_window_border.setChecked(self.preferences.hide_window_border)                
        self.e_default_splash.setChecked(self.preferences.splash)           
        self.e_dark_theme.setChecked(self.preferences.dark_theme)
        self.e_message_systray.setChecked(self.preferences.message_systray)
        self.e_hide_toolbar.setChecked(self.preferences.hide_toolbar)
        self.e_loop_when_connect.setChecked(self.preferences.loop_when_connect)

        # preparo elenco server        
        self.o_server.setColumnCount(3)
        self.o_server.setHorizontalHeaderLabels(['Server title','IP port','Default (check only one)'])           
        v_rig = 1                
        for record in self.preferences.elenco_server:                                    
            self.o_server.setRowCount(v_rig) 
            self.o_server.setItem(v_rig-1,0,QTableWidgetItem(record[0]))       
            self.o_server.setItem(v_rig-1,1,QTableWidgetItem(record[1]))                                                                     
            # la terza colonna è una check-box per la selezione del server di default
            # da notare come la checkbox viene inserita in un widget di layout in modo che si possa
            # attivare la centratura 
            v_checkbox = QCheckBox()          
            v_widget = QWidget()      
            v_layout = QHBoxLayout(v_widget)
            v_layout.addWidget(v_checkbox)
            v_layout.setAlignment(Qt.AlignCenter)
            v_layout.setContentsMargins(0,0,0,0)
            v_widget.setLayout(v_layout)
            if record[2] == '1':
                v_checkbox.setChecked(True)                                            
            else:
                v_checkbox.setChecked(False)                                                        
            self.o_server.setCellWidget(v_rig-1,2,v_widget)                               
            
            v_rig += 1
        self.o_server.resizeColumnsToContents()

        # preparo elenco user        
        self.o_users.setColumnCount(4)
        self.o_users.setHorizontalHeaderLabels(['PC-NAME','Title name','IP','Default (check only one)'])   
        v_rig = 1                
        for record in self.preferences.elenco_user:                                    
            self.o_users.setRowCount(v_rig) 
            self.o_users.setItem(v_rig-1,0,QTableWidgetItem(record[0]))       
            self.o_users.setItem(v_rig-1,1,QTableWidgetItem(record[1]))                               
            self.o_users.setItem(v_rig-1,2,QTableWidgetItem(record[2]))                               
            # la quarta colonna è una check-box per la selezione del user di default
            # da notare come la checkbox viene inserita in un widget di layout in modo che si possa
            # attivare la centratura 
            v_checkbox = QCheckBox()          
            v_widget = QWidget()      
            v_layout = QHBoxLayout(v_widget)
            v_layout.addWidget(v_checkbox)
            v_layout.setAlignment(Qt.AlignCenter)
            v_layout.setContentsMargins(0,0,0,0)
            v_widget.setLayout(v_layout)
            if record[3] == '1':
                v_checkbox.setChecked(True)                                            
            else:
                v_checkbox.setChecked(False)                                                        
            self.o_users.setCellWidget(v_rig-1,3,v_widget)                               

            v_rig += 1
        self.o_users.resizeColumnsToContents()

    def slot_set_color_server(self):
        """
           Gestione della scelta dei colori sull'elenco dei server
        """
        # ottengo un oggetto index-qt della riga selezionata
        index = self.o_server.currentIndex()           
        # prendo la cella che contiene il colore in modo da aprire la selezione partendo dal colore corrente
        v_color_corrente = self.o_server.item( index.row(), 2).text()                        
        # apro la dialog color
        color = QColorDialog.getColor(QColor(v_color_corrente))                
        # imposto il colore
        self.o_server.setItem( index.row(), 2, QTableWidgetItem(color.name()) )            
    
    def slot_b_restore(self):
        """
           Ripristina tutte preferenze di default
        """
        if message_question_yes_no('Do you want to restore default preferences?') == 'Yes':
            # cancello il file delle preferenze
            if os.path.isfile(self.nome_file_preferences):
                os.remove(self.nome_file_preferences)

            # emetto messaggio di fine
            message_info('Preferences restored! Restart MChat to see the changes ;-)')
            # esco dal programma delle preferenze
            self.close()

    def slot_b_open_pref_dir(self):
        """
           Apre la cartella che contiene le preferenze
        """
        os.startfile(os.path.expanduser(self.nome_dir_preferences))        
    
    def slot_b_server_add(self):
        """
           Crea una riga vuota dove poter inserire informazioni connessioni al server
        """
        # aggiungo una riga
        self.o_server.setRowCount(self.o_server.rowCount()+1)        
        # inserisce nella terza colonna la checkbox 
        v_checkbox = QCheckBox()          
        v_widget = QWidget()      
        v_layout = QHBoxLayout(v_widget)
        v_layout.addWidget(v_checkbox)
        v_layout.setAlignment(Qt.AlignCenter)
        v_layout.setContentsMargins(0,0,0,0)
        v_widget.setLayout(v_layout)
        v_checkbox.setChecked(False)                                                        
        self.o_server.setCellWidget(self.o_server.rowCount()-1,2,v_widget)                        

    def slot_b_server_remove(self):
        """
           Toglie la riga selezionata, da elenco server
        """
        self.o_server.removeRow(self.o_server.currentRow())

    def slot_b_user_add(self):
        """
           Crea una riga vuota dove poter inserire informazioni utente di connessione al server
        """
        # aggiungo una riga
        self.o_users.setRowCount(self.o_users.rowCount()+1)        
        # inserisce nella quarta colonna la checkbox 
        v_checkbox = QCheckBox()          
        v_widget = QWidget()      
        v_layout = QHBoxLayout(v_widget)
        v_layout.addWidget(v_checkbox)
        v_layout.setAlignment(Qt.AlignCenter)
        v_layout.setContentsMargins(0,0,0,0)
        v_widget.setLayout(v_layout)
        v_checkbox.setChecked(False)                                                        
        self.o_users.setCellWidget(self.o_users.rowCount()-1,3,v_widget)                        

    def slot_b_user_remove(self):
        """
           Toglie la riga selezionata, da elenco user
        """
        self.o_users.removeRow(self.o_users.currentRow())

    def slot_b_save(self):
        """
           Salvataggio
        """	
        # il default per ricordare posizione della window
        if self.e_remember_window_pos.isChecked():
            v_remember_window_pos = 1
        else:
            v_remember_window_pos = 0

        # flag indicante se i bordi della finestra vanno nascosti
        if self.e_hide_window_border.isChecked():
            v_hide_window_border = 1
        else:
            v_hide_window_border = 0
            
        # flag indicante se attivare il tema scuro
        if self.e_dark_theme.isChecked():
            v_dark_theme = 1
        else:
            v_dark_theme = 0
        
        # splash screen
        if self.e_default_splash.isChecked():
            v_splash = 1
        else:
            v_splash = 0
            
        # elenco dei server
        v_server = []
        for i in range(0,self.o_server.rowCount()):
            # controllo la checkbox del default (da notare come la checkbox è annegata in un oggetto di layout 
            # e quindi prima prendo l'oggetto che c'è annegato nella cella della tabella, poi in quell'oggetto
            # prendo tutti gli oggetti di tipo checkbox e poi prendo il primo checkbox (che è anche l'unico)
            # e da li prendo il suo stato!
            v_widget = self.o_server.cellWidget(i,2)
            v_checkbox = v_widget.findChildren(QCheckBox)
            if v_checkbox[0].isChecked():                
                v_default = '1'
            else:
                v_default = '0'
            # preparo l'array con la stringa della riga server
            v_server.append( ( self.o_server.item(i,0).text(), self.o_server.item(i,1).text(), v_default ) )            

        # elenco dei users
        v_users = []
        for i in range(0,self.o_users.rowCount()):
            # controllo la checkbox del default (da notare come la checkbox è annegata in un oggetto di layout 
            # e quindi prima prendo l'oggetto che c'è annegato nella cella della tabella, poi in quell'oggetto
            # prendo tutti gli oggetti di tipo checkbox e poi prendo il primo checkbox (che è anche l'unico)
            # e da li prendo il suo stato!
            v_widget = self.o_users.cellWidget(i,3)
            v_checkbox = v_widget.findChildren(QCheckBox)
            if v_checkbox[0].isChecked():                
                v_default = '1'
            else:
                v_default = '0'    
            # preparo l'array con la stringa della riga server
            v_users.append( ( self.o_users.item(i,0).text(), self.o_users.item(i,1).text() , self.o_users.item(i,2).text(), v_default) )            

        # messaggio nella systray
        if self.e_message_systray.isChecked():
            v_message_systray = 1
        else:
            v_message_systray = 0
        
        # toolbar nascosta
        if self.e_hide_toolbar.isChecked():
            v_hide_toolbar = 1
        else:
            v_hide_toolbar = 0
        
        # loop quando ci si connette come client
        if self.e_loop_when_connect.isChecked():
            v_loop_when_connect = 1
        else:
            v_loop_when_connect = 0

		# scrivo nel file un elemento json contenente le informazioni inseriti dell'utente
        v_json ={'remember_window_pos': v_remember_window_pos,                 
                 'hide_window_border': v_hide_window_border,                 
                 'dark_theme': v_dark_theme,		         
                 'splash' : v_splash,                 
                 'server': v_server,
                 'users': v_users,
                 'message_systray':v_message_systray,
                 'hide_toolbar':v_hide_toolbar,
                 'loop_when_connect':v_loop_when_connect
                }

		# scrittura nel file dell'oggetto json
        with open(self.nome_file_preferences, 'w') as outfile:json.dump(v_json, outfile)
        
        message_info('Preferences saved! Restart MChat to see the changes ;-)')

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QApplication([])
    application = win_preferences_class(os.path.expanduser('~\\AppData\\Local\\MChat\\'))
    application.show()
    sys.exit(app.exec())        