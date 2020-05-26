#!/usr/bin/env python3

import json
import os.path
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


INDEX_FN = 'index.json'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, path, parent=None):
        super().__init__(parent)

        self.path = path
        self.images = sorted(self._load_index(INDEX_FN))

        self._init_ui()

    def _load_index(self, filename):
        fn_index = os.path.join(self.path, filename)
        if os.path.isfile(fn_index):
            with open(fn_index) as f:
                return json.load(f)

        return [[fn, 0] for fn in os.listdir(self.path)
                if os.path.splitext(fn)[-1].lower() in {'.jpg', '.png'}]

    def _init_ui(self):
        self.files_list = QtWidgets.QListWidget()
        self.files_list.setFixedWidth(256)
        self.files_list.itemSelectionChanged.connect(self._select_file)

        for (filename, _) in self.images:
            self.files_list.addItem(filename)

        self.image_view = QtWidgets.QLabel()
        self.image_info = QtWidgets.QLabel()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.image_view)
        layout.addWidget(self.files_list)

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addWidget(self.image_info)
        layout2.addLayout(layout)

        window = QtWidgets.QWidget()
        window.setLayout(layout2)

        self.setCentralWidget(window)
        self.resize(640, 480)
        self.setWindowTitle("Viewer")

        for mark in range(6):
            QtWidgets.QShortcut(QtGui.QKeySequence(str(mark or 'Del')),
                                self, self._mark(mark))

        QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+S'), self,
                            lambda: self._save_marks(INDEX_FN))

        if self.images:
            self.files_list.setCurrentRow(0)

    def _select_file(self):
        image = self.images[self.files_list.currentRow()]
        filename = os.path.join(self.path, image[0])

        pixmap = QtGui.QPixmap(filename)

        view_size = self.image_view.size()
        if pixmap.width() > view_size.width() or pixmap.height() > view_size.height():
            pixmap = pixmap.scaled(view_size, QtCore.Qt.KeepAspectRatio)
        self.image_view.setPixmap(pixmap)

        self.image_info.setText(f'Filename: {image[0]}\nMark: {image[1]}')

    def _mark(self, mark):
        def handler():
            index = self.files_list.currentRow()
            if index >= 0:
                self.images[index][1] = mark
                self._select_file()

        return handler

    def _save_marks(self, filename):
        try:
            with open(os.path.join(self.path, filename), 'w') as f:
                json.dump(self.images, f)

            QtWidgets.QMessageBox.information(
                self, 'Information', 'Mark file saved',
                QtWidgets.QMessageBox.Ok)
        except Exception as e:
            QtWidgets.QMessageBox.error(
                self, 'Error', f'Error on save mark file:\n{e}',
                QtWidgets.QMessageBox.Ok)

    def closeEvent(self, event):
        self._save_marks(INDEX_FN)


def main():
    app = QtWidgets.QApplication(sys.argv)

    path = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        path = sys.argv[1]

    window = MainWindow(path)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
