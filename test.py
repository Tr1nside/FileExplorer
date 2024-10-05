print('''QPushButton {
icon: url("ui/icons/arrowBackOff.png");
color: white;
border: none;
background-color: none;
}

QPushButton:hover {
background-color: none;

}

QPushButton:pressed {
background-color: none;
}
''')
a = '''QPushButton {
icon: '''
b =''' ;
color: white;
border: none;
background-color: none;
}

QPushButton:hover {
background-color: none;

}

QPushButton:pressed {
background-color: none;
}
'''
c = 'url("ui/icons/arrowBackOff.png")'


print(a+c+b)