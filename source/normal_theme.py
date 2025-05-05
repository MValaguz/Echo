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
def normal_theme_definition():
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
}"""