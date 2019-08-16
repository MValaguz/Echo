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
                 Attenzione! Il file elenco_pc.txt deve contenere i nomi pc a cui connettersi compreso chi fa da server.
                 Il formato è il seguente (nome_pc_nella_rete alias_nome_pc indirizzo_ip):
                 PC-MVALAGUZ Marco 10.0.47.9
                 PC-ABERLEND Ale 10.0.47.1
                 
                 Nel codice del programma si fa riferimento a server per quella parte di programma che si metterà in ascolto
                 mentre ci si riferisce a client con quella parte di programma che si mette in comunicazione con il server.
                 Client e server sono ruoli svolti da questo codice e non ci sono procedure esterne ad esso.
                 
                 L'interfaccia di base è stata creata usando qtdesigner; è di fatto il motivo per cui esiste una cartella di nome "ui" dove ci sono i file .ui che possono essere usati da qtdesigner
                 Attenzione! Questi file sono stati usati solo come base per la creazione del programma. 
                 
                 La struttura delle directory:
                 - ui: contiene i file creati tramite qtdesigner
                 - old: vecchi file usati per avere esempi con cui costruire il programma
                 - compila: contiene MChat_compile.bat che è lo script con cui è possibile creare l'eseguibile. 
                            Esso si appoggia sul programma pyinstaller e sul file di configurazione MChar.spec il cui contenuto ha tutti i riferimenti per la compilazione
                 - icons: cartella delle icone di programma
                 - help: cartella con in files di help
"""
#Librerie sistema
import os
import time
import socket
import sys
#from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal
# Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
# Libreria per criptare i messaggi 
import base64

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

def message_error(p_message):
    """
       visualizza messaggio di errore usando interfaccia qt
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText(p_message)
    msg.setWindowTitle("Error")
    msg.exec_()        
    
#--------------------------
# CLASSE THREAD
#--------------------------                                            
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
            if self.tools_chat.tipo_connessione=='server':
                try:
                    # mi metto in attesa di un messaggio e una volta ricevuto lo decripto
                    message = decripta_messaggio( self.tools_chat.connection.recv(1024) )                    
                except:
                    message = 'CONNECTION_LOST'                                                                
                    errore = True                
            elif self.tools_chat.tipo_connessione=='client':
                try:
                    # mi metto in attesa di un messaggio e una volta ricevuto lo decripto
                    message = decripta_messaggio( self.tools_chat.soc.recv(1024) )                    
                except:
                    message = 'CONNECTION_LOST'
                    errore = True
            # restituisco il messaggio        
            self.signal.emit(message)               
                
#------------------------------------------------
# CLASSE VISUALIZZAZIONE FINESTRA INFO PROGRAMMA
#------------------------------------------------                                                
class ui_window_about(object):
    def setupUi(self, window_about):
        window_about.setObjectName("window_about")
        window_about.resize(330, 140)
        window_about.setWindowTitle("About MChat")      
        # disattiva il punto di domanda sulla window 
        window_about.setWindowFlags( QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.buttonBox = QtWidgets.QDialogButtonBox(window_about)
        self.buttonBox.setGeometry(QtCore.QRect(240, 110, 75, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(window_about)
        self.label.setGeometry(QtCore.QRect(5, 10, 100, 100))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("icons/qt.gif"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(window_about)
        self.label_2.setGeometry(QtCore.QRect(110, 20, 214, 88))
        self.label_2.setText("<html><head/><body><p>MChat</p><p>is a little chat program for ethernet network.</p><p>Developed by Marco Valaguzza (C) 2019</p><p>with Phyton and Qt library</p></body></html>")
        self.label_2.setObjectName("label_2")
        
        self.buttonBox.accepted.connect(window_about.accept)
        self.buttonBox.rejected.connect(window_about.reject)
        QtCore.QMetaObject.connectSlotsByName(window_about)        

#------------------------------------------------
# CLASSE FINESTRA PRINCIPALE
#------------------------------------------------                                                
class class_tools_chat(object):
    """
        Programma per la gestione di una chat tra utenti
        Nota Bene: E' stata costruita anche la classe mchat_thread
                   Questa classe è quella che si occupa di ricevere i messaggi. Perché una classe?
                   Perchè in questo modo il main del programma rimane sempre attivo e mentre si è in 
                   attesa di un messaggio se ne può inviare un altro. La classe mchat_thread riceve 
                   in ingresso la stessa classe class_tools_chat in modo da avere in pancia le sue variabili.
    """            
    def setupUi(self, MainWindow):
        # definizione dell'interfaccia grafica (parte di questo codice è stato creato tramite il programma qtdesigner e poi copiato qui all'interno
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(290, 318)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/MChat.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.nome_finestra = u"MChat 1.1"
        MainWindow.setWindowTitle(self.nome_finestra)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setText("Messages:")
        self.verticalLayout.addWidget(self.label)        
        self.o_messaggi = QtWidgets.QTextEdit(self.centralwidget)
        self.o_messaggi.setReadOnly(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.o_messaggi.sizePolicy().hasHeightForWidth())
        self.o_messaggi.setSizePolicy(sizePolicy)
        self.o_messaggi.setObjectName("o_messaggi")
        self.verticalLayout.addWidget(self.o_messaggi)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Send:")
        self.verticalLayout.addWidget(self.label_2)
        self.e_invia_messaggio = QtWidgets.QLineEdit(self.centralwidget)
        self.e_invia_messaggio.setObjectName("e_invia_messaggio")
        self.verticalLayout.addWidget(self.e_invia_messaggio)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setWindowTitle("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionConnect = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/call.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnect.setIcon(icon1)
        self.actionConnect.setObjectName("actionConnect")
        self.actionConnect.setText("Connect")
        self.actionConnect.setToolTip("Connect to a server PC as a client")        
        self.actionCreate_Server = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/create_server.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCreate_Server.setIcon(icon2)
        self.actionCreate_Server.setObjectName("actionCreate_Server")
        self.actionCreate_Server.setText("Create Server")
        self.actionCreate_Server.setToolTip("Create a server connection on my own computer")
         
        self.nomi_pc = QtWidgets.QComboBox(MainWindow)
        self.nomi_pc.setObjectName("nomi_pc")
        
        self.actionClear_my_chat = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/clear.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClear_my_chat.setIcon(icon3)
        self.actionClear_my_chat.setObjectName("actionClear_my_chat")
        self.actionClear_my_chat.setText("Clear my chat")
        self.actionClear_my_chat.setToolTip("Clear my chat (F1 shortcut key)")
        self.actionClear_my_chat.setShortcut("F1")
        
        self.actionReduce_to_systray = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/systray.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReduce_to_systray.setIcon(icon4)
        self.actionReduce_to_systray.setObjectName("actionReduce_to_systray")
        self.actionReduce_to_systray.setText("Reduce to systray")
        self.actionReduce_to_systray.setToolTip("Reduce to systray (F2 shortcut key)")
        self.actionReduce_to_systray.setShortcut("F2")
        
        self.actionProgram_Info = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/info.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProgram_Info.setIcon(icon5)
        self.actionProgram_Info.setObjectName("actionProgram_Info")
        self.actionProgram_Info.setText("Program Info")
        self.actionProgram_Info.setToolTip("Program Info")
        
        self.actionHelp = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/help.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon6)
        self.actionHelp.setObjectName("actionHelp")
        self.actionHelp.setText("Help")
        self.actionHelp.setToolTip("Help")        
        
        self.toolBar.addAction(self.actionCreate_Server)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.nomi_pc)        
        self.toolBar.addAction(self.actionConnect)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear_my_chat)
        self.toolBar.addAction(self.actionReduce_to_systray)
        self.toolBar.addAction(self.actionProgram_Info)
        self.toolBar.addAction(self.actionHelp)
        # collego logicamente l'etichetta con item di testo (per avere l'effetto responsive dell'interfaccia)
        self.label.setBuddy(self.o_messaggi)
        self.label_2.setBuddy(self.e_invia_messaggio)
                
        self.actionClear_my_chat.triggered.connect(self.pulisci_chat)
        self.actionProgram_Info.triggered.connect(self.show_program_info)
        self.actionReduce_to_systray.triggered.connect(self.riduci_a_systray)
        self.actionHelp.triggered.connect(self.visualizza_help)
        self.actionCreate_Server.triggered.connect(self.crea_server_chat)
        self.actionConnect.triggered.connect(self.crea_client_chat)
        self.e_invia_messaggio.returnPressed.connect(self.invia_il_messaggio)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # carico elenco dei pc
        self.carica_elenco_pc()
        self.tipo_connessione = ''   
        
        # imposto il fuoco sul campo di invio messaggio
        self.e_invia_messaggio.setFocus()
                
        # definizione dei pennelli per scrivere il testo in diversi colori 
        self.pennello_rosso = QtGui.QTextCharFormat()
        self.pennello_rosso.setForeground(QtCore.Qt.red)        
        self.pennello_blu = QtGui.QTextCharFormat()
        self.pennello_blu.setForeground(QtCore.Qt.blue)        
        self.pennello_nero = QtGui.QTextCharFormat()
        self.pennello_nero.setForeground(QtCore.Qt.black)  
           
        # imposto la var che controlla se la systray è utilizzata o meno
        self.systray_attiva = False    
        
        # imposto la funzione che si attiva alla chiusura del programma
        app.aboutToQuit.connect(self.chiusura_programma)
        
    def riduci_a_systray(self):
        """
           Riduce programma a systray
        """
        # creo e attivo la systray solo se non è già attiva
        if not self.systray_attiva:            
            self.systray_attiva = True
            self.systray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon('icons\MChat.ico'), parent=app)
            self.systray_icon.activated.connect(self.riapri_da_systray)
            self.systray_icon.setToolTip("MChat")
            self.systray_icon.show()
        
        # nascondo la finestra     
        MainWindow.hide()             
        
    def riapri_da_systray(self):
        """
           Rende nuovamente visibile la finestra della chat
        """
        MainWindow.show()         
                                
    def carica_elenco_pc(self):
        """
           Carica in una lista l'elenco dei PC 
        """        
        try:
            v_file = open('computer_list.txt', 'r')
            v_ok = True
        except:
            message_error('File "computer_list.txt" not found!\nCreate it respecting this format:\nPC-NAME, ALIAS, IP_ADDRESS\n(es. PC-MVALAGUZ Marco 10.0.47.9)')            
            v_ok = False

        if v_ok:
            elenco_pc = []
            for v_line in v_file:
                elenco_pc.append( v_line.rstrip('\n').split() )
            v_file.close()                                    
                        
            self.alias = []
            self.ip_address = []
            for v_list_line in elenco_pc:                                
                self.nomi_pc.addItem(v_list_line[0])
                self.alias.append(v_list_line[1])
                self.ip_address.append(v_list_line[2])                            
            # sposto indice a -1 in modo che all'inizio il combobox non abbia valore selezionato
            self.nomi_pc.setCurrentIndex(-1)            
        
    def show_program_info(self):
        """
           Visualizzo la finestra con le info dello sviluppo 
        """        
        window_about = QtWidgets.QDialog()
        my_window = ui_window_about()
        my_window.setupUi(window_about)
        window_about.exec_()     
        
    def pulisci_chat(self):
        """
           Pulisco la chat
        """        
        self.o_messaggi.clear()        
        
    def visualizza_help(self):
        """
           Visualizzo help
        """
        os.system("start help/help.html")
        
    def crea_server_chat(self):
        """
           Attiva l'applicazione lato server in attesa di connessione da parte di un client
        """
        # emetto messaggio di stato        
        self.statusbar.showMessage('Setup Server...')
        time.sleep(1)
        # get the hostname, IP Address from socket and set Port
        soc = socket.socket()
        self.host_name = socket.gethostname()
        self.ip = socket.gethostbyname(self.host_name)
        self.port = 1234
        soc.bind((self.host_name, self.port))
        self.statusbar.showMessage( self.host_name + ' ({})'.format(self.ip) )
        #self.name = self.host_name
        # nella lista dei pc ricerco il nome del pc per ricavarne l'alias e inviarlo al client che si sta collegando
        self.name = ''
        v_error = False                        
        for i in range(len(self.nomi_pc)):                           
            if self.host_name == self.nomi_pc.itemText(i):                
               self.name = self.alias[i]            
            
        if self.name == '':
           message_error('PC name ' + self.host_name + ' not found in elenco_pc.txt!')                        
           v_error = True
        
        if not v_error:
            # try to locate using socket
            soc.listen(1) 
            self.statusbar.showMessage('Waiting for incoming connections...')
            self.connection, self.addr = soc.accept()                        
            self.statusbar.showMessage('Received connection from ' + str(self.addr[0]) + ' (' + str(self.addr[1]) + ')')            
            time.sleep(1)
            self.statusbar.showMessage('Connection Established!')            
            time.sleep(1)
            self.statusbar.showMessage('Connected From: ' + '({})'.format(self.addr[0],self.addr[0]) )
            time.sleep(1)
            # in qualsiasi caso faccio lampeggiare la finestra (nel caso fosse dietro a tutte le altre l'utente capisce che è successo qualcosa)                            
            MainWindow.activateWindow()   
            # get a connection from client side
            self.client_name = self.connection.recv(1024)
            self.client_name = self.client_name.decode()                    
            self.statusbar.showMessage( self.client_name.upper() + ' has connected')            
            # in qualsiasi caso faccio lampeggiare la finestra (nel caso fosse dietro a tutte le altre l'utente capisce che è successo qualcosa)                
            MainWindow.activateWindow()            
            # invio l'alias di chi fa da server
            self.connection.send(self.name.encode())
            
            self.tipo_connessione='server'
            
            # creo un job che si mette in attesa di una risposta così da lasciare libera l'applicazione da questo lavoro
            # viene passato al thread l'oggetto chat
            self.thread_in_attesa = class_mchat_thread(self)   
            # collego il thread con la relativa funzione 
            self.thread_in_attesa.signal.connect(self.ricevo_il_messaggio)            
            self.thread_in_attesa.start()
            
    def crea_client_chat(self):    
        """
           Si collega ad un PC dove questa stessa applicazione è stata attivata in modalità server
        """                
        v_error = False
        # controllo che sia stato selezionato un PC a cui connettersi (esso deve essere attivo come server)        
        if self.nomi_pc.currentText()=='':
            message_error('Select a PC to connect!')            
            v_error = True
        
        if not v_error:
            # creazione dlla wait window
            self.statusbar.showMessage('Client Server...' )            
            time.sleep(1)
            #Get the hostname, IP Address from socket and set Port
            self.soc = socket.socket()
            self.client_name = socket.gethostname()
            self.ip = socket.gethostbyname(self.client_name)            
            self.statusbar.showMessage(self.client_name + '({})'.format(self.ip) )            
            self.server_host = self.ip_address[ self.nomi_pc.currentIndex() ]                        
            if self.server_host == '':
                message_error('PC not found!')
                v_error = True
            
            if not v_error:    
                # nella lista dei pc ricerco il nome del pc per ricavarne l'alias e inviarlo al server a cui mi sto collegando
                self.alias_client_name = ''
                for i in range(len(self.nomi_pc)):                                    
                    if self.client_name == self.nomi_pc.itemText(i):                
                        self.alias_client_name = self.alias[i]            
                    
                if self.alias_client_name == '':
                    message_error('PC name not found in elenco_pc.txt!')                 
                    v_error = True
                
            if not v_error:
                self.port = 1234
                self.statusbar.showMessage('Trying to connect to the server: {}, ({})'.format(self.server_host, self.port) )                
                time.sleep(1)
                try:
                    self.soc.connect((self.server_host, self.port))
                except:
                    message_error('Error to connect!')            
                    v_error = True
                
                if not v_error:
                    self.statusbar.showMessage('Connected...')                    
                    self.soc.send(self.alias_client_name.encode())
                    # mi metto in attesa che il server mi restituisca il suo alias
                    self.alias_server_name = self.soc.recv(1024)
                    self.alias_server_name = self.alias_server_name.decode()
                    self.statusbar.showMessage( '{} has joined...'.format(self.alias_server_name) )                    
            
                    self.tipo_connessione='client'
            
                    # creo un job che si mette in attesa di una risposta così da lasciare libera l'applicazione da questo lavoro
                    # viene passato al thread l'oggetto chat
                    self.thread_in_attesa = class_mchat_thread(self)
                    # collego il thread con la relativa funzione 
                    self.thread_in_attesa.signal.connect(self.ricevo_il_messaggio)            
                    self.thread_in_attesa.start()

                # sposto indice a -1 in modo che all'inizio il combobox non abbia valore selezionato
                self.nomi_pc.setCurrentIndex(-1)        
                
    def ricevo_il_messaggio(self, p_messaggio):
        """
           Ho ricevuto in messaggio dal thread che è in ascolto
        """
        if p_messaggio == 'CONNECTION_LOST':
            message_error('Connection lost!')                        
            self.statusbar.showMessage('')                                
        elif p_messaggio != '':
            self.o_messaggi.setCurrentCharFormat(self.pennello_blu)            
            self.o_messaggi.append(p_messaggio)                                                                                       
            # in qualsiasi caso faccio lampeggiare la finestra (nel caso fosse dietro a tutte le altre l'utente capisce che è successo qualcosa)                
            MainWindow.activateWindow()
            # se programma è ridotto a systray manda messaggio
            if self.systray_attiva:
                self.systray_icon.showMessage('MChat','You have a new message :-)')            
                
    def invia_il_messaggio(self):
        """
           Invia messaggio al destinatario
        """
        if self.tipo_connessione=='server':
            # invio il messaggio al destinatario in modalità server    
            try:                
                self.connection.send( cripta_messaggio( self.e_invia_messaggio.text() ) )        
            except:
                message_error('Connection lost!')                                            
                        
            self.o_messaggi.setCurrentCharFormat(self.pennello_nero)
            self.o_messaggi.append(self.e_invia_messaggio.text())            
            self.e_invia_messaggio.clear()
        elif self.tipo_connessione=='client':
            # invio il messaggio al destinatario in modalità client    
            try:                
                self.soc.send( cripta_messaggio( self.e_invia_messaggio.text() ) )
            except:
                message_error('Connection lost!')                                            
            
            self.o_messaggi.setCurrentCharFormat(self.pennello_nero)
            self.o_messaggi.append(self.e_invia_messaggio.text())            
            self.e_invia_messaggio.clear()   
            
    def chiusura_programma(self):
        """
           Chiude il programma 
        """        
        # se la systray è stata aperta, la chiudo        
        if self.systray_attiva:
            self.systray_icon.hide()                
            
# -------------------
# AVVIO APPLICAZIONE
# -------------------    
if __name__ == "__main__":
    # se l'applicazione è stata compilata con pyinstaller con modalità onefile, quando andrà in esecuzione l'exe, devo cambiare la dir di lavoro
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)    
    # creazione della classe principale e avvio del programma
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    my_chat = class_tools_chat()
    my_chat.setupUi(MainWindow)
    MainWindow.show()    
    sys.exit(app.exec_())

