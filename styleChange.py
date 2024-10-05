import dir_transitions as dt_tr 
from functools import partial

# Функция для смены css кнопок назад, вперед. 
# num: 1 - отключает ButtonBack, 2 - отключает ButtonFor, 3 - включает ButtonFor, 4 - включает ButtonBack, 5 - включаем ButtinUps, 6 - выключает ButtonUps
# 7-12 тоже самое что и 1-6, но без функции button.disconnect()

def style_pattern(pattern_num: int, url: str):
    if pattern_num == 1:
        css = '''QPushButton {
border-radius: 15px;
icon: url("''' + url + '''");
color: white;
border: None;
background-color: None;
}

QPushButton:hover {
background-color: None;

}

QPushButton:pressed {
background-color: None;
}
'''
        return css
    if pattern_num == 2:
        css = '''QQPushButton {
border-radius: 15px;
color: white;
border: None;
background-color: None;
}

QPushButton:hover {
background-color: None;
}

QPushButton:pressed {
background-color: None;
}
'''
        return css


def set_but_style(self, num: int):
    if num == 1:
        if self.butBackOn:
            self.butBackOn = False
            self.ui.pushButtonBack.clicked.disconnect()
            self.ui.pushButtonBack.setStyleSheet(style_pattern(1, "ui/icons/arrowBackOff.png"))
        else:
            return
    elif num == 2:
        if self.butForOn:
            self.butForOn = False
            self.ui.pushButtonFor.clicked.disconnect()
            self.ui.pushButtonFor.setStyleSheet(style_pattern(1, "ui/icons/arrowForOff.png"))
        else:
            return
    elif num == 3:
        if self.butForOn:
            return
        else:
            self.butForOn = True
            self.ui.pushButtonFor.clicked.connect(partial(dt_tr.forward, self=self))
            self.ui.pushButtonFor.setStyleSheet(style_pattern(2, None))
    elif num == 4:
        if self.butBackOn:
            return
        else:
            self.butBackOn = True
            self.ui.pushButtonBack.clicked.connect(partial(dt_tr.backward, self=self))
            self.ui.pushButtonBack.setStyleSheet(style_pattern(2, None))
    elif num == 5:
        if self.butUpsOn:
            return
        else:
            self.butUpsOn = True
            self.ui.pushButtonUps.clicked.connect(partial(dt_tr.up_directory, self=self))
            self.ui.pushButtonUps.setStyleSheet(style_pattern(2, None))
    elif num == 6:
        if self.butUpsOn:
            self.butUpsOn = False
            self.ui.pushButtonUps.clicked.disconnect()
            self.ui.pushButtonUps.setStyleSheet(style_pattern(1, "ui/icons/arrowUpsOff.png"))
        else:
            return
    if num == 7:
        self.ui.pushButtonBack.setStyleSheet(style_pattern(1, "ui/icons/arrowBackOff.png"))
    elif num == 8:
        self.ui.pushButtonFor.setStyleSheet(style_pattern(1, "ui/icons/arrowForOff.png"))
    elif num == 9:
        self.ui.pushButtonFor.setStyleSheet(style_pattern(2, None))
    elif num == 10:
        self.ui.pushButtonBack.setStyleSheet(style_pattern(2, None))
    elif num == 11:self.ui.pushButtonUps.setStyleSheet(style_pattern(2, None))
    elif num == 12:
        self.ui.pushButtonUps.setStyleSheet(style_pattern(1, "ui/icons/arrowUpsOff.png"))

def up_text_size(self):
    self.ui.setStyleSheet('''QWidget {
font-size: 24px;
color: while;
background-color:  rgb(38, 41, 42);
}

QWidget#MainWindow { 
border: none; 
background-color:  rgb(38, 41, 42);
}

QLineEdit {
padding-left: 10px;
border-radius: 10px;
color: white;
border: None;
background-color:  rgb(49, 52, 54);
}

QPushButton {
border-radius: 10px;
color: white;
border: None;
background-color: rgb(49, 52, 54);
}

QPushButton:hover {
background-color: #666;
}

QPushButton:pressed {
background-color: #888;
}

QTreeView {
color: white;
border: None;
}



QHeaderView::section { 
border-radius: 10px;
background-color:  rgb(49, 52, 54);
color: white;
border: None;
}
QWidget#MainWindow { 
border: None; 
}
''')
