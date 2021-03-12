import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebKitWidgets import *

print("Qt5 Version Number is: {0}".format(QT_VERSION_STR))
print("PyQt5 Version is: {}".format(PYQT_VERSION_STR))

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setWindowTitle('加载外部网页的例子')
#         self.setGeometry(0,0,800,480)
#         self.browser=QWebView()
#         #加载外部的web界面
#         self.browser.load(QUrl('https://zhjq.g2world.cn/'))
#         self.browser.show()
#         self.setCentralWidget(self.browser)
# if __name__ == '__main__':
#     app=QApplication(sys.argv)              
#     win=MainWindow()
#     win.show()
#     app.exit(app.exec_())

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('加载外部网页的例子')
        self.setGeometry(0,0,800,480)
        self.browser=QWebEngineView()
        #加载外部的web界面
        self.browser.load(QUrl('https://zhjq.g2world.cn/'))
        
        self.setCentralWidget(self.browser)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.settings = QWebEngineSettings.globalSettings()
        self.settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)
        self.settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=MainWindow()
    win.show()
    app.exit(app.exec_())

# import webbrowser 
# url = "www.baidu.com"
# webbrowser.open(url, new=0, autoraise=True)
# webbrowser.open_new(url)
# webbrowser.open_new_tab(url)