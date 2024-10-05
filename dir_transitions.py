from distutils.dir_util import copy_tree
import styleChange as hm_SC
import os
from PySide2.QtCore import QDir
from PySide2.QtWidgets import *
from PySide2.QtGui import QCursor
import shutil
from functools import partial


def copy(self):
    self.copied_path = self.model.filePath(self.ui.treeView.currentIndex())
    self.copied_object = self.copied_path.split("/")[-1]
    print(self.copied_object)

def paste(self):
    if os.path.isdir(self.copied_path):
        copy_tree(self.copied_path, f"{self.model.filePath(self.ui.treeView.rootIndex())}\{self.copied_object}")
    else:  
        shutil.copy(self.copied_path, f"{self.model.filePath(self.ui.treeView.rootIndex())}\{self.copied_object}")


# Функция перехода вверх по ветке
def up_directory(self):
    path = self.history_array[self.in_path]
    if path != "":
        path = path[:len(path)-1]
        splited_path = path.split('/')
        splited_path = '\\'.join(splited_path)
        splited_path = splited_path.split('\\')
        splited_path.pop()
        path = '\\'.join(splited_path)
        if path != "" or path[:1] != ":":
            path += '\\'
        if path == "\\":
            path = ""
        change_path(self,path)
    else: pass


# Функция для перехода назад
def backward(self):
    if self.in_path > 0:
        path = self.history_array[self.in_path-1]
        self.in_path -= 1
        self.ui.treeView.setRootIndex(self.model.index(path))
        if self.in_path == 0:
            hm_SC.set_but_style(self,1)
            hm_SC.set_but_style(self,3)
        elif self.in_path < len(self.history_array)-1:
            hm_SC.set_but_style(self,3)
        if path == "":
            hm_SC.set_but_style(self, 6)
            self.ui.lineEdit.setText("Этот компьютер")
        else:
            path = change_slash(path)
            self.ui.lineEdit.setText(path)
            hm_SC.set_but_style(self, 5)
    else: pass

# Функция для перехода вперед
def forward(self):
    if self.in_path < len(self.history_array)-1:
        path = self.history_array[self.in_path+1]
        self.in_path += 1
        self.ui.treeView.setRootIndex(self.model.index(path))
        if self.in_path == len(self.history_array)-1:
            hm_SC.set_but_style(self,2)
            hm_SC.set_but_style(self,4)
        elif self.in_path > 0:
            hm_SC.set_but_style(self,4)
        if path == "":
            hm_SC.set_but_style(self, 6)
            self.ui.lineEdit.setText("Этот компьютер")
        else:
            path = change_slash(path)
            self.ui.lineEdit.setText(path)
            hm_SC.set_but_style(self, 5)
    else:
        pass

# Функция для перехода в котолог из lineEdit
def change_path_lineEdit(self):
    # если юзер находится не в последнем каталоге в массиве истории переходов, то удаляем последующие пути
    if self.in_path < len(self.history_array) - 1:
        i = self.in_path + 1
        while i < len(self.history_array):
            self.history_array.pop(i)
    else:
        pass

    # Изменяем стиль кнопок
    hm_SC.set_but_style(self,2)
    hm_SC.set_but_style(self,4)

    path = self.ui.lineEdit.text()

    # удаляем первый путь в массиве истории переходов если в массиве больше 10 элементов
    if len(self.history_array) > 10:
        self.history_array.pop(0)

    self.history_array.append(path)
    self.in_path = len(self.history_array) - 1

    if os.path.isdir(path) == True:
        self.ui.treeView.setRootIndex(self.model.index(path))
    else:
        pass
    
    if path == "":
        hm_SC.set_but_style(self,6)
    else:
        hm_SC.set_but_style(self,5)


# Создаем функцию для перехода в каталог
def change_path(self, path: str):
    # если юзер находится не в последнем каталоге в массиве истории переходов, то удаляем последующие пути
    if self.in_path < len(self.history_array) - 1:
        i = self.in_path + 1
        while i < len(self.history_array):
            self.history_array.pop(i)
    else:
        pass

    # Изменяем стиль кнопок
    hm_SC.set_but_style(self,2)
    hm_SC.set_but_style(self,4)

    # удаляем первый путь в массиве истории переходов если в массиве больше 10 элементов
    if len(self.history_array) > 10:
        self.history_array.pop(0)

    self.history_array.append(path)
    self.in_path = len(self.history_array) - 1

    self.ui.treeView.setRootIndex(self.model.index(path))
    if path == "":
        self.ui.lineEdit.setText("Этот компьютер")
    else:
        path = change_slash(path)
        self.ui.lineEdit.setText(path)
    
    if path == "":
        hm_SC.set_but_style(self,6)
    else:
        hm_SC.set_but_style(self,5)

# Функция в которой накидывает модель файловой системы на treeView
def fill_window(self):
    self.model = QFileSystemModel()
    self.model.setRootPath(QDir.rootPath())
    self.ui.treeView.setModel(self.model)
    self.ui.treeView.setSortingEnabled(True)
    self.ui.lineEdit.setText("Этот компьютер")
    self.ui.treeView.setColumnWidth(0, 250)

# Создаем контекстное меню при клике правой кнопкой мыши
def context_menu(self):
    menu = QMenu()
    open = menu.addAction("Открыть")
    open.triggered.connect(partial(open_file, self=self))
    rm = menu.addAction("Удалить")
    rm.triggered.connect(partial(remove_file_or_dir, self=self))
    create_f = menu.addAction("Создать файл")
    create_f.triggered.connect(partial(create_file, self=self))
    create_d = menu.addAction("Создать папку")
    create_d.triggered.connect(partial(create_dir, self=self))
    cursor = QCursor()
    menu.exec_(cursor.pos())

# Функция открытия файла
def open_file(self):
    index = self.ui.treeView.currentIndex()
    file_path = self.model.filePath(index)
    if os.path.isdir(file_path) == False:
        os.startfile(file_path)
    else:
        change_path(self,file_path)

# Функция удаления файла или каталога
def remove_file_or_dir(self):
    index = self.ui.treeView.currentIndex()
    file_path = self.model.filePath(index)
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        os.remove(file_path)

# Функция для вызова диалогового окна с текстом
def dialog_window(self, title: str, text: str):
    dlg = QDialog(self)
    dlg.setWindowTitle(title)
    label = QLabel(text)
    layout = QVBoxLayout()
    layout.addWidget(label)
    dlg.setLayout(layout)

    dlg.exec_()

# Функция создания файла
def create_file(self):
    index = self.ui.treeView.rootIndex()
    file_path = self.model.filePath(index)
    file_name, _ = QInputDialog.getText(
        self, "Создание нового файла", "Введите название файла с расширением:")
    if file_name:
        open(file_path+"/"+file_name, 'w').close()
    elif _:
        dialog_window(self, "Отмена создания файла",
                            "Не указано название файла.")
    else:
        pass

# Функция создания каталога
def create_dir(self):
    index = self.ui.treeView.rootIndex()
    dir_path = self.model.filePath(index)
    dir_name, _ = QInputDialog.getText(
        self, "Создание новой папки", "Введите название папки:")
    if dir_name:
        os.mkdir(dir_path+"/"+dir_name)
    elif _:
        dialog_window(self, "Отмена создания папки",
                            "Не указано название папки.")
    else:
        pass

def change_slash(path: str):
    splited_path = path.split('/')
    path = '\\'.join(splited_path)
    return path