import sys
import os
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QFileDialog


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setWindowIcon(QIcon("icon.png"))  # Replace "icon.png" with your own icon file
        self.setGeometry(200, 200, 500, 300)

        self.playlist = []
        self.current_index = 0
        self.player = QMediaPlayer()
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)

        self.setup_ui()

    def setup_ui(self):
        vbox = QVBoxLayout()

        self.label_file_name = QLabel("File Name")
        self.label_duration = QLabel("--:-- / --:--")

        hbox_slider = QHBoxLayout()
        self.slider_position = QSlider(Qt.Horizontal)
        self.slider_position.setTracking(False)
        self.slider_position.sliderMoved.connect(self.set_position)
        hbox_slider.addWidget(self.slider_position)

        hbox_controls = QHBoxLayout()
        button_open = QPushButton("Open")
        button_open.clicked.connect(self.open_file)
        button_play = QPushButton("Play")
        button_play.clicked.connect(self.play)
        button_pause = QPushButton("Pause")
        button_pause.clicked.connect(self.pause)
        button_stop = QPushButton("Stop")
        button_stop.clicked.connect(self.stop)
        hbox_controls.addWidget(button_open)
        hbox_controls.addWidget(button_play)
        hbox_controls.addWidget(button_pause)
        hbox_controls.addWidget(button_stop)

        vbox.addWidget(self.label_file_name)
        vbox.addWidget(self.label_duration)
        vbox.addLayout(hbox_slider)
        vbox.addLayout(hbox_controls)

        self.setLayout(vbox)

    def open_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Audio Files (*.mp3)")
        if file_dialog.exec_():
            files = file_dialog.selectedFiles()
            for file in files:
                self.playlist.append(file)
            if not self.player.state() == QMediaPlayer.PlayingState:
                self.play()

    def play(self):
        if self.current_index < len(self.playlist):
            file_path = self.playlist[self.current_index]
            self.label_file_name.setText(os.path.basename(file_path))
            media_content = QMediaContent(QUrl.fromLocalFile(file_path))
            self.player.setMedia(media_content)
            self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def update_duration(self, duration):
        minutes = int(duration / 60000)
        seconds = int((duration % 60000) / 1000)
        self.label_duration.setText(f"--:-- / {minutes:02d}:{seconds:02d}")

    def update_position(self, position):
        minutes = int(position / 60000)
        seconds = int((position % 60000) / 1000)
        self.label_duration.setText(f"{minutes:02d}:{seconds:02d} / {self.label_duration.text().split(' / ')[1]}")
        self.slider_position.setValue(position)

    def set_position(self, position):
        self.player.setPosition(position)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
