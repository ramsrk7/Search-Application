from PyQt5.QtWidgets import QApplication, QWidget, QListView, QLineEdit, QHBoxLayout, QVBoxLayout, QToolBar, QAction, QCompleter
from PyQt5.QtCore import Qt, QPoint, QSize, QEvent
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QApplication,QTextEdit, QLineEdit, QCompleter, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from neo4j import GraphDatabase
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QCompleter, QLabel, QVBoxLayout, QListWidget, QListWidgetItem, QWidget, QLineEdit, QApplication, QMainWindow, QSpacerItem, QSizePolicy, QComboBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
import subprocess
import rumps
from spotlightSearch import search_files_with_content

class CompleterModel(QAbstractListModel):
    def __init__(self, suggestions):
        super().__init__()
        self.suggestions = suggestions
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.suggestions)
    
    def data(self, index, role=Qt.DisplayRole):
        print(index)
        if role == Qt.DisplayRole:
            
            return self.modify_string(self.suggestions[index.row()])
            
        return None
    def modify_string(self, string):
        # Manipulate the string for display purposes
        # For example, you can add ellipsis (...) to the end
        try:
            modified_string = string.split("/")[-1]
        except:
            modified_string = string
        return modified_string

class SpotlightSearchBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Tool) 
        font = QFont("Helvetica Neue", 20)
        self.setFixedHeight(800)
        self.setFixedWidth(600)

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Enter search query...")
        self.input_text.setFont(font)
        self.input_text.setFixedHeight(50)
        self.input_text.selectAll()

        self.suggestions_list = QListView()
        #self.suggestions_list.setFixedHeight(150)
        self.suggestions_list.setAlternatingRowColors(True)
        self.suggestions_list.setFixedHeight(0)
        self.suggestions_list.setStyleSheet("""
            QListView {
                /* Add your other styles for QListView here */
            }
            QListView::scrollbar {
                background-color: #F5F5F5;  /* Set the background color */
                width: 10px;  /* Set the width of the scrollbar */
            }
            QListView::scrollbar:vertical {
                border-radius: 5px;  /* Set the border radius */
            }
            QListView::scrollbar::handle:vertical {
                background-color: #CCCCCC;  /* Set the background color of the handle */
                border-radius: 5px;  /* Set the border radius of the handle */
            }
            QListView::scrollbar::handle:vertical:hover {
                background-color: #AAAAAA;  /* Set the background color of the handle when hovered */
            }
            QListView::scrollbar::add-line:vertical,
            QListView::scrollbar::sub-line:vertical {
                background: none;  /* Remove the background of the add/subtract buttons */
            }
        """)
        self.suggestions_label = QLabel("Keyword Search")
        self.suggestions_label.setVisible(False)
        self.suggestions_label.setMouseTracking(True)
        palette = self.input_text.palette()
        background_color = palette.color(QPalette.Base)
        radius = 10 
        self.suggestions_label.setStyleSheet(f"background-color: {background_color.name()}; padding: 5px; font-weight: bold; border-top-left-radius: {radius}px; border-top-right-radius: {radius}px;")
        self.file_suggestions_list = QListView()
        #self.file_suggestions_list.setFixedHeight(150)
        self.file_suggestions_list.setAlternatingRowColors(True)
        self.file_suggestions_list.setFixedHeight(0)
        self.file_suggestions_list.setStyleSheet("""
            QListView {
                /* Add your other styles for QListView here */
            }
            QListView::scrollbar {
                background-color: #F5F5F5;  /* Set the background color */
                width: 10px;  /* Set the width of the scrollbar */
            }
            QListView::scrollbar:vertical {
                border-radius: 5px;  /* Set the border radius */
            }
            QListView::scrollbar::handle:vertical {
                background-color: #CCCCCC;  /* Set the background color of the handle */
                border-radius: 5px;  /* Set the border radius of the handle */
            }
            QListView::scrollbar::handle:vertical:hover {
                background-color: #AAAAAA;  /* Set the background color of the handle when hovered */
            }
            QListView::scrollbar::add-line:vertical,
            QListView::scrollbar::sub-line:vertical {
                background: none;  /* Remove the background of the add/subtract buttons */
            }
        """)
        self.file_suggestions_label = QLabel("Filename Search")
        self.file_suggestions_label.setVisible(False)
        self.file_suggestions_label.setMouseTracking(True)
        palette = self.input_text.palette()
        background_color = palette.color(QPalette.Base)
        self.file_suggestions_label.setStyleSheet(f"background-color: {background_color.name()}; padding: 5px; font-weight: bold; border-top-left-radius: {radius}px; border-top-right-radius: {radius}px;")

        self.entered_text_box = QTextEdit()
        self.entered_text_box.setReadOnly(True)
        self.entered_text_box.setLineWrapMode(QTextEdit.WidgetWidth)
        self.entered_text_box.setFixedHeight(0)
        self.entered_text_box_label = QLabel("Search Assistant")
        self.entered_text_box_label.setVisible(False)
        palette = self.input_text.palette()
        background_color = palette.color(QPalette.Base)
        self.entered_text_box_label.setStyleSheet(f"background-color: {background_color.name()}; padding: 5px; font-weight: bold; border-top-left-radius: {radius}px; border-top-right-radius: {radius}px;")



        self.container_widget = QWidget()  # Use QFrame as the container widget

        # Apply rounded corners to the container widget
        radius = 10  # Adjust the radius as desired
        self.container_widget.setStyleSheet(f"QFrame {{ border-radius: {radius}px; }}")

        container_layout = QVBoxLayout(self.container_widget)
        container_layout.addWidget(self.input_text)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addSpacing(5)
        container_layout.addWidget(self.entered_text_box_label)
        container_layout.addWidget(self.entered_text_box)
        container_layout.addSpacing(5)
        container_layout.addWidget(self.suggestions_label)
        container_layout.addWidget(self.suggestions_list)
        container_layout.addSpacing(5)
        container_layout.addWidget(self.file_suggestions_label)
        container_layout.addWidget(self.file_suggestions_list)
        container_layout.addStretch()

        # Set background color of container widget
        palette = self.input_text.palette()
        background_color = palette.color(QPalette.Base)
        self.container_widget.setStyleSheet(f"background-color: {background_color.name()};")

       

        #self.container_widget.setFixedHeight(self.input_text.height()+5)

        

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.container_widget)

        self.setRoundedCorners()

        # Initialize Neo4j driver
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "neo4jneo4j"
        try:
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
        except:
            print("Can't connect to DB.")

        # Connect the textChanged signal to the on_text_changed slot
        self.input_text.textChanged.connect(self.on_text_changed)
        # Connect the textChanged signal to the on_text_changed slot
        self.input_text.returnPressed.connect(self.on_text_entered)


    def setRoundedCorners(self):
        radius = 10  # Adjust the radius as desired

        # Apply rounded corners to the input text
        self.input_text.setStyleSheet(f"QLineEdit {{ border-radius: {radius}px; }}")
        # Remove focus highlight
        self.input_text.setAttribute(Qt.WA_MacShowFocusRect, False)

        # Apply rounded corners to the list views
        self.suggestions_list.setStyleSheet(f"QListView {{ border-radius: {radius}px; }}; border-bottom-left-radius: {radius}px; border-bottom-right-radius: {radius}px;")
        self.file_suggestions_list.setStyleSheet(f"QListView {{ border-radius: {radius}px; }}; border-bottom-left-radius: {radius}px; border-bottom-right-radius: {radius}px;")

        # Apply rounded corners to the entered text box
        self.entered_text_box.setStyleSheet(f"QTextEdit {{ border-radius: {radius}px; }}")
        self.container_widget.setStyleSheet(f"QTextEdit {{ border-radius: {radius}px; }}")
        # Apply rounded corners to the list views and set hover color
        list_style = """
            QListView {{
                border-radius: {radius}px;
            }}
            QListView::item:hover {{
                background-color: #DDDDDD;
            }}
            QListView::item:selected {{
                background-color: #AAAAAA;
            }}
            QListView::scrollbar {{
                background-color: #F5F5F5;
                width: 10px;
            }}
            QListView::scrollbar:vertical {{
                border-radius: 5px;
            }}
            QListView::scrollbar::handle:vertical {{
                background-color: #CCCCCC;
                border-radius: 5px;
            }}
            QListView::scrollbar::handle:vertical:hover {{
                background-color: #AAAAAA;
            }}
            QListView::scrollbar::add-line:vertical,
            QListView::scrollbar::sub-line:vertical {{
                background: none;
            }}
        """.format(radius=radius)

        self.suggestions_list.setStyleSheet(list_style)
        self.file_suggestions_list.setStyleSheet(list_style)

    def adjust_list_height(self, list_view, model):
        item_height = 20
        max_items = 5
        if model.rowCount() < 5:
            total_height = model.rowCount() * item_height
        else:
            total_height = max_items * item_height

        list_view.setFixedHeight(total_height)

    def on_list_item_clicked(self, index, list_view):
        model = list_view.model()
        if model is not None:
            item = model.suggestions[index.row()]
            print("Clicked item:", item)
            # self.input_text.setText(item)
            try:
                subprocess.call(["open", item])
            except FileNotFoundError:
                print(f"File not found: {item}")
            except subprocess.CalledProcessError:
                print(f"Error opening file: {item}")
            # self.input_text.setFocus(Qt.OtherFocusReason)
    
    def on_text_entered(self):
        text = self.input_text.text()
        text = "YOU: " + text
        self.input_text.clear()

        if text:
            self.entered_text_box_label.setVisible(True)
            current_text = self.entered_text_box.toPlainText()
            if current_text:
                self.entered_text_box.setPlainText(current_text + "\n" + text)
            else:
                self.entered_text_box.setPlainText(text)

            # Adjust the size of the QTextEdit widget based on the height of the text
            document = self.entered_text_box.document()
            document.adjustSize()
            height = int(document.size().height())
            self.entered_text_box.setFixedHeight(height+15)

            self.entered_text_box.append("BOT: OK")


    def on_text_changed(self, text):
        if not text:
            self.suggestions_list.setModel(None)
            self.file_suggestions_list.setModel(None)
            self.suggestions_list.setFixedHeight(0)
            self.file_suggestions_list.setFixedHeight(0)
            self.suggestions_label.setVisible(False)
            self.file_suggestions_label.setVisible(False)
            return

        suggestions, file_suggestions = self.get_suggestions(text)
        all_suggestions = suggestions + file_suggestions

        if suggestions:
            suggestions_model = CompleterModel(suggestions)
            self.suggestions_list.setModel(suggestions_model)
            self.adjust_list_height(self.suggestions_list, suggestions_model)
            self.suggestions_label.setVisible(True)
        else:
            self.suggestions_list.setModel(None)
            self.suggestions_list.setFixedHeight(0)
            self.suggestions_label.setVisible(False)

        if file_suggestions:
            file_suggestions_model = CompleterModel(file_suggestions)
            self.file_suggestions_list.setModel(file_suggestions_model)
            self.adjust_list_height(self.file_suggestions_list, file_suggestions_model)
            self.file_suggestions_label.setVisible(True)
        else:
            self.file_suggestions_list.setModel(None)
            self.file_suggestions_list.setFixedHeight(0)
            self.file_suggestions_label.setVisible(False)

        self.suggestions_list.clicked.connect(lambda index: self.on_list_item_clicked(index, self.suggestions_list))
        self.file_suggestions_list.clicked.connect(lambda index: self.on_list_item_clicked(index, self.file_suggestions_list))

        # Set the text in the QLineEdit widget
        self.input_text.setText(text)


    def get_suggestions(self, text):
        suggestions = []
        file_suggestions = []
        with self.driver.session() as session:
            result = session.run("MATCH (n:Keywords)-[r]-(m:Files) WHERE toLower(n.name) STARTS WITH toLower($text) RETURN DISTINCT m.name", text=text)
            for record in result:
                suggestion = record["m.name"]
                suggestions.append(suggestion)

            result = session.run("MATCH (n:Files) WHERE toLower(n.name) CONTAINS toLower($text) RETURN DISTINCT n.name", text=text)
            for record in result:
                suggestion = record["n.name"]
                file_suggestions.append(suggestion)

        suggestion_spotlight = search_files_with_content(text,path="/Users/ram/Desktop/Final-Project/Sample_Files")
        for s in suggestion_spotlight:
            if s not in suggestions:
                suggestions.append(s)
        

        return suggestions, file_suggestions
    


from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtGui import QWindow, QStyleHints
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")

        #self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # Set the presentation options to enable window level features
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.X11BypassWindowManagerHint
            | Qt.WindowTitleHint  # Disable the title bar
        )

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
        search_bar = self.centralWidget().layout().itemAt(0).widget()
        search_bar.input_text.setFocus()

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
        #self.setFocus(Qt.OtherFocusReason)
    

    def search(self):
        # get the text from the text input box
        search_text = self.sender().parent().children()[1].text()

        # do something with the search text, such as print it to the console
        print(f"Searching for {search_text}")


class App(rumps.App):
    def __init__(self):
        super().__init__('Search')
        self.dimensions = (40, 30)
        self.menu = []
        self.init_menu()

    def init_menu(self):
        self.menu = [
            rumps.MenuItem('Open', callback=self.openApp)
        ]

    @rumps.clicked('Open')
    def openApp(self, sender):
        # Implement your code to open the application here
        app = QApplication(sys.argv)
        window = MainWindow()
        window.setWindowOpacity(0.8)
        window.show()
        sys.exit(app.exec_())
        pass

    

if __name__ == '__main__':
    app = App()

    app.run()


