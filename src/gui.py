from PyQt5.QtWidgets import QApplication, QWidget, QListView, QLineEdit, QHBoxLayout, QVBoxLayout, QToolBar, QAction, QCompleter
from PyQt5.QtCore import Qt, QPoint, QSize, QEvent
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLineEdit, QCompleter, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from neo4j import GraphDatabase
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QCompleter, QVBoxLayout, QListWidget, QListWidgetItem, QWidget, QLineEdit, QApplication, QMainWindow, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
import subprocess
import rumps

class CompleterModel(QAbstractListModel):
    def __init__(self, suggestions):
        super().__init__()
        self.suggestions = suggestions
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.suggestions)
    
    def data(self, index, role=Qt.DisplayRole):
        print(index)
        if role == Qt.DisplayRole:
            
            return self.suggestions[index.row()]
            
        return None

class SpotlightSearchBar(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        font = QFont("Helvetica Neue",20)
        self.setPlaceholderText("Search smart with Search Application...")
        self.setFont(font)
        self.setFixedHeight(50)
        self.setFixedWidth(600)
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(5)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)


        self.popup_layout = QVBoxLayout()

        self.container_widget = QListView()
        self.container_layout = QVBoxLayout(self.container_widget)
        
        self.completer.activated.connect(self.on_completer_activated)
        self.textChanged.connect(self.on_text_changed)
        #self.popup_list.itemClicked.connect(self.on_list_item_clicked)
        self.suggestions_list = QListWidget()
        self.suggestions_list.setSpacing(0)
        self.container_layout.addWidget(self.suggestions_list)

        spacer_item = QSpacerItem(30, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.container_layout.addItem(spacer_item)
        
        self.file_suggestions_list = QListWidget()
        self.file_suggestions_list.setSpacing(0)
        self.container_layout.addWidget(self.file_suggestions_list)
        
        #self.popup_layout.addWidget(self.container_widget)
        
        self.completer.setPopup(self.container_widget)
        
        #self.completer.activated.connect(self.on_completer_activated)
        #self.textChanged.connect(self.on_text_changed)
        
        #self.setCompleter(self.completer)


        # Initialize Neo4j driver
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "neo4jneo4j"
        try:
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
        except:
            print("Can't connect to DB.")


        # Add sample suggestions to the completer model
        
        #self.completer_model = CompleterModel(['apple', 'banana', 'orange', 'peach', 'pear'])
        #self.completer.setModel(self.completer_model)


    def on_completer_activated(self, index):

        selected_index = self.completer.popup().currentIndex()
        selected_option = self.completer.popup().model().data(selected_index, Qt.DisplayRole)
        print("Selected option:", selected_option)
        self.setText(selected_option)
        self.setFocus(Qt.OtherFocusReason)
        selected_index = self.completer.currentIndex()
        try:
            subprocess.call(["open", selected_option])
        except FileNotFoundError:
            print(f"File not found: {selected_option}")
        except subprocess.CalledProcessError:
            print(f"Error opening file: {selected_option}")


    def on_list_item_clicked(self, item):
        print("Clicked item:", item.text())
        self.setText(item.text())
        self.setFocus(Qt.OtherFocusReason)

    def on_text_changed(self, text):
        if not text:
            #self.popup_widget.hide()
            return
        suggestions, file_suggestions = self.get_suggestions(text)
        all_suggestions = suggestions + file_suggestions

        # Create a completer model with all suggestions
        completer_model = CompleterModel(all_suggestions)

        # Set the completer model in the completer
        self.completer.setModel(completer_model)


        self.suggestions_list.clear()
        # for suggestion in suggestions:
        #     item = QListWidgetItem()
        #     item.setText(suggestion)
        #     item.setSizeHint(QSize(0, 30))
        #     self.popup_list.addItem(item)
        # Add the suggestion items to the popup list
        for suggestion in suggestions:
            item = QListWidgetItem()
            item.setText(suggestion)
            item.setSizeHint(QSize(0, 30))
            self.suggestions_list.addItem(item)

    

        # Add the file suggestion items to the popup list
        self.file_suggestions_list.clear()
        for file_suggestion in file_suggestions:
            item = QListWidgetItem()
            item.setBackground(QColor(0, 0, 0, 20))
            item.setText(file_suggestion)
            item.setSizeHint(QSize(0, 30))
            self.file_suggestions_list.addItem(item)

    def get_suggestions(self, text):
        suggestions = []
        file_suggestions = []
        with self.driver.session() as session:
            result = session.run("MATCH (n:Keywords)-[r]-(m:Files) WHERE toLower(n.name) STARTS WITH toLower($text) RETURN DISTINCT n.name, r, m.name", text=text)
            for record in result:
                suggestion = record["m.name"]
                suggestions.append(suggestion)

            result = session.run("MATCH (n:Files) WHERE toLower(n.name) CONTAINS toLower($text) RETURN DISTINCT n.ctime", text=text)
            for record in result:
                suggestion = record["n.ctime"]
                file_suggestions.append(suggestion)

        return suggestions, file_suggestions
    








from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtGui import QWindow, QStyleHints
import sys

class MainWindow(QMainWindow):
    def __init__(self, rumps_app):
        super().__init__()
        self.rumps_app = rumps_app
        #self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # Set the presentation options to enable window level features

        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setAttribute(Qt.WA_TranslucentBackground)
        search_bar = SpotlightSearchBar()
        layout = QHBoxLayout()
        layout.addWidget(search_bar)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.mouse_pos = None
        self.start_size = None
        self.installEventFilter(self)
        # Get the dimensions of the desktop
        # center the window on the screen
        screen_geometry = QDesktopWidget().availableGeometry()
        self.setMinimumSize(screen_geometry.width() - 60, screen_geometry.height() - 20)
        x = int((screen_geometry.width() - self.width()))
        y = int((screen_geometry.height() - self.height()) )
        self.move(x, y)
        # Set the initial size of the window based on the search bar size
        self.resize(search_bar.sizeHint())
  

    def showEvent(self, event):
        super().showEvent(event)
        if sys.platform == 'darwin':
            #self.setSystemMenuOptions()
            pass

    def setSystemMenuOptions(self):
        window_handle = self.windowHandle()
        if window_handle is not None:
            options = window_handle.styleHints().setSystemMenu
            options |= window_handle.styleHints().setWindowSystemMenu
            options |= window_handle.styleHints().setWindowMinMaxButtons
            options |= window_handle.styleHints().setWindowCloseButton
            window_handle.setStyleHints(options)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            # close the widget when it loses focus
            self.close()
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # get the position of the mouse press event
            self.oldPosition = event.globalPos()
            event.accept()

    def focusOutEvent(self, event):
        # close the widget when it loses focus
        self.close()
        pass

  

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # calculate the new position of the window based on the mouse movement
            
            new_pos = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + new_pos.x(), self.y() + new_pos.y())
            self.oldPosition = event.globalPos()


    def on_list_item_clicked(self, item):
        print("Clicked item:", item.text())
        self.setText(item.text())
        self.setFocus(Qt.OtherFocusReason)
    

    def search(self):
        # get the text from the text input box
        search_text = self.sender().parent().children()[1].text()

        # do something with the search text, such as print it to the console
        print(f"Searching for {search_text}")


class App(rumps.App):
    def __init__(self):
        super().__init__('MyApp')
        self.dimensions = (40, 30)
        self.menu = []
        self.init_menu()

    def init_menu(self):
        self.menu = [
            rumps.MenuItem('Open App', callback=self.openApp)
        ]

    @rumps.clicked('Open App')
    def openApp(self, sender):
        # Implement your code to open the application here
        app = QApplication(sys.argv)
        window = MainWindow(self)
        window.setWindowOpacity(0.8)
        window.show()
        sys.exit(app.exec_())
        pass

    

if __name__ == '__main__':
    app = App()

    app.run()


