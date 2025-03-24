"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.13 con libreria pyqt6
 Data..........: 29/11/2023
 Descrizione...: Gestione delle preferenze di Echo
 
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
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
#Definizioni interfaccia
from preferences_ui import Ui_preferences_window
#Librerie aggiuntive interne
from utilita import message_error, message_info, message_question_yes_no, cripta_messaggio, decripta_messaggio
#Amplifico la pathname per ricercare le icone
QDir.addSearchPath('icons', 'qtdesigner/icons/')
#Messaggio che esce come maschera 
v_global_mask_window_message = """
<ol>
    <li>
        <strong>Controllo delle comunicazioni</strong>
        <ul>
            <li>Rivedere e rispondere alle email o ai messaggi su piattaforme come Slack.</li>
            <li>Partecipare alle riunioni mattutine (stand-up) per condividere aggiornamenti e pianificare la giornata.</li>
        </ul>
    </li>
    <li>
        <strong>Pianificazione</strong>
        <ul>
            <li>Rivedere l'elenco delle attività (ad esempio, in uno strumento come Jira).</li>
            <li>Dare priorità ai compiti più urgenti o importanti.</li>
        </ul>
    </li>
    <li>
        <strong>Scrivere codice</strong>
        <ul>
            <li>Implementare nuove funzionalità richieste nel progetto.</li>
            <li>Correggere bug segnalati durante i test o dagli utenti finali.</li>
            <li>Ottimizzare il codice esistente per migliorare le prestazioni.</li>
        </ul>
    </li>
    <li>
        <strong>Test e debug</strong>
        <ul>
            <li>Scrivere ed eseguire test unitari per garantire il funzionamento del codice.</li>
            <li>Eseguire il debug per identificare e risolvere i problemi.</li>
        </ul>
    </li>
    <li>
        <strong>Collaborazione</strong>
        <ul>
            <li>Discutere soluzioni tecniche con il team o i designer.</li>
            <li>Rivedere e fornire feedback sui commit e pull request dei colleghi.</li>
        </ul>
    </li>
    <li>
        <strong>Documentazione</strong>
        <ul>
            <li>Aggiornare i documenti tecnici relativi al progetto.</li>
            <li>Scrivere commenti chiari nel codice per aiutare altri sviluppatori.</li>
        </ul>
    </li>
    <li>
        <strong>Apprendimento</strong>
        <ul>
            <li>Dedica tempo all'apprendimento di nuove tecnologie, strumenti o framework.</li>
            <li>Consultare documentazione, guide e tutorial online per risolvere problemi complessi.</li>
        </ul>
    </li>
    <li>
        <strong>Perfezionamento del lavoro</strong>
        <ul>
            <li>Testare le funzionalità implementate in ambienti di staging o pre-produzione.</li>
            <li>Assicurarsi che il lavoro soddisfi i requisiti del progetto e gli standard di qualità.</li>
        </ul>
    </li>
    <li>
        <strong>Consegna</strong>
        <ul>
            <li>Preparare e distribuire il codice in produzione.</li>
            <li>Monitorare il comportamento del sistema dopo il rilascio.</li>
        </ul>
    </li>
    <li>
        <strong>Pausa e rilassamento</strong>
        <ul>
            <li>Fare pause per rinfrescare la mente e aumentare la produttività.</li>
            <li>A volte, le migliori idee nascono durante una pausa!</li>
        </ul>
    </li>
</ol>
"""

class preferences_class():
    """
        Classe che riporta tutte le preferenze
    """
    def __init__(self):
        """
           Lettura del file delle preferenze e caricamento nella classe
        """
        # Se esiste il file delle preferenze...le carico nell'oggetto
        v_json = QSettings("Echo Utility", "Echo").value("preferences")                
        if v_json:
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
            self.elenco_server = []
            for line in v_json['server']:
                self.elenco_server.append( ( decripta_messaggio(line[0]), decripta_messaggio(line[1]), line[2] ) )                                
            # users            
            self.elenco_user = []
            for line in v_json['users']:
                self.elenco_user.append( ( decripta_messaggio(line[0]), decripta_messaggio(line[1]), decripta_messaggio(line[2]), line[3], line[4] ) )                                
            # messaggio attivo nella systray                         
            if v_json['message_systray'] == 1:
                self.message_systray = True
            else:
                self.message_systray = False
            # inserisce il nome dell'utente nel titolo del tooltip quando si è in modalità systray
            if v_json['hide_name_in_systray_title'] == 1:
                self.hide_name_in_systray_title = True
            else:
                self.hide_name_in_systray_title = False
            # toolbar nascosta
            if v_json['hide_toolbar'] == 1:
                self.hide_toolbar = True
            else:
                self.hide_toolbar = False
            # loop quando ci si connette come client
            if v_json['loop_when_connect'] == 1:
                self.loop_when_connect = True
            else:
                self.loop_when_connect = False
            # livello di opacità della window
            self.opacity = v_json['opacity'] 
            # timer che pulisce la chat
            self.clear_chat_timer = v_json['clear_chat_timer']             
            # timer che minimizza la window
            self.minimize_window_timer = v_json['minimize_window_timer']             
            # timer che maschera la window
            self.mask_window_timer = v_json['mask_window_timer']             
            # messaggio da far uscire quando compare la maschera
            self.mask_window_message = v_json['mask_window_message']
            # indica avvio programma in modalità maschera
            if v_json['start_in_mask_mode'] == 1:
                self.start_in_mask_mode = True
            else:
                self.start_in_mask_mode = False
            # indica di minimizzare la window nella systray
            if v_json['minimize_window_to_systray'] == 1:
                self.minimize_window_to_systray = True
            else:
                self.minimize_window_to_systray = False
            # zoom generale
            self.general_zoom = v_json['general_zoom']             

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
            self.elenco_user = [('PORT-MVALAGUZ',';-)','10.0.47.9','1','#0068ad'),
                                ('PORT-ABERLEND',':-)','10.0.47.1','0','#246c35'),                                
                                ('PC-TRAINIM',':-)','10.0.47.17','0','#0068ad'),
                                ('PC-FDAMIANI',';-)','10.0.47.18','0','#246c35')]
            # messaggio attivo nella systray
            self.message_systray = False
            # inserisce il nome dell'utente nel titolo del tooltip quando si è in modalità systray
            self.hide_name_in_systray_title = True            
            # toolbar nascosta
            self.hide_toolbar = False
            # loop quando ci si connette come client
            self.loop_when_connect = True
            # livello di opacità della window
            self.opacity = 90
            # timer che pulisce la chat (10 minuti)
            self.clear_chat_timer = 600            
            # timer che minimizza la window (5 minuti)
            self.minimize_window_timer = 300
            # timer che maschera la window come se fosse un programma di top-sessions (1 minuto)
            self.mask_window_timer = 60
            # messaggio da far uscire quando compare la maschera
            self.mask_window_message = v_global_mask_window_message
            # indica avvio programma in modalità maschera
            self.start_in_mask_mode = True            
            # indica di minimizzare la window nella systray
            self.minimize_window_to_systray = True            
            # zoom generale
            self.general_zoom = 100
       
class win_preferences_class(QMainWindow, Ui_preferences_window):
    """
        Gestione delle preferenze di Echo
    """                
    def __init__(self):
        super(win_preferences_class, self).__init__()        
        self.setupUi(self)

        # creo l'oggetto preferenze che automaticamente carica dal registro le preferenze o se non presenti, quelle di default
        self.preferences = preferences_class()        
        # le preferenze caricate vengono riportate a video
        self.e_remember_window_pos.setChecked(self.preferences.remember_window_pos)        
        self.e_hide_window_border.setChecked(self.preferences.hide_window_border)                
        self.e_default_splash.setChecked(self.preferences.splash)           
        self.e_dark_theme.setChecked(self.preferences.dark_theme)
        self.e_message_systray.setChecked(self.preferences.message_systray)
        self.e_hide_name_in_systray_title.setChecked(self.preferences.hide_name_in_systray_title)
        self.e_hide_toolbar.setChecked(self.preferences.hide_toolbar)
        self.e_loop_when_connect.setChecked(self.preferences.loop_when_connect)
        self.e_opacity.setValue(self.preferences.opacity)
        self.e_clear_chat_timer.setValue(self.preferences.clear_chat_timer)
        self.e_minimize_window_timer.setValue(self.preferences.minimize_window_timer)
        self.e_general_zoom.setValue(self.preferences.general_zoom)
        self.e_minimize_window_to_systray.setChecked(self.preferences.minimize_window_to_systray)
        self.e_mask_window_timer.setValue(self.preferences.mask_window_timer)
        self.e_mask_window_message.setPlainText(self.preferences.mask_window_message)
        self.e_start_in_mask_mode.setChecked(self.preferences.start_in_mask_mode)

        # preparo elenco server        
        self.o_server.setColumnCount(3)
        self.o_server.setHorizontalHeaderLabels(['Server title','IP port','Default (check only one)'])           
        v_rig = 1                
        for record in self.preferences.elenco_server:                                    
            self.o_server.setRowCount(v_rig) 
            self.carico_riga_server(v_rig,record)
            v_rig += 1
        self.o_server.resizeColumnsToContents()

        # preparo elenco user        
        self.o_users.setColumnCount(6)
        self.o_users.setHorizontalHeaderLabels(['PC-NAME','User-Name','IP','Default (check only one)','Label color',''])   
        v_rig = 1                
        for record in self.preferences.elenco_user:                                    
            self.o_users.setRowCount(v_rig) 
            self.carico_riga_user(v_rig,record)
            # passo alla prossima riga
            v_rig += 1
        self.o_users.resizeColumnsToContents()

    def carico_riga_server(self, v_rig, record):
        """
           Carica una nuova riga nella tabella server
        """
        self.o_server.setItem(v_rig-1,0,QTableWidgetItem(record[0]))       
        self.o_server.setItem(v_rig-1,1,QTableWidgetItem(record[1]))                                                                     
        # la terza colonna è una check-box per la selezione del server di default
        # da notare come la checkbox viene inserita in un widget di layout in modo che si possa
        # attivare la centratura 
        v_checkbox = QCheckBox()          
        v_widget = QWidget()      
        v_layout = QHBoxLayout(v_widget)
        v_layout.addWidget(v_checkbox)
        v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.setContentsMargins(0,0,0,0)
        v_widget.setLayout(v_layout)
        if record[2] == '1':
            v_checkbox.setChecked(True)                                            
        else:
            v_checkbox.setChecked(False)                                                        
        self.o_server.setCellWidget(v_rig-1,2,v_widget)                               
        
    def carico_riga_user(self, v_rig, record):        
        """
           Carica una nuova riga nella tabella server
        """            
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
        v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.setContentsMargins(0,0,0,0)
        v_widget.setLayout(v_layout)
        if record[3] == '1':
            v_checkbox.setChecked(True)                                            
        else:
            v_checkbox.setChecked(False)                                                        
        self.o_users.setCellWidget(v_rig-1,3,v_widget)                               
        # come quinta colonna il nome del colore
        self.o_users.setItem(v_rig-1,4,QTableWidgetItem(record[4]))                                           
        # come sesta colonna metto il pulsante per la scelta del colore
        v_color_button = QPushButton()            
        v_icon = QIcon()
        v_icon.addPixmap(QPixmap("icons:color.png"), QIcon.Mode.Normal, QIcon.State.Off)
        v_color_button.setIcon(v_icon)
        v_color_button.clicked.connect(self.slot_set_color_user)
        self.o_users.setCellWidget(v_rig-1,5,v_color_button)                 
    
    def slot_b_restore(self):
        """
           Ripristina tutte preferenze di default
        """
        if message_question_yes_no('Do you want to restore default preferences?') == 'Yes':
             # Se esiste il file delle preferenze...le carico nell'oggetto
            v_settings = QSettings("Echo Utility", "Echo")
            v_settings.remove("preferences")            
            # emetto messaggio di fine
            message_info('Preferences restored! Restart Echo to see the changes ;-)')
            # esco dal programma delle preferenze
            self.close()
    
    def slot_b_server_add(self):
        """
           Crea una riga vuota dove poter inserire informazioni connessioni al server
        """
        v_rig = self.o_server.rowCount()+1
        self.o_server.setRowCount(v_rig)
        self.carico_riga_server(v_rig, ['','','',0,0,0]) 

    def slot_b_server_remove(self):
        """
           Toglie la riga selezionata, da elenco server
        """
        self.o_server.removeRow(self.o_server.currentRow())

    def slot_b_user_add(self):
        """
           Crea una riga vuota dove poter inserire informazioni utente di connessione al server
        """
        v_rig = self.o_users.rowCount()+1
        self.o_users.setRowCount(v_rig)
        self.carico_riga_user(v_rig, ['','','',0,0,0]) 

    def slot_b_user_remove(self):
        """
           Toglie la riga selezionata, da elenco user
        """
        self.o_users.removeRow(self.o_users.currentRow())
    
    def slot_set_color_user(self):
        """
           Gestione della scelta dei colori sull'elenco degli user
        """
        # ottengo un oggetto index-qt della riga selezionata
        index = self.o_users.currentIndex()           
        # prendo la cella che contiene il colore in modo da aprire la selezione partendo dal colore corrente
        v_color_corrente = self.o_users.item( index.row(), 4).text()                        
        # apro la dialog color
        color = QColorDialog.getColor(QColor(v_color_corrente))                
        # imposto il colore
        if color.isValid():
            self.o_users.setItem( index.row(), 4, QTableWidgetItem(color.name()) )            

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
            # preparo l'array con la stringa della riga server (nome, ip-port, default)
            v_server.append( ( cripta_messaggio(self.o_server.item(i,0).text()), cripta_messaggio(self.o_server.item(i,1).text()), v_default ) )            

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
            # preparo l'array con la stringa della riga server (nome-pc, nome-user, ip, default)
            v_users.append( ( cripta_messaggio(self.o_users.item(i,0).text()), cripta_messaggio(self.o_users.item(i,1).text()) , cripta_messaggio(self.o_users.item(i,2).text()), v_default, self.o_users.item(i,4).text()) )            

        # messaggio nella systray
        if self.e_message_systray.isChecked():
            v_message_systray = 1
        else:
            v_message_systray = 0
                
        # messaggio nella systray
        if self.e_hide_name_in_systray_title.isChecked():
            v_hide_name_in_systray_title = 1
        else:
            v_hide_name_in_systray_title = 0
        
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

        # indica di minimizzare la window nella systray
        if self.e_minimize_window_to_systray.isChecked():
            v_minimize_window_to_systray = 1
        else:
            v_minimize_window_to_systray = 0

        # indica avvio programma in modalità maschera
        if self.e_start_in_mask_mode == 1:
            v_start_in_mask_mode = True
        else:
            v_start_in_mask_mode = False

		# scrivo nel file un elemento json contenente le informazioni inseriti dell'utente
        v_json ={'remember_window_pos': v_remember_window_pos,                 
                 'hide_window_border': v_hide_window_border,                 
                 'dark_theme': v_dark_theme,		         
                 'splash' : v_splash,                 
                 'server': v_server,
                 'users': v_users,
                 'message_systray':v_message_systray,
                 'hide_name_in_systray_title': v_hide_name_in_systray_title,
                 'hide_toolbar':v_hide_toolbar,
                 'loop_when_connect':v_loop_when_connect,
                 'opacity':self.e_opacity.value(),
                 'clear_chat_timer': self.e_clear_chat_timer.value(),
                 'minimize_window_timer': self.e_minimize_window_timer.value(),
                 'general_zoom': self.e_general_zoom.value(),
                 'minimize_window_to_systray': v_minimize_window_to_systray,
                 'mask_window_timer': self.e_mask_window_timer.value(),
                 'mask_window_message': self.e_mask_window_message.toPlainText(),
                 'start_in_mask_mode': v_start_in_mask_mode
                }
        
        # scrittura delle preferenze (nel registro nel caso di Windows)        
        v_settings = QSettings("Echo Utility", "Echo")
        v_settings.setValue("preferences", v_json)   
        
        message_info('Preferences saved! Restart Echo to see the changes ;-)')

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QApplication([])
    application = win_preferences_class()
    application.show()
    sys.exit(app.exec())        