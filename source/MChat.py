# -*- coding: utf-8 -*-

"""
 __  __  _____ _           _   
|  \/  |/ ____| |         | |  
| \  / | |    | |__   __ _| |_ 
| |\/| | |    | '_ \ / _` | __|
| |  | | |____| | | | (_| | |_ 
|_|  |_|\_____|_| |_|\__,_|\__|

 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria PyQt5
 Data..........: 17/07/2019
 Descrizione...: Programma per la gestione di una chat tra due utenti
 
 Note..........: Il programma funziona in questo modo. 
                 Uno dei due utenti deve attivarlo come "Server" e l'altro utente si collega come client a quel server.
                 Attenzione! L'elenco dei pc deve contenere anche il PC di chi fa da server!
                 Il formato è il seguente (nome_pc_nella_rete alias_nome_pc indirizzo_ip):
                 PC-MVALAGUZ Marco 10.0.47.9
                 PC-ABERLEND Ale 10.0.47.1
                 
                 Nel codice del programma si fa riferimento a server per quella parte di programma che si metterà in ascolto
                 mentre ci si riferisce a client con quella parte di programma che si mette in comunicazione con il server.
                 Client e server sono ruoli svolti da questo codice e non ci sono procedure esterne ad esso.
"""
# Librerie sistema
import os
import socket
import sys
# Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
# Nota bene! Quando tramite pyinstaller verrà creato l'eseguibile, tutti i file della cartella qtdesigner verranno messi 
#            nella cartella principale e questa istruzione di cambio path di fatto non avrà alcun senso. Serve dunque solo
#            in fase di sviluppo. 
sys.path.append('qtdesigner')
# Librerie grafiche 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# Libreria per criptare i messaggi
import base64
# Definizione interfaccia QtDesigner
from MChat_ui import Ui_MChat_window
from program_info_ui import Ui_Program_info
from preferences import preferences_class, win_preferences_class
from utilita import message_error

def cripta_messaggio(messaggio):
    """
       Cripta una stringa con la chiave mchat. Il valore restituito è di tipo bytes, lo stesso che deve essere passato
       all'invio dei dati su rete
    """
    key = 'mchat'
    enc = []
    for i in range(len(messaggio)):
        key_c = key[i % len(key)]
        enc_c = (ord(messaggio[i]) + ord(key_c)) % 256
        enc.append(enc_c)
    return base64.urlsafe_b64encode(bytes(enc))

def decripta_messaggio(messaggio):
    """
       decripta una stringa con la chiave mchat. Il valore restituito è di tipo stringa, lo stesso che deve essere 
       passato ai campi di visualizzazione 
    """
    key = 'mchat'
    dec = []
    enc = base64.urlsafe_b64decode(messaggio)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

class class_mchat_thread(QThread):
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

