import sys
import getpass  # Импортируем модуль для получения имени пользователя
# импортируем самописные модули
import rc_design
import styleChange as hm_SC
import dir_transitions as dt_tr   
# Импортнул функцию для исправления ошибки при обаботке кнопки в цикле
from functools import partial
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt, QEvent
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QKeySequence
import win32api  # библиотека для работы с window api

class MainClass(QWidget):
    def __init__(self, width: int, height: int, parent=None):
        QWidget.__init__(self, parent)

        # Загружаем дизайн из файла
        designer_file = QFile("./ui/design.ui")
        designer_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(designer_file, self)
        designer_file.close()

        # Устанавливаем размер окна
        self.width = 1000
        self.height = 600
        self.setMinimumSize(1000, 600)

        # Меняю размер шрифта через css если экран больше FHD
        if width > 1080:
            hm_SC.up_text_size(self)
        # Растягиваем дизайн по сетке
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui, stretch=3)
        self.setLayout(grid_layout)

        # Устанавливаем иконку приложения и заголовок
        self.setWindowIcon(QIcon("ui/icons/icon.ico"))
        self.setWindowTitle("File explorer")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Получаем список дисков с помощью windows api
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]

        # Создаем переменные для хранения пути к копированному объекту
        self.copied_path = ""
        self.copied_object = ""

        # Проходимся по списку дисков и добавляем кнопки для них
        for drive in drives:
            if drive == 'C:\\':
                continue
            else:
                pb = QPushButton(
                    f"{win32api.GetVolumeInformation(drive)[0]} ({drive})")
                pb.setIcon(QIcon(f"ui/icons/disk.ico"))
                pb.clicked.connect(partial(dt_tr.change_path, path=drive, self=self))
                pb.setStyleSheet('QPushButton { text-align: left; }')
                pb.setMinimumSize(150, 25)
                self.ui.verticalLayout_3.addWidget(pb)

        self.ui.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(lambda: dt_tr.context_menu(self))
        dt_tr.fill_window(self)

        # Создаем массив с сылками каталогов и вешаем обработчик клика на боковые кнопки
        self.paths = ["",
                      f"C:\\Users\\{getpass.getuser()}\\Videos",
                      f"C:\\Users\\{getpass.getuser()}\\Documents",
                      f"C:\\Users\\{getpass.getuser()}\\Downloads",
                      f"C:\\Users\\{getpass.getuser()}\\Pictures",
                      f"C:\\Users\\{getpass.getuser()}\\Music",
                      f"C:\\Users\\{getpass.getuser()}\\Desktop", 
                      "C:\\"]
        self.ui.pushButton_2.clicked.connect(
            lambda: dt_tr.change_path(self,self.paths[0]))
        self.ui.pushButton_8.clicked.connect(
            lambda: dt_tr.change_path(self,self.paths[1]))
        self.ui.pushButton_7.clicked.connect(
            lambda: dt_tr.change_path(self,self.paths[2]))
        self.ui.pushButton_6.clicked.connect(
            lambda: dt_tr.change_path(self,self.paths[3]))
        self.ui.pushButton_5.clicked.connect(
            lambda: dt_tr.change_path(self,self.paths[4]))
        self.ui.pushButton_4.clicked.connect(
            lambda: dt_tr.change_path(self,self.paths[5]))
        self.ui.pushButton_3.clicked.connect(
            lambda: dt_tr.change_path(self,self.paths[6]))
        self.ui.pushButton.clicked.connect(
            lambda: dt_tr.change_path(self,self.paths[7]))

        # Обрабатываем нажатие enter в lineEdit
        self.ui.lineEdit.editingFinished.connect(partial(dt_tr.change_path_lineEdit, self=self))

        # Обрабатываем дабл клик по файлам и каталогам
        self.ui.treeView.doubleClicked.connect(lambda: dt_tr.open_file(self))

        # Изменяем стиль кнопок управления на выключеные
        hm_SC.set_but_style(self, 7)
        hm_SC.set_but_style(self, 8)
        hm_SC.set_but_style(self, 12)

        # Создаем массив для истории переходов по каталогам и переменную с индексом массива истории путя в котором юзер сейчас находится
        self.history_array = ['']
        self.in_path = 0

        # Создаем булевые переменые для обработки понимания включены ли кнопоки
        self.butBackOn = False
        self.butForOn = False
        self.butUpsOn = False

        # подключение управления с клавиатуры и мышки
        QShortcut(QKeySequence("esc"), self.ui.pushButtonUps, lambda: dt_tr.up_directory(self))
        QShortcut(QKeySequence("delete"), self.ui.pushButtonUps, lambda: dt_tr.remove_file_or_dir(self))
        QShortcut(QKeySequence("ctrl+c"), self.ui.treeView, lambda: dt_tr.copy(self) )
        QShortcut(QKeySequence("ctrl+v"), self.ui.treeView, lambda: dt_tr.paste(self) )

        for child in self.findChildren(QWidget):
            child.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                return False
            elif event.button() == Qt.RightButton:
                return False
            elif event.button() == Qt.MiddleButton:
                return False
            elif event.button() == Qt.XButton1:
                dt_tr.backward(self)
                return True
            elif event.button() == Qt.XButton2:
                dt_tr.forward(self)
                return True 
        return False

    
# инизиализация и запуск приложения
def start_program():
    app = QApplication(sys.argv)
    screen_rect = app.primaryScreen().availableGeometry()
    window = MainClass(screen_rect.width(), screen_rect.height())
    window.show()
    sys.exit(app.exec_())


# Проверяем запускаем ли мы исполняемый файл или нет
if __name__ == '__main__':
    start_program()
