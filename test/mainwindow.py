"""
pyglpainter - Minimalistic, modern OpenGL drawing for technical applications
Copyright (C) 2015 Michael Franzl

This file is part of pyglpainter.

pyglpainter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyglpainter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyglpainter. If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QLayout, QHBoxLayout, QGridLayout
from pyglpainter.classes.painterwidget import PainterWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.centralWidget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.gridLayout1 = QGridLayout()
        self.gridLayout1.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout.addLayout(self.gridLayout1)
        self.setCentralWidget(self.centralWidget)

        self.painter = PainterWidget(self)
        self.gridLayout1.addWidget(self.painter)