class MChat_window_class(QMainWindow, Ui_MChat_window):
    """
        Programma per la gestione di una chat tra utenti
        Nota Bene: E' stata costruita anche la classe mchat_thread
                   Questa classe è quella che si occupa di ricevere i messaggi. Perché una classe?
                   Perchè in questo modo il main del programma rimane sempre attivo e mentre si è in 
                   attesa di un messaggio se ne può inviare un altro. La classe mchat_thread riceve 
                   in ingresso la stessa classe class_tools_chat in modo da avere in pancia le sue variabili.
    """
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(MChat_window_class, self).__init__()        
        self.setupUi(self)
        
        # carico preferenze
        self.preferences = preferences_class('C:\\MChat\\MChat.ini')

        # carico posizione e dimensione window
        self.carico_posizione_window()

        ###
        # Dalle preferenze carico il menu con elenco dei server e degli user
        # Per i primi due server collego lo shortcut F1 e F2
        ###
        self.action_elenco_server = []
        self.action_elenco_user = []
        if len(self.preferences.elenco_server) > 0:            
            self.menuAs_Server.addSeparator()
            self.action_elenco_server = []
            for rec in self.preferences.elenco_server:
                v_qaction = QAction()
                v_qaction.setCheckable(True)
                v_qaction.setText(rec[0])
                v_qaction.setData('MENU_SERVER')
                self.action_elenco_server.append(v_qaction)
                self.menuAs_Server.addAction(v_qaction)               

        if len(self.preferences.elenco_user) > 0:
            self.menuAs_Client.addSeparator()
            self.action_elenco_user = []
            for rec in self.preferences.elenco_user:
                v_qaction = QAction()
                v_qaction.setCheckable(True)
                v_qaction.setText(rec[0])
                v_qaction.setData('MENU_USER')
                self.action_elenco_user.append(v_qaction)
                self.menuAs_Client.addAction(v_qaction)               

        # impostazione delle var dell'oggetto
        self.record_server = []
        self.record_user = []
        self.tipo_connessione = ''
        self.systray_attiva = False
        self.splash_window = self.preferences.splash
        self.slot_splash_window()

        # imposto il fuoco sul campo di invio messaggio
        self.e_invia_messaggio.setFocus()

        # definizione dei pennelli per scrivere il testo in diversi colori
        self.pennello_rosso = QTextCharFormat()
        self.pennello_rosso.setForeground(Qt.red)
        self.pennello_blu = QTextCharFormat()
        self.pennello_blu.setForeground(Qt.blue)
        self.pennello_nero = QTextCharFormat()
        self.pennello_nero.setForeground(Qt.black)

        # imposto il font per la parte di messaggistica                
        if self.preferences.font_editor != '':
            v_split = self.preferences.font_editor.split(',')            
            v_font = QFont(str(v_split[0]),int(v_split[1]))
            if len(v_split) > 2 and v_split[2] == ' BOLD':
                v_font.setBold(True)
            self.o_messaggi.setFont(v_font)    
            self.e_invia_messaggio.setFont(v_font)

        # per smistare i segnali che arrivano dal menù, utilizzo un apposito connettore
        # attenzione! eventi come la selezione di help, info, passa tramite i segnali standard
        self.menuBar.triggered[QAction].connect(self.smistamento_voci_menu)        

    def smistamento_voci_menu(self, p_slot):
        """
            Contrariamente al solito, le voci di menù non sono pilotate da qtdesigner ma direttamente
            dal connettore al menu che riporta a questa funzione che poi si occupa di fare lo smistamento.            
        """        
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
        
    def carico_posizione_window(self):
        """
            Leggo dal file la posizione della window (se richiesto dalle preferenze)
        """
        # se utente ha richiesto di salvare la posizione della window...
        if self.preferences.remember_window_pos:
            if os.path.isfile('C:\\MChat\\MChat_window_pos.ini'):
                v_file = open('C:\\MChat\\MChat_window_pos.ini','r')
                # al momento leggo solo la prima riga che contiene la dimensione della mainwindow
                v_my_window_pos = v_file.readline().rstrip('\n').split()                                
                if v_my_window_pos[0] == 'MainWindow':
                    # finestra massimizzata
                    if v_my_window_pos[1] == 'MAXIMIZED':
                        self.showMaximized()
                    # finestra a dimensione specifica
                    else:
                        self.setGeometry(int(v_my_window_pos[1]), int(v_my_window_pos[2]), int(v_my_window_pos[3]), int(v_my_window_pos[4]))    
                v_file.close()
                                
    def salvo_posizione_window(self):
        """
           Salvo in un file la posizione della window (se richiesto dalle preferenze)
           Questo salvataggio avviene automaticamente alla chiusura di MSql
        """
        # se utente ha richiesto di salvare la posizione della window...
        if self.preferences.remember_window_pos:
            v_file = open('C:\\MChat\\MChat_window_pos.ini','w')
            if self.isMaximized():
                v_file.write("MainWindow MAXIMIZED")
            else:
                o_pos = self.geometry()            
                o_rect = o_pos.getRect()                        
                v_file.write("MainWindow " + str(o_rect[0]) + " " + str(o_rect[1]) + " " +  str(o_rect[2]) + " " + str(o_rect[3]))
            v_file.close()
        
    def slot_splash_window(self):
        """
           Attiva o disattiva l'opzione che controlla lo splash window
        """
        icon1 = QIcon()                
        if self.splash_window:
            self.splash_window = False
            icon1.addPixmap(QPixmap(":/icons/icons/exclamation.gif"), QIcon.Normal, QIcon.Off)            
            self.statusbar.showMessage('Splash window deactivated')
        else:
            self.splash_window = True
            icon1.addPixmap(QPixmap(":/icons/icons/dexclamation.gif"), QIcon.Normal, QIcon.Off)            
            self.statusbar.showMessage('Splash window activated')
        self.actionSplash_window.setIcon(icon1)                
    
    def slot_riduci_a_systray(self):
        """
           Riduce programma a systray
        """
        # creo e attivo la systray solo se non è già attiva
        if not self.systray_attiva:            
            self.systray_attiva = True
            self.systray_icon = QSystemTrayIcon(QIcon(":/icons/icons/MChat.ico"), parent=app)
            self.systray_icon.activated.connect(self.riapri_da_systray)
            self.systray_icon.setToolTip("MChat")
            self.systray_icon.show()

        # nascondo la finestra
        self.hide()

    def riapri_da_systray(self):
        """
           Rende nuovamente visibile la finestra della chat
        """
        self.show()

    def slot_program_info(self):
        """
           Visualizzo la finestra con le info dello sviluppo 
        """
        self.dialog_program_info = QDialog()
        self.win_program_info = Ui_Program_info()
        self.win_program_info.setupUi(self.dialog_program_info)
        self.dialog_program_info.show()

    def slot_preferences(self):
        """
           Gestione delle preferenze
        """
        self.my_app = win_preferences_class('C:\\MChat\\MSql.ini')        
        self.my_app.show()   
    
    def slot_pulisci_chat(self):
        """
           Pulisco la chat
        """
        self.o_messaggi.clear()        

    def slot_visualizza_help(self):
        """
           Visualizzo help
        """
        os.system("start help/help.html")

    def slot_crea_server_chat(self):
        """
           Attiva l'applicazione lato server in attesa di connessione da parte di un client                      
        """        
        # prendo la voce del menu server che è stata selezionata, per capire con quale modalità server mi devo mettere in attesa
        v_found = False
        for action in self.action_elenco_server:            
            if action.isChecked():
                v_found = True
                # ricerco i dati del server nelle relative preferenze
                for rec in self.preferences.elenco_server:
                    if rec[0] == action.text():
                       self.record_server = rec

        if not v_found or self.record_server is None:
            message_error('You must select a server from server-menu!')
            return 'ko'

        # imposto il colore della chat in base alle preferenze
        self.o_messaggi.setStyleSheet("QPlainTextEdit {background-color: " + self.record_server[2] + ";}")
        self.e_invia_messaggio.setStyleSheet("QLineEdit {background-color: " + self.record_server[2] + ";}")

        # ricerco il nome del PC di esecuzione del programma
        soc = socket.socket()
        self.host_name = socket.gethostname()                
                
        # nella lista dei pc ricerco il nome del pc per ricavarne l'alias e inviarlo al client che si sta collegando
        self.name = ''
        v_error = False
        for rec in self.preferences.elenco_user:
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
            # try to locate using socket
            soc.listen(1)            
            self.statusbar.showMessage(self.record_server[0] + ' IP=' + str(self.ip) + ', PORT=' + self.record_server[1])
            # sostituisce la freccia del mouse con icona "clessidra"
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))       
            self.repaint()
            # da questo punto il programma entra in attesa di una connessione da parte di un client
            self.connection, self.addr = soc.accept()            
            # get a connection from client side
            self.client_name = self.connection.recv(1024)
            self.client_name = self.client_name.decode()
            # ripristino icona freccia del mouse
            QApplication.restoreOverrideCursor()    
            # indico l'utente che si è connesso
            self.statusbar.showMessage(self.client_name + ' has connected')
            # invio l'alias di chi fa da server
            self.connection.send(self.name.encode())            
            
            self.tipo_connessione = 'server'
            
            # creo un job che si mette in attesa di una risposta così da lasciare libera l'applicazione da questo lavoro
            # viene passato al thread l'oggetto chat
            self.thread_in_attesa = class_mchat_thread(self)
            # collego il thread con la relativa funzione
            self.thread_in_attesa.signal.connect(self.ricevo_il_messaggio)
            self.thread_in_attesa.start()

    def slot_crea_client_chat(self):
        """
           Si collega ad un PC dove questa stessa applicazione è stata attivata in modalità server
           Da notare come lato cliente deve essere selezionato un server....questo perché su PC di destinazione 
           MChat potrebbe essere attivo con più porte server!
        """
        v_error = False

        # prendo la voce del menu server che è stata selezionata, per capire a quale porta dovrò richiedere l'accesso
        v_found = False
        for action in self.action_elenco_server:            
            if action.isChecked():
                v_found = True
                # ricerco i dati del server nelle relative preferenze
                for rec in self.preferences.elenco_server:
                    if rec[0] == action.text():
                       self.record_server = rec

        if not v_found or self.record_server is None:
            message_error('You must select a server from server-menu!')
            return 'ko'

        # imposto il colore della chat in base alla preferenze
        self.o_messaggi.setStyleSheet("QPlainTextEdit {background-color: " + self.record_server[2] + ";}")
        self.e_invia_messaggio.setStyleSheet("QLineEdit {background-color: " + self.record_server[2] + ";}")

        # prendo la voce del menu client che è stata selezionata, per capire con quale modalità server mi devo mettere in attesa
        v_found = False
        for action in self.action_elenco_user:            
            if action.isChecked():
                v_found = True
                # ricerco i dati dello user nelle relative preferenze
                for rec in self.preferences.elenco_user:
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
            self.statusbar.showMessage(self.client_name + '({})'.format(self.ip))
            self.server_host = self.record_user[2]
            if self.server_host == '':
                message_error('PC not found!')
                v_error = True

            if not v_error:
                # alias..lo prendo per inviarlo al server a cui mi sto collegando
                self.alias_client_name = self.record_user[1]

                if self.alias_client_name == '':
                    message_error('Alias name not valid!')
                    v_error = True

            if not v_error:                
                # prendo numero della porta a cui collegarmi
                self.port = int(self.record_server[1])                
                try:
                    self.soc.connect((self.server_host, self.port))
                except:
                    message_error('Error to connect!')
                    v_error = True

                if not v_error:
                    self.soc.send(self.alias_client_name.encode())
                    # mi metto in attesa che il server mi restituisca il suo alias
                    self.alias_server_name = self.soc.recv(1024)
                    self.alias_server_name = self.alias_server_name.decode()
                    self.statusbar.showMessage('{} has joined...'.format(self.alias_server_name))

                    self.tipo_connessione = 'client'

                    # creo un job che si mette in attesa di una risposta così da lasciare libera l'applicazione da questo lavoro
                    # viene passato al thread l'oggetto chat
                    self.thread_in_attesa = class_mchat_thread(self)
                    # collego il thread con la relativa funzione
                    self.thread_in_attesa.signal.connect(self.ricevo_il_messaggio)
                    self.thread_in_attesa.start()

    def ricevo_il_messaggio(self, p_messaggio):
        """
           Ho ricevuto in messaggio dal thread che è in ascolto
        """
        if p_messaggio == 'CONNECTION_LOST':
            message_error('Connection lost!')
            self.statusbar.showMessage('')
        elif p_messaggio != '':
            self.o_messaggi.setCurrentCharFormat(self.pennello_blu)
            self.o_messaggi.appendPlainText(p_messaggio)
            # in qualsiasi caso faccio lampeggiare la finestra (nel caso fosse dietro a tutte le altre l'utente capisce che è successo qualcosa)
            if self.splash_window:
                self.activateWindow()
            # se programma è ridotto a systray manda messaggio
            if self.systray_attiva:
                self.systray_icon.showMessage('MChat', 'You have a new message :-)')

    def slot_invia_il_messaggio(self):
        """
           Invia messaggio al destinatario
        """
        if self.tipo_connessione == 'server':
            # invio il messaggio al destinatario in modalità server
            try:
                self.connection.send(cripta_messaggio(self.e_invia_messaggio.text()))
            except:
                message_error('Connection lost!')

            self.o_messaggi.setCurrentCharFormat(self.pennello_nero)
            self.o_messaggi.appendPlainText(self.e_invia_messaggio.text())
            self.e_invia_messaggio.clear()
        elif self.tipo_connessione == 'client':
            # invio il messaggio al destinatario in modalità client
            try:
                self.soc.send(cripta_messaggio(self.e_invia_messaggio.text()))
            except:
                message_error('Connection lost!')

            self.o_messaggi.setCurrentCharFormat(self.pennello_nero)
            self.o_messaggi.appendPlainText(self.e_invia_messaggio.text())
            self.e_invia_messaggio.clear()

# -------------------
# AVVIO APPLICAZIONE
# -------------------
if __name__ == "__main__":
    app = QApplication([])    
    application = MChat_window_class()         
    application.show()
    sys.exit(app.exec())    