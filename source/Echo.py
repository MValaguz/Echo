#  _____     _           
# | ____|___| |__   ___  
# |  _| / __| '_ \ / _ \ 
# | |__| (__| | | | (_) |
# |_____\___|_| |_|\___/ 
#                                                                 
#  Creato da.....: Marco Valaguzza
#  Piattaforma...: Python3.13 con libreria PyQt6
#  Data inizio...: 17/07/2019
#  Descrizione...: Programma per la gestione di una chat tra due utenti
#
#  Note..........: Il programma funziona in questo modo. 
#                  Uno dei due utenti deve attivarlo come "Server" e l'altro utente si collega come client a quel server.
#                  Attenzione! L'elenco dei pc deve contenere anche il PC di chi fa da server!
#                  Il formato è il seguente (nome_pc_nella_rete alias_nome_pc indirizzo_ip):
#                  PC-MVALAGUZ Marco  10.0.47.9
#                  PC-SVITALI  Simone 10.0.47.10
#                 
#                  Nel codice del programma si fa riferimento a server per quella parte di programma che si metterà in ascolto
#                  mentre ci si riferisce a client con quella parte di programma che si mette in comunicazione con il server.
#                  Client e server sono ruoli svolti da questo codice e non ci sono procedure esterne ad esso.

# Librerie sistema
import os
import socket
import sys
import time
# Libreria per pyinstaller che serve per capire dove creata la dir temporanea di esecuzione
import tempfile
# Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
# Nota bene! Quando tramite pyinstaller verrà creato l'eseguibile, tutti i file della cartella qtdesigner verranno messi 
#            nella cartella principale e questa istruzione di cambio path di fatto non avrà alcun senso. Serve dunque solo
#            in fase di sviluppo. 
sys.path.append('qtdesigner')
# Librerie grafiche 
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
# Definizione interfaccia QtDesigner
from Echo_ui import Ui_Echo_window
from program_info_ui import Ui_Program_info
from help_ui import Ui_Help
from preferences import preferences_class, win_preferences_class
from utilita import message_error, message_question_yes_no, cripta_messaggio, decripta_messaggio
# Definizione dei temi (è stato definito anche il tema normal perché non venivano prese le dimensioni corrette dei font)
from dark_theme import dark_theme_definition
from normal_theme import normal_theme_definition
        
# carico preferenze
o_global_preferences = preferences_class()

class class_Echo_thread(QThread):
    """
       Questa classe serve per creare un thread separato che si metta in ascolto di eventuali messaggi
       al parametro p_tool_chat dovrà essere passata la classe tools_chat (di fatto l'oggetto principale di questo programma
    """
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, p_tools_chat):
        QThread.__init__(self)
        # mi prendo in pancia l'oggetto di partenza perché poi avrò bisogno delle sue variabili
        self.tools_chat = p_tools_chat

    def run(self):
        # ciclo di scambio messaggi fino a quando con si chiude la connessione
        errore = False
        while not errore:
            if self.tools_chat.tipo_connessione == 'server':
                try:
                    # mi metto in attesa di un messaggio e una volta ricevuto lo decripto
                    message = decripta_messaggio(self.tools_chat.connection.recv(1024))
                except:
                    message = 'CONNECTION_LOST'
                    errore = True
            elif self.tools_chat.tipo_connessione == 'client':
                try:
                    # mi metto in attesa di un messaggio e una volta ricevuto lo decripto
                    message = decripta_messaggio(self.tools_chat.soc.recv(1024))
                except:
                    message = 'CONNECTION_LOST'
                    errore = True
            # restituisco il messaggio
            self.signal.emit(message)

class MyPlainTextEdit(QPlainTextEdit):
    """
        Questa classe modifica il comportamento del widget qplaintextedit disattivando lo zoom con il mouse, perché
        lo zoom viene gestito in altro modo con CTRL++ e CTRL+- tramite voci di menu
    """
    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:            
            return
        super().wheelEvent(event)

class Echo_window_class(QMainWindow, Ui_Echo_window):
    """
        Programma per la gestione di una chat tra utenti
        Nota Bene: E' stata costruita anche la classe Echo_thread
                   Questa classe è quella che si occupa di ricevere i messaggi. Perché una classe?
                   Perchè in questo modo il main del programma rimane sempre attivo e mentre si è in 
                   attesa di un messaggio se ne può inviare un altro. La classe Echo_thread riceve 
                   in ingresso la stessa classe class_tools_chat in modo da avere in pancia le sue variabili.
    """
    def __init__(self, p_arg1, p_arg2):
        # p_arg1 = S = connessione automatica come server
        #          C = connessione automatica come client
        # p_arg2 = nome del server o del client 
        self.p_arg1 = p_arg1
        self.p_arg2 = p_arg2
        
        # incapsulo la classe grafica da qtdesigner
        super(Echo_window_class, self).__init__()        
        # creo oggetto settings per salvare posizione della window e delle dock
        self.settings = QSettings("Echo Utility", "Echo")
        self.setupUi(self)

        # il widget dei messaggi viene sostituito con un widget personalizzato che disattiva lo zoom tramite ctrl+rotella del mouse
        self.custom_editor = MyPlainTextEdit(self)        
        self.verticalLayout_2.replaceWidget(self.o_messaggi, self.custom_editor)  # Sostituzione nel layout
        self.o_messaggi.deleteLater()  # Rimuovi il vecchio widget        
        self.o_messaggi = self.custom_editor

        # imposto opacità della window (Valore tra 0 (trasparente) e 1 (opaco))
        if o_global_preferences.opacity != 100:            
            self.setWindowOpacity(o_global_preferences.opacity/100)  

        self._margin = 8  # Spessore della zona sensibile per il ridimensionamento
        self._resizing = False
        self._resize_direction = None
        self._mouse_pos = QPoint()

        # carico posizione e dimensione window
        self.default_window_pos = self.geometry()                    
        self.carico_posizione_window()
        
        # tolgo i bordi alla window (in modo che sia più invisibile) cambio anche il titolo in modo che 
        # se ridotto ad icona non sia visibile
        if o_global_preferences.hide_window_border:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint) 

        # nascondo la toolbar se richiesto
        if o_global_preferences.hide_toolbar:            
            self.actionHide_toolbar.setChecked(True)
            self.toolBar.hide()
        else:
            self.actionHide_toolbar.setChecked(False)
            self.toolBar.show()
                                   
        ###
        # Dalle preferenze carico il menu con elenco dei server e degli user        
        # e imposto eventuali default
        ###
        self.action_elenco_server = []
        self.action_elenco_user = []
        if len(o_global_preferences.elenco_server) > 0:            
            self.menuAs_Server.addSeparator()
            self.action_elenco_server = []
            for rec in o_global_preferences.elenco_server:
                v_qaction = QAction()
                v_qaction.setCheckable(True)
                v_qaction.setText(rec[0])
                v_qaction.setData('MENU_SERVER')                
                # controllo se ho ricevuto dei parametri all'avvio del programma e se si, reimposto le preferenze di menu        
                if self.p_arg1 == '-S' and self.p_arg2 != '':
                    if self.p_arg2 == rec[0].upper():                        
                        v_qaction.setChecked(True)
                # altrimenti imposto come check quella indicata nelle preferenze
                elif rec[2] == '1':
                    v_qaction.setChecked(True)
                self.action_elenco_server.append(v_qaction)
                self.menuAs_Server.addAction(v_qaction)               

        if len(o_global_preferences.elenco_user) > 0:
            self.menuAs_Client.addSeparator()
            self.action_elenco_user = []
            for rec in o_global_preferences.elenco_user:
                v_qaction = QAction()
                v_qaction.setCheckable(True)
                v_qaction.setText(rec[0])
                v_qaction.setData('MENU_USER')
                # controllo se ho ricevuto dei parametri all'avvio del programma e se si, reimposto le preferenze di menu        
                if self.p_arg1 == '-C' and self.p_arg2 != '':
                    if self.p_arg2 == rec[0].upper():                        
                        v_qaction.setChecked(True)
                # altrimenti imposto come check quella indicata nelle preferenze
                elif rec[3] == '1':
                    v_qaction.setChecked(True)
                self.action_elenco_user.append(v_qaction)
                self.menuAs_Client.addAction(v_qaction)   
            
        # impostazione delle var dell'oggetto
        self.record_server = []
        self.record_user = []
        self.tipo_connessione = ''
        self.systray_attiva = False        
        self.systray_pos_window = self.geometry()  
        self.alias_client_name = ''
        self.alias_server_name = ''

        # imposto icona della preferenza splash window
        self.actionSplash_window.setChecked(o_global_preferences.splash)
        
        # imposto icona della preferenza messaggio quando systray attiva
        self.actionMessage_systray.setChecked(o_global_preferences.message_systray)

        # definizione dei pennelli per scrivere il testo in diversi colori
        if o_global_preferences.dark_theme:
            self.pennello_blu = QTextCharFormat()
            self.pennello_blu.setForeground(QColor('#3399FF'))
            self.pennello_nero = QTextCharFormat()
            self.pennello_nero.setForeground(QColor("white"))
        else:
            self.pennello_blu = QTextCharFormat()
            self.pennello_blu.setForeground(QColor("blue"))
            self.pennello_nero = QTextCharFormat()
            self.pennello_nero.setForeground(QColor("black"))

        # label (in formato html) che viene visualizzata quando si attiva la maschera che nasconde la chat come se fosse un programma di to-do
        # se richiesto viene sovrapposta già all'avvio del programma
        # e se richiesto, il contenuto viene preso da un file dove premendo ctrl-s verrà salvato (formato testo!)
        self.mask_window_message = QTextEdit('', self)
        self.mask_window_message.hide()  
        self.mask_window_timer_active = False
        if o_global_preferences.start_in_mask_mode:
            self.slot_mask_window_timer()        
        else:            
            # imposto il fuoco sul campo di invio messaggio 
            self.e_invia_messaggio.setFocus()        

        # per smistare i segnali che arrivano dal menù, utilizzo un apposito connettore
        # attenzione! eventi come la selezione di info, ecc. passa tramite i segnali standard
        self.menuBar.triggered[QAction].connect(self.smistamento_voci_menu)        
            
        # se è stato scelto di avere il tema dei colori scuro, lo carico
        # Attenzione! La parte principale del tema colori rispetta il meccanismo di QT library
        #             Mentre per la parte di QScintilla ho dovuto fare le impostazioni manuali (v. definizione del lexer)
        if o_global_preferences.dark_theme:                    
            self.setStyleSheet(dark_theme_definition())    
        else:
            self.setStyleSheet(normal_theme_definition())    

        # attivo evento di cambiamento di focus sulla window 
        QApplication.instance().focusChanged.connect(self.on_focusChanged)   

        # se richiesto dalle preferenze, viene creato un timer per la pulizia automatica della chat
        if o_global_preferences.clear_chat_timer != 0:             
            self.clear_chat_timer = QTimer(self)
            self.clear_chat_timer.setInterval(o_global_preferences.clear_chat_timer*1000) 
            self.clear_chat_timer.timeout.connect(self.slot_pulisci_chat)
            
        # se richiesto dalle preferenze, viene creato un timer per minimizzare la window
        if o_global_preferences.minimize_window_timer != 0:             
            self.minimize_window_timer = QTimer(self)
            self.minimize_window_timer.setInterval(o_global_preferences.minimize_window_timer*1000) 
            self.minimize_window_timer.timeout.connect(self.slot_minimize_window_timer)            

        # se richiesto dalle preferenze, viene creato un timer per mascherare il contenuto della window, simulando un programma di to-do
        if o_global_preferences.mask_window_timer != 0:             
            self.mask_window_timer = QTimer(self)
            self.mask_window_timer.setInterval(o_global_preferences.mask_window_timer*1000) 
            self.mask_window_timer.timeout.connect(self.slot_mask_window_timer)            

        # se tramite parametri d'ingresso è stato richiesto di avviare in modalità server automatica...
        if self.p_arg1 == '-S' and self.p_arg2 != '':
            self.slot_crea_server_chat()
        # se tramite parametri d'ingresso è stato richiesto di avviare in modalità client automatica...
        if self.p_arg1 == '-C' and self.p_arg2 != '':
            self.slot_crea_client_chat()        
                    
    def event(self, event):
        """
           Intercetta qualsiasi attività da parte dell'utente e resetta i timer che minimizzano la window, che puliscono la chat e che mascherano la chat
           Tramite questo meccanismo i timer iniziano a conteggiare solo a partire dall'ultima inittività dell'utente dentro la window
        """                        
        if event.type() == QEvent.Type.KeyPress:            
            # premuta combinazione CTRL+S e maschera della window è attiva -->  
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_S and self.mask_window_timer_active and o_global_preferences.mask_filename != '':                                            
                open(o_global_preferences.mask_filename,'w').write(self.mask_window_message.toPlainText())
            
        #if event.type() in (QEvent.Type.MouseMove, QEvent.Type.KeyPress, QEvent.Type.MouseButtonPress, QEvent.Type.WindowActivate):
        if o_global_preferences.minimize_window_timer != 0:                    
            self.reset_minimize_window_timer()
        if o_global_preferences.clear_chat_timer != 0:                    
            self.reset_clear_chat_timer()
        if o_global_preferences.mask_window_timer != 0:                    
            self.reset_mask_window_timer()
            
        # esco rilasciando l'evento normalmente
        return super().event(event)    
    
    def smistamento_voci_menu(self, p_slot):
        """
            Contrariamente al solito, le voci di menù non sono pilotate da qtdesigner ma direttamente
            dal connettore al menu che riporta a questa funzione che poi si occupa di fare lo smistamento.            
        """      
        global o_global_preferences

        #print('Voce di menù --> ' + str(p_slot.data()))    
        #print('Voce di menù --> ' + p_slot.text())    

        ###
        # Refresh del menu
        ###
        if str(p_slot.data()) == 'MENU_SERVER':
            # disattivo la check sulla parte server
            for action in self.action_elenco_server:            
                action.setChecked(False)

            # attivo la posizione di menu che è stata selezionata (server)
            for action in self.action_elenco_server:            
                if action.text() == p_slot.text():                    
                    action.setChecked(True)                                           

        if str(p_slot.data()) == 'MENU_USER':
            # disattivo la check sulla parte user
            for action in self.action_elenco_user:
                action.setChecked(False)
                        
            # attivo la posizione di menu che è stata selezionata (user)
            for action in self.action_elenco_user:            
                if action.text() == p_slot.text():
                    action.setChecked(True)    

        if str(p_slot.text()) == 'Reset window position':            
            # reimposto la dimensione della window con le dimensioni definite a designer            
            self.setGeometry(self.default_window_pos)

        if str(p_slot.text()) == 'Show/Hide toolbar':            
            # mostra o nasconde la toolbar        
            if self.actionHide_toolbar.isChecked():
                self.toolBar.hide()           
            else:
                self.toolBar.show()           
        
        if str(p_slot.text()) == 'Show/Hide window border':            
            # mostra o nasconde i bordi della window        
            if o_global_preferences.hide_window_border:                
                o_global_preferences.hide_window_border = False
                self.setWindowFlags(Qt.WindowType.WindowTitleHint) 
            else:                
                o_global_preferences.hide_window_border = True
                self.setWindowFlags(Qt.WindowType.FramelessWindowHint) 
            self.show()

    def closeEvent(self, event):
        """
           Intercetto l'evento di chiusura 
           Questa funzione sovrascrive quella nativa di QT 
        """     
        # salvo posizione della window se richiesto dalle preferenze
        self.salvo_posizione_window()
        
        # se la systray è stata aperta, la chiudo
        if self.systray_attiva:
            self.systray_icon.hide()

    def on_focusChanged(self, old, now):
        """
           Intercetto evento che indica la perdita del focus sulla window principale
        """
        # se la window principale perde il focus, pulisco il titolo; in questo modo all'arrivo 
        # di un messaggio, sarà possibile da parte dell'utente, capire che è cambiato qualcosa
        if now == None and self.windowTitle().find('Echo') == -1:
            self.imposta_titolo_window(False)
    
    def changeEvent(self, event):
        """
           Intercetto l'evento che indica alla finestra di riaprirsi dalla barra delle window
           e ne azzero il titolo. In realtà questo evento prende tutto quello che succede alla window... 
        """        
        if event.type() == QEvent.Type.WindowStateChange:            
            if event.type() == QEvent.Type.WindowStateChange:
                # da minimizzata passa a massimizzata...cambio il titolo e azzero eventuale icona sulla systray
                if event.oldState() and Qt.WindowState.WindowMinimized:
                    if self.windowTitle() == '_____.._____':
                        self.imposta_titolo_window(False)
                    if self.systray_attiva:     
                        self.systray_icon.setIcon(QIcon("icons:Echo.ico"))
                # da massimizzata passa a minimizzata....azzero il titolo (utente capisce che sono in attesa e non ci sono messaggi)
                elif event.oldState() == Qt.WindowState.WindowNoState or self.windowState() == Qt.WindowState.WindowMaximized:
                    self.imposta_titolo_window(False)

    def carico_posizione_window(self):
        """
            Leggo dal file la posizione della window (se richiesto dalle preferenze)
        """
        # se utente ha richiesto di salvare la posizione della window...
        if o_global_preferences.remember_window_pos:
            # recupero dal registro di sistema (regedit) la posizione della window
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)                        
            # recupero dal registro di sistema (regedit) la posizione delle dock                
            windowstate = self.settings.value("windowstate")
            if windowstate:
                self.restoreState(windowstate)                        
                                
    def salvo_posizione_window(self):
        """
           Salvo in un file la posizione della window (se richiesto dalle preferenze)
           Questo salvataggio avviene automaticamente alla chiusura di Echo
        """
        # se utente ha richiesto di salvare la posizione della window...
        if o_global_preferences.remember_window_pos:
            # salvo nel registro di sistema (regedit) la posizione della window
            self.settings.setValue("geometry", self.saveGeometry())            
            # salvo nel registro di sistema (regedit) la posizione delle dock
            self.settings.setValue("windowstate", self.saveState())                            

    def imposta_titolo_window(self, p_active):
        """
           Imposta il titolo della window e la relativa icona.
           In pratica quando non ci sono messaggi il titolo della window è vuoto e l'icona della window è grigia
           mentre quando arriva un messaggio il titolo si riempie e l'icona della window si colora
        """
        if p_active:
            self.setWindowTitle('_____.._____')
            v_icon = QIcon()
            v_icon.addPixmap(QPixmap("icons:Echo.ico"), QIcon.Mode.Normal, QIcon.State.Off)
            self.setWindowIcon(v_icon)                                    
            # se programma è ridotto a systray...
            if self.systray_attiva:
                # se richiesto dalle preferenze emetto un messaggio sulla systray
                if self.actionMessage_systray.isChecked():
                    self.systray_icon.showMessage('Echo', 'New message!')
                # cambio il colore dell'icona in systray con icona rossa 
                self.systray_icon.setIcon(QIcon("icons:Echo_red.ico"))
        else:
            self.setWindowTitle(' ')
            v_icon = QIcon()
            v_icon.addPixmap(QPixmap("icons:Echo_grey.ico"), QIcon.Mode.Normal, QIcon.State.Off)
            self.setWindowIcon(v_icon)            
            # se programma è ridotto a systray...
            if self.systray_attiva:
                # cambio il colore dell'icona in systray con icona neutra
                self.systray_icon.setIcon(QIcon("icons:Echo.ico"))

    def reset_minimize_window_timer(self):
        """
           Avvia/Riavvia il timer che minimizza la window
        """
        try:
            self.minimize_window_timer.start()
        except:
            pass
    
    def slot_minimize_window_timer(self):
        """
           Richiamato dal timer che minimizza la window. Nel caso sia attivo apposito flagh, la window viene minimizzata nella systray
        """
        if o_global_preferences.minimize_window_to_systray:
            self.slot_riduci_a_systray()
        else:
            self.slot_minimize_window()
    
    def slot_minimize_window(self):
        """
           Minizza la window
        """
        self.showMinimized()
    
    def slot_zoom_in(self):
        """
           Zoom dei caratteri
        """        
        v_font = self.o_messaggi.font()
        v_font.setPointSize(v_font.pointSize()+1)        
        self.o_messaggi.setFont(v_font)        

        v_font = self.e_invia_messaggio.font()
        v_font.setPointSize(v_font.pointSize()+1)        
        self.e_invia_messaggio.setFont(v_font)

    def slot_zoom_out(self):
        """
           Zoom dei caratteri
        """        
        v_font = self.o_messaggi.font()
        v_font.setPointSize(v_font.pointSize()-1)        
        self.o_messaggi.setFont(v_font)

        v_font = self.e_invia_messaggio.font()
        v_font.setPointSize(v_font.pointSize()-1)
        self.e_invia_messaggio.setFont(v_font)
    
    def slot_riduci_a_systray(self):
        """
           Riduce programma a systray
        """
        # creo e attivo la systray solo se non è già attiva
        if not self.systray_attiva:            
            self.systray_attiva = True
            self.systray_icon = QSystemTrayIcon(QIcon("icons:Echo.ico"), parent=app)
            self.systray_icon.activated.connect(self.riapri_da_systray)                        
            # imposto titolo del tooltip della modalità systray (se richiesto dalla preferenza ci metto il nome utente)
            if not o_global_preferences.hide_name_in_systray_title:
                if self.tipo_connessione == 'server':
                    self.systray_icon.setToolTip("Echo with " + self.alias_server_name)
                else:
                    self.systray_icon.setToolTip("Echo with " + self.alias_client_name)
            # altrimenti solo nome dell'applicazione
            else:
                self.systray_icon.setToolTip("Echo")
            self.systray_icon.show()
        # forzo icona neutrale nella systray             
        else:
            self.systray_icon.setIcon(QIcon("icons:Echo.ico"))

        # salvo attuale posizione della window (questo perché si è notato che quando si ripristina da systray, a volte perde il posizionamento)
        self.systray_pos_window = self.geometry()        

        # nascondo la finestra
        self.hide()

    def riapri_da_systray(self):
        """
           Rende nuovamente visibile la finestra della chat (riportando l'icona a colore neutro)
        """
        self.show()
        self.setGeometry(self.systray_pos_window)        
        self.systray_icon.setIcon(QIcon("icons:Echo.ico"))

    def slot_program_info(self):
        """
           Visualizzo la finestra con le info dello sviluppo 
        """
        self.dialog_program_info = QDialog()
        self.win_program_info = Ui_Program_info()
        self.win_program_info.setupUi(self.dialog_program_info)
        self.dialog_program_info.show()
    
    def slot_help(self):
        """
           Visualizzo la finestra di help (è stato fatto così perché poi il programma viene
           pacchettizzato in un unico file)
        """
        self.dialog_help = QDialog()
        self.win_help = Ui_Help()
        self.win_help.setupUi(self.dialog_help)
        self.dialog_help.show()

    def slot_preferences(self):
        """
           Gestione delle preferenze
        """
        self.my_app = win_preferences_class()        
        self.my_app.show()   
        
    def reset_clear_chat_timer(self):
        """
           Avvia/Riavvia il timer che pulisce la char
        """
        try:
            self.clear_chat_timer.start()
        except:
            pass
    
    def slot_pulisci_chat(self):
        """
           Pulisco la chat
        """                
        self.o_messaggi.clear()        
        self.e_invia_messaggio.clear()

    def slot_crea_server_chat(self):
        """
           Attiva l'applicazione lato server in attesa di connessione da parte di un client                      
        """             
        # prendo la voce del menu server che è stata selezionata, per capire con quale server mi devo mettere in attesa
        v_found = False
        for action in self.action_elenco_server:            
            if action.isChecked():
                v_found = True
                # ricerco i dati del server nelle relative preferenze
                for rec in o_global_preferences.elenco_server:
                    if rec[0] == action.text():
                       self.record_server = rec

        if not v_found or self.record_server is None:
            message_error('You must select a server from server-menu!')
            return 'ko'

        # ricerco il nome del PC di esecuzione del programma
        soc = socket.socket()
        self.host_name = socket.gethostname()                
                
        # nella lista dei pc ricerco il nome del pc per ricavarne l'alias e inviarlo al client che si sta collegando
        self.name = ''
        v_error = False
        for rec in o_global_preferences.elenco_user:
            if self.host_name == rec[0]:
                self.name = rec[1]
                self.ip = rec[2]

        if self.name == '':
            message_error('PC name ' + self.host_name + ' not found into preferences!')
            v_error = True
        
        # l'istruzione di ricerca del proprio ip è stata sostituita in quanto se presenti più schede di rete
        # prendeva il primo ip che gli capitava. Ora indirizzo ip viene ricavato dal file della lista pc
        # viene presa la porta impostata nelle preferenze 
        self.port = int(self.record_server[1])        
        #self.ip = socket.gethostbyname(self.host_name)                        
        soc.bind((self.ip, self.port))
                        
        if not v_error:
            # prova a localizzare usando il socket
            soc.listen(1)            
            self.setWindowTitle('Waiting ' + self.record_server[0] + ' IP=' + str(self.ip) + ', PORT=' + self.record_server[1])
            # sostituisce la freccia del mouse con icona "clessidra"
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))       
            # attivo la maschera
            self.actionMask.setChecked(True)
            self.slot_mask_window_timer()            
            self.repaint()
            # da questo punto il programma entra in attesa di una connessione da parte di un client
            # addr è una tupla che contiene due elementi di cui il primo è l'indirizzo ip
            self.connection, self.addr = soc.accept()                        
            # ottiene una connessione dal lato client
            self.client_name = self.connection.recv(1024)
            self.client_name = self.client_name.decode()
            # ripristino icona freccia del mouse
            QApplication.restoreOverrideCursor()    
            # disattivo la maschera            
            self.actionMask.setChecked(False)
            self.slot_mask_window_timer()            
            # se lanciato con parametri di input minimizzo la window
            if self.p_arg1 != '':
                self.showMinimized()
            # indico l'utente che si è connesso            
            self.setWindowTitle(self.client_name + ' has connected')            
            self.l_invia_messaggio.setText('Send to ' + self.client_name + ':')
            # dall'indirizzo IP cerco il colore attribuito all'utente e lo imposto nelle label "Messages:" e "Send to:"
            for rec in o_global_preferences.elenco_user:
                if self.addr[0] in rec:                    
                    v_colore_user = rec[4]                    
                    self.l_messaggi.setStyleSheet("color: " + v_colore_user + ";") 
                    self.l_invia_messaggio.setStyleSheet("color: " + v_colore_user + ";")                     
            # invio l'alias di chi fa da server
            self.connection.send(self.name.encode())            
            # disattivo i button di server e client
            self.attiva_disattiva_voci_menu_connessione(False)            
            
            self.tipo_connessione = 'server'
            self.alias_server_name = self.client_name
            
            # creo un job che si mette in attesa di una risposta così da lasciare libera l'applicazione da questo lavoro
            # viene passato al thread l'oggetto chat
            self.thread_in_attesa = class_Echo_thread(self)
            # collego il thread con la relativa funzione
            self.thread_in_attesa.signal.connect(self.ricevo_il_messaggio)
            self.thread_in_attesa.start()

    def slot_crea_client_chat(self):
        """
           Si collega ad un PC dove questa stessa applicazione è stata attivata in modalità server
           Da notare come lato cliente deve essere selezionato un server....questo perché su PC di destinazione 
           Echo potrebbe essere attivo con più porte server!
        """
        v_error = False

        # prendo la voce del menu server che è stata selezionata, per capire a quale porta dovrò richiedere l'accesso
        v_found = False
        for action in self.action_elenco_server:            
            if action.isChecked():
                v_found = True
                # ricerco i dati del server nelle relative preferenze
                for rec in o_global_preferences.elenco_server:
                    if rec[0] == action.text():
                       self.record_server = rec

        if not v_found or self.record_server is None:
            message_error('You must select a server from server-menu!')
            return 'ko'

        # prendo la voce del menu client che è stata selezionata, per capire con quale modalità server mi devo mettere in attesa
        v_found = False
        for action in self.action_elenco_user:            
            if action.isChecked():
                v_found = True
                # ricerco i dati dello user nelle relative preferenze
                for rec in o_global_preferences.elenco_user:
                    if rec[0] == action.text():
                       self.record_user = rec

        if not v_found or self.record_user is None:
            message_error('You must select a user from client-menu!')
            v_error = True

        if not v_error:
            # Get the hostname, IP Address from socket and set Port
            self.soc = socket.socket()
            self.client_name = socket.gethostname()
            self.ip = socket.gethostbyname(self.client_name)
            self.setWindowTitle(self.client_name + '({})'.format(self.ip))
            self.server_host = self.record_user[2]
            if self.server_host == '':
                message_error('PC not found!')
                v_error = True

            if not v_error:
                # alias..lo prendo per inviarlo al server a cui mi sto collegando
                self.alias_client_name = self.record_user[1]
                # nella lista degli user ricerco il nome del mio pc per ricavarne l'alias e inviarlo al server a cui mi sto collegando
                self.alias_client_name = ''
                for rec in o_global_preferences.elenco_user:
                    if self.client_name == rec[0]:
                        self.alias_client_name = rec[1]

                if self.alias_client_name == '':
                    message_error('Alias name not valid!')
                    v_error = True

            if not v_error:                
                # prendo numero della porta a cui collegarmi
                self.port = int(self.record_server[1])      
                # connessione al server
                v_repeat = True
                while v_repeat :                         
                    try:
                        self.soc.connect((self.server_host, self.port))
                        v_repeat = False
                    except:
                        if not o_global_preferences.loop_when_connect:
                            message_error('Error to connect!')
                            v_error = True
                            v_repeat = False
                        else:
                            # il tentativo è ogni 5 secondi
                            time.sleep(5)              
                            pass

                if not v_error:
                    self.soc.send(self.alias_client_name.encode())
                    # mi metto in attesa che il server mi restituisca il suo alias
                    self.alias_server_name = self.soc.recv(1024)
                    self.alias_server_name = self.alias_server_name.decode()
                    self.setWindowTitle('{} has joined'.format(self.alias_server_name))                                                            
                    self.l_invia_messaggio.setText('Send to ' + self.alias_server_name + ':')
                    # disattivo i button di server e client
                    self.attiva_disattiva_voci_menu_connessione(False)
                    # se lanciato con parametri di input minimizzo la window
                    if self.p_arg1 != '':
                        self.showMinimized()

                    self.tipo_connessione = 'client'
                    # creo un job che si mette in attesa di una risposta così da lasciare libera l'applicazione da questo lavoro
                    # viene passato al thread l'oggetto chat
                    self.thread_in_attesa = class_Echo_thread(self)
                    # collego il thread con la relativa funzione
                    self.thread_in_attesa.signal.connect(self.ricevo_il_messaggio)
                    self.thread_in_attesa.start()
    
    def ricevo_il_messaggio(self, p_messaggio):
        """
           Ho ricevuto in messaggio dal thread che è in ascolto
        """
        if p_messaggio == 'CONNECTION_LOST':
            message_error('Connection lost!')
            self.imposta_titolo_window(False)
            self.attiva_disattiva_voci_menu_connessione(True)
        elif p_messaggio != '':
            # nettifico il cursore nel testo, cambio il pennello e inserisco il messaggio
            v_cursor = self.o_messaggi.textCursor()
            v_cursor.clearSelection()            
            v_cursor.movePosition(QTextCursor.MoveOperation.End)
            self.o_messaggi.setTextCursor(v_cursor)
            self.o_messaggi.setCurrentCharFormat(self.pennello_blu)
            self.o_messaggi.appendPlainText(p_messaggio)
            # se richiesto, faccio lampeggiare la finestra 
            if self.actionSplash_window.isChecked():
                self.activateWindow()
            
            # in qualsiasi caso cambio il titolo per far capire che è arrivato un nuovo messaggio             
            self.imposta_titolo_window(True)

    def slot_invia_il_messaggio(self):
        """
           Invia messaggio al destinatario
        """
        if self.e_invia_messaggio.text() != '':
            if self.tipo_connessione == 'server':
                # invio il messaggio al destinatario in modalità server
                try:
                    self.connection.send(cripta_messaggio(self.e_invia_messaggio.text()))
                except:
                    message_error('Connection lost!')
                    self.attiva_disattiva_voci_menu_connessione(True)
                # nettifico il cursore nel testo, cambio il pennello e inserisco il messaggio
                v_cursor = self.o_messaggi.textCursor()
                v_cursor.clearSelection()
                v_cursor.movePosition(QTextCursor.MoveOperation.End)
                self.o_messaggi.setTextCursor(v_cursor)
                self.o_messaggi.setCurrentCharFormat(self.pennello_nero)
                self.o_messaggi.appendPlainText(self.e_invia_messaggio.text())
                self.e_invia_messaggio.clear()
            elif self.tipo_connessione == 'client':
                # invio il messaggio al destinatario in modalità client
                try:
                    self.soc.send(cripta_messaggio(self.e_invia_messaggio.text()))
                except:
                    message_error('Connection lost!')
                    self.attiva_disattiva_voci_menu_connessione(True)
                # nettifico il cursore nel testo, cambio il pennello e inserisco il messaggio
                v_cursor = self.o_messaggi.textCursor()
                v_cursor.clearSelection()
                v_cursor.movePosition(QTextCursor.MoveOperation.End)
                self.o_messaggi.setTextCursor(v_cursor)
                self.o_messaggi.setCurrentCharFormat(self.pennello_nero)
                self.o_messaggi.appendPlainText(self.e_invia_messaggio.text())
                self.e_invia_messaggio.clear()        

    def attiva_disattiva_voci_menu_connessione(self, p_flag):
        """
           Attiva/disattiva le voci di menu della connessione
        """        
        self.actionStart_as_server.setEnabled(p_flag)
        self.actionClient_connection.setEnabled(p_flag)

    def reset_mask_window_timer(self):
        """
           Avvia/Riavvia il timer che maschera il contenuto della chat, simulando che sia un programma di to-do
        """
        try:
            if not self.mask_window_timer_active:
                self.mask_window_timer.start()
        except:
            pass
    
    def slot_mask_window_timer(self):
        """
           Crea sopra la window un sorta di programma to-do
        """
        if not self.actionMask.isChecked():                                            
            # se la maschera era un file di testo --> lo salvo (nel caso sia stato modificato)
            if o_global_preferences.mask_filename != '':                                            
                open(o_global_preferences.mask_filename,'w').write(self.mask_window_message.toPlainText())
            self.mask_window_timer_active = False
            self.reset_mask_window_timer()
            self.mask_window_message.hide()                
            self.e_invia_messaggio.setFocus()                        
        else:
            # indico che la maschera è attiva
            self.mask_window_timer_active = True                    
            
            # carico il contenuto dal file se indicato
            if o_global_preferences.mask_filename != '':
                try:
                    self.mask_window_message.setText(open(o_global_preferences.mask_filename,'r').read())      
                except:
                    pass
            else:
                self.mask_window_message.setText('Please select a text file for the mask ;-)')      
            
            if o_global_preferences.dark_theme:
                self.mask_window_message.setStyleSheet("background-color: black; color: white; font-size: 10px;")                
            else:
                self.mask_window_message.setStyleSheet("background-color: white; color: black; font-size: 10px;")                
            
            self.mask_window_message.resize(self.size())          
            self.mask_window_message.show()  

            # nel caso sia richiesto che all'avvio del programma deve comparire la maschera, il timer non sarà attivo, e stessa cosa anche quando si è in attesa di connessione
            try:
                self.mask_window_timer.stop() 
            except:
                pass

# -------------------
# AVVIO APPLICAZIONE
# -------------------
if __name__ == "__main__":    
    # se il programma è eseguito da pyinstaller, cambio la dir di riferimento passando a dove si trova l'eseguibile
    # in questo modo dovrebbe riuscire a trovare tutte le risorse
    if getattr(sys, 'frozen', False): 
        # si usa questa istruzione quando è stato creato un onefile come eseguibile...che quindi viene decompresso al momento
        v_dir_eseguibile = sys._MEIPASS
        os.chdir(v_dir_eseguibile)
        QDir.addSearchPath('icons', 'icons/')        
    
    # controllo se richiamato tramite parametri da riga di comando
    try:
        v_arg1 = sys.argv[1].upper()
    except:
        v_arg1 = ''
    try:
        v_arg2 = sys.argv[2].upper()
    except:
        v_arg2 = ''            

    # eventuale preferenza di zoom di tutto il programma
    os.environ['QT_SCALE_FACTOR'] = str(o_global_preferences.general_zoom / 100)

    # avvio di Echo    
    app = QApplication([])            
    application = Echo_window_class(v_arg1, v_arg2)         
    application.show()    
    sys.exit(app.exec())    