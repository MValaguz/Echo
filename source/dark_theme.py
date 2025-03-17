#  ___  ____ ____   
# / _ \/ ___/ ___|  
#| | | \___ \___ \  
#| |_| |___) |__) | 
# \__\_\____/____/                     
#
# QSS è l'acronimo che indica il "linguaggio" di definizione stile degli oggetti offerti dalla libreria grafica QT
# Normalmente queste info potrebbero essere lette dal file di testo, al momento dell'apertura del programma....ma
# ho scoperto che una volta reso esguibile e pacchettizzato il tutto, il file do questa definizione non veniva recuperato
# presumibilmente per un problema di pathname. A questo punto è stato inserita come var di testo.
#
# Definizione dei colori principali usati da questo tema
# #242424 = "Nero"
# #4a5157 = "Grigio"
# #667078 = "Grigio chiaro"
# #003333 = "Verde petrolio scuro"
# #006666 = "Verde petrolio chiaro"
#
# Nota! Attenzione! L'editor che si basa sulla libreria QScintilla non è sottomesso alle regole del tema (penso per ignoranza mia
#       nel costruire la classe) quindi l'applicazione del tema-dark viene effettuata direttamente nella definizione della classe
#       del lexer ripetendo i codici colori utilizzati in questa definizione.

def dark_theme_definition():
    return """
/*-----QWidget------------------------------------------------------------*/
QWidget
{
	background-color: #242424;
	color: #fff;
	selection-background-color: #fff;
	selection-color: #000;
    alternate-background-color: #4f585e;
}


/*-----QLabel------------------------------------------------------------*/
QLabel
{
	background-color: transparent;
	color: #fff;
}

/*-----QMenuBar------------------------------------------------------------*/
QMenuBar 
{
	background-color: #4a5157;
	color: #fff;
}

QMenuBar::item 
{
	background-color: transparent;	
	padding: 5px;
	padding-left: 15px;
	padding-right: 15px;
}

QMenuBar::item:selected 
{
	background-color: #003333;
	border: 1px solid #006666;
	color: #fff;
}

QMenuBar::item:pressed 
{
	background-color: #006666;
	border: 1px solid #006666;
	color: #fff;
}

/*-----QMenu------------------------------------------------------------*/
QMenu
{
    background-color: #4a5157;
    border: 1px solid #4a5157;
    padding: 10px;
	color: #fff;
}

QMenu::item
{
    background-color: transparent;    
	min-width: 200px;
	padding: 5px;
}

QMenu::separator
{
   	background-color: #242424;
	height: 1px;
}

QMenu::item:disabled
{
    color: gray;
    background-color: transparent;
    padding: 2px 20px 2px 20px;
}

QMenu::item:selected
{
	background-color: #006666;	
	color: #fff;
}

/*-----QToolBar------------------------------------------------------------*/
QToolBar
{
	background-color: #4a5157;	
	border-top: none;
	border-bottom: none;
	border-left: none;
	border-right: none;
}

QToolBar::separator
{
	background-color: #2e2e2e;
	width: 1px;
}

/*-----QListView---------------------------------------------------------------*/
QListView
{
 background-color: #4a5157;
}

/*-----QTreeView---------------------------------------------------------------*/
QTreeView
{
 background-color: #4a5157;
}

/*-----QToolButton------------------------------------------------------------*/
QToolButton
{
    color: #b1b1b1;
    background-color: 242424;
	border-top: none;
	border-bottom: none;
	border-left: none;
	border-right: none;
    margin-right: 2px;
	padding: 3px;
}

QToolButton:pressed
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
}

QToolButton:checked
{
    background-color: gray;
}

/*-----QLineEdit------------------------------------------------------------*/
QLineEdit
{
	background-color: #4a5157;
	color : #fff;
	border: 1px solid #006666;
	padding: 1px;
	padding-left: 5px;
}

/*-----QComboBox------------------------------------------------------------*/
QComboBox
{
    background-color: #4a5157;
    border: 1px solid #006666;
    padding-left: 6px;
    color: #fff;
    height: 20px;
}

QComboBox::disabled
{
	background-color: #404040;
	color: #656565;
	border-color: #051a39;
}

QComboBox:on
{
    background-color: #4a5157;
	color: #fff;
}

QComboBox QAbstractItemView
{
    background-color: #4a5157;
    color: #ffffff;
    border: 1px solid black;
    selection-background-color: #003333;
	selection-color: #ffffff;
    outline: 0;
}

/*-----QPushButton------------------------------------------------------------*/
QPushButton
{
	/*background-color: #4891b4;*/
	background-color: #006666;
	color: #fff;	
	border-radius: 4px;
	padding: 5px;
}

QPushButton::flat
{
	background-color: transparent;
	border: none;
	color: #000;
}

QPushButton::disabled
{
	background-color: #606060;
	color: #959595;
	border-color: #051a39;
}

QPushButton::hover
{
	background-color: #54aad3;
	border: 1px solid #46a2da;
}

QPushButton::pressed
{
	background-color: #2385b4;
	border: 1px solid #46a2da;
}

QPushButton::checked
{
	background-color: #bd5355;
	border: 1px solid #bd5355;
}

/*-----QTabBar------------------------------------------------------------*/
QTabBar::tab
{
	background-color: #4a5157;
	color: white;
	border-style: solid;
	border-width: 1px;
	border-color: black;
	border-bottom: none;
	padding: 5px;
	padding-left: 15px;
	padding-right: 15px;

}

QTabWidget::pane 
{
	background-color: red;
	border: 1px solid #006666;
	top: 1px;
	bottom: 1px
}

QTabBar::tab:last
{
	margin-right: 0; 
}

QTabBar::tab:first:!selected
{
	color: white;
	border-bottom-style: solid;
	background-color: black;
}

QTabBar::tab:!selected
{
	color: white;
	border-bottom-style: solid;
	background-color: black;
}

QTabBar::tab:selected
{
    color: white;
	border-bottom-style: solid;
	background-color: #006666;
}

/*-----QDockWidget------------------------------------------------------------*/
QDockWidget::title 
{
	background-color: #006666;	
	border: 1px solid;
	padding: 7px;
}

/*-----QTableView & QTableWidget------------------------------------------------------------*/
QTableView
{
    background-color: #242424;
    border: 1px groove #333333;
    color: #f0f0f0;	
    gridline-color: #333333;
    outline : 0;
}

QTableView::disabled
{
    background-color: #242526;
    border: 1px solid #32414B;
    color: #656565;
    gridline-color: #656565;
    outline : 0;
}

QTableView::item:hover 
{
    background-color: #484c58;
    color: #f0f0f0;
}

QTableView::item:selected 
{
    background-color: #484c58;
    border: 2px groove #006666;
    color: #F0F0F0;
}

QTableView::item:selected:disabled
{
    background-color: #1a1b1c;
    border: 2px solid #525251;
    color: #656565;
}

QTableCornerButton::section
{
    background-color: #282830;
}

QHeaderView::section
{
    background-color: #282830;
    color: #fff;
	/*font-weight: bold;*/
    text-align: left;
	padding: 4px;
}

QHeaderView::section:disabled
{
    background-color: #525251;
    color: #656565;
}

QHeaderView::section:checked
{
    background-color: #006666;
}

QHeaderView::section:checked:disabled
{
    color: #656565;
    background-color: #525251;
}

QHeaderView::section::vertical::first,
QHeaderView::section::vertical::only-one
{
    border-top: 0px;
}

QHeaderView::section::vertical
{
    border-top: 0px;
}

QHeaderView::section::horizontal::first,
QHeaderView::section::horizontal::only-one
{
    border-left: 0px;
}

QHeaderView::section::horizontal
{
    border-left: 0px;
}

/*-----QScrollBar------------------------------------------------------------*/
QScrollBar:vertical 
{
   border: none;
   width: 12px;
}

QScrollBar::handle:vertical 
{
   border: none;
   border-radius : 0px;
   background-color: #7a7a7a;
   min-height: 80px;
   width : 12px;
}

QScrollBar::handle:vertical:pressed
{
   background-color: #5d5f60; 
}

QScrollBar::add-line:vertical
{
   border: none;
   background: transparent;
   height: 0px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover 
{
   background-color: transparent;
}

QScrollBar::add-line:vertical:pressed 
{
   background-color: #3f3f3f;
}

QScrollBar::sub-line:vertical
{
   border: none;
   background: transparent;
   height: 0px;
}

QScrollBar::sub-line:vertical:hover 
{
   background-color: transparent;
}

QScrollBar::sub-line:vertical:pressed 
{
   background-color: #3f3f3f;
}

QScrollBar::up-arrow:vertical
{
   width: 0px;
   height: 0px;
   background: transparent;
}

QScrollBar::down-arrow:vertical 
{
   width: 0px;
   height: 0px;
   background: transparent;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
   background-color: #222222;	
}

QScrollBar:horizontal 
{
   border: none;
   height: 12px;
}

QScrollBar::handle:horizontal 
{
   border: none;
   border-radius : 0px;
   background-color: #7a7a7a;
   min-height: 80px;
   height : 12px;
}

QScrollBar::handle:horizontal:pressed
{
   background-color: #5d5f60; 
}

QScrollBar::add-line:horizontal
{
   border: none;
   background: transparent;
   height: 0px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover 
{
   background-color: transparent;
}

QScrollBar::add-line:horizontal:pressed 
{
   background-color: #3f3f3f;
}

QScrollBar::sub-line:horizontal
{
   border: none;
   background: transparent;
   height: 0px;
}

QScrollBar::sub-line:horizontal:hover 
{
   background-color: transparent;
}

QScrollBar::sub-line:horizontal:pressed 
{
   background-color: #3f3f3f;
}

QScrollBar::up-arrow:horizontal
{
   width: 0px;
   height: 0px;
   background: transparent;
}

QScrollBar::down-arrow:horizontal 
{
   width: 0px;
   height: 0px;
   background: transparent;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
   background-color: #222222;	
}

/*-----QCheckBox------------------------------------------------------------*/
QCheckBox{
	background-color: transparent;		
}

QCheckBox::indicator
{    
    background-color: #006666; 
}


QCheckBox::indicator:checked
{
    image:url(://icons//icons//checkbox_dark_theme.png);
    border: 1px solid white;
}

QCheckBox::indicator:unchecked:hover
{
    border: 1px solid white;
}

/*-----QMdiArea---------------------------------------------------------
siccome non ho trovato le impostazioni, ho dovuto inserire 
le impostazioni di stile dentro il programma nella sezione di
inizializzazione dell'oggetto principale
*/

/*-----QScintilla-------------------------------------------------------
siccome non ho trovato le impostazioni, ho dovuto inserire 
le impostazioni di stile dentro il programma nella sezione di
inizializzazione dell'oggetto lexer!
*/

"""