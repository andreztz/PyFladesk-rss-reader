
import sys,webbrowser
import urllib2
from PyQt4.QtCore import QThread, QUrl,SIGNAL,QSize
from PyQt4.QtGui import QApplication,QMainWindow,QIcon
from PyQt4.QtWebKit import QWebView,QWebPage


PORT = 5000
ROOT_URL = 'http://localhost:{}'.format(PORT)
WIDTH = 700
HEIGHT = 500
WINDOW_TITLE = "PyFladesk RSS Reader"

class FlaskThread(QThread):
    def __init__(self, application):
        QThread.__init__(self)
        self.application = application

    def __del__(self):
        self.wait()

    def run(self):
        self.application.run(port=PORT,debug=True, use_reloader=False)


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize (WIDTH , HEIGHT)
        self.setWindowTitle(WINDOW_TITLE)
        self.webView = WebView(self)
        self.setCentralWidget(self.webView)
        

   

class WebView(QWebView):
    def __init__(self ,parent=None):
        super(WebView,self).__init__(parent)

    def dragEnterEvent(self,e):
        e.ignore()

    def dropEvent(self,e):
        e.ignore()

    def contextMenuEvent(self,e):
        pass

    # open links in default browser 
    # stolen from http://stackoverflow.com/a/3188942/1103397 :D
    def linkClicked(self,url): 
        # url = url.toEncoded().data()
        # if url.find('localhost') == -1:
        webbrowser.open(url.toEncoded().data())
    

def provide_GUI_for(application):
    qtapp = QApplication(sys.argv)

    webapp = FlaskThread(application)
    webapp.start()
    
    #when quit app terminate theared
    qtapp.aboutToQuit.connect(webapp.terminate)

    mainWindow = MainWindow()
    # set app icon    
    mainWindow.setWindowIcon(QIcon('static/images/icon-48.png'))
    
    mainWindow.webView.load(QUrl(ROOT_URL))
    
    # prevent open urls in QWebView
    mainWindow.webView.page().setLinkDelegationPolicy(QWebPage.DelegateExternalLinks)
    mainWindow.webView.connect(mainWindow.webView, SIGNAL("linkClicked (const QUrl&)"),mainWindow.webView.linkClicked)
    mainWindow.show()

    return qtapp.exec_()
    


if __name__ == '__main__':
    from routes import app
    provide_GUI_for(app)
