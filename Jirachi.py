import os
import sys
import random
import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import pygame
from srcs.Array import cartas

class Jirachi(QWidget):
    def __init__(self):
        super().__init__()

        # Inicialização da interface gráfica
        self.initUI()

        # Verifica se o programa já foi executado hoje
        self.check_execution_date()
        
        # Adiciona ícone ao programa
        icon = QIcon("srcs/Jirachi.ico")
        self.setWindowIcon(icon)

        # Define as cartas iniciais
        self.initialize_cards()

        # Inicialização do mixer do pygame
        pygame.mixer.init()
        # Carrega o arquivo de áudio da trilha sonora
        trilha_sonora = pygame.mixer.music.load("srcs/OST.mp3")
        # Reproduz a trilha sonora em loop
        pygame.mixer.music.play(-1)

        # Carrega o arquivo de áudio do efeito sonoro
        self.sound_effect = pygame.mixer.Sound("srcs/cardflip.mp3")
        

    def initUI(self):
        # Configurações da janela principal
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Jirachi')
        self.setFixedSize(800, 600)

        # Configura o fundo como um GIF
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 800, 600)
        self.background_label.setScaledContents(True)
        self.background_label.setMovie(QMovie("srcs/background.gif"))
        self.background_label.movie().start()

        # Configuração das cartas
        card_width = 165
        spacing = (800 - (3 * card_width)) / 4  # Espaço entre as cartas
        self.card_labels = []
        for i in range(3):
            card_label = QLabel(self)
            card_label.setGeometry(int(spacing + i * (card_width + spacing)), 70, card_width, 284)
            card_label.setScaledContents(True)
            card_label.setPixmap(QPixmap("srcs/cartas/back.png"))
            card_label.mousePressEvent = lambda event, index=i: self.card_clicked(index)
            self.card_labels.append(card_label)

        # Configuração do texto da carta selecionada
        # Nome da Carta
        self.card_name_label = QLabel(self)
        self.card_name_label.setGeometry(300, 5, 200, 80)
        self.card_name_label.setAlignment(Qt.AlignCenter)
        self.card_name_label.setStyleSheet("color: white;")
        self.card_name_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        # Significado da carta
        self.card_meaning_label = QLabel(self)
        self.card_meaning_label.setGeometry(100, 370, 600, 200) 
        self.card_meaning_label.setAlignment(Qt.AlignCenter)
        self.card_meaning_label.setStyleSheet("color: white;")
        self.card_meaning_label.setWordWrap(True)
        self.card_meaning_label.setFont(QFont("Calibri (corpo)", 12))

    def check_execution_date(self):
        # Verifica se o programa já foi executado hoje
        today = datetime.date.today().strftime("%Y-%m-%d")
        file_path = "srcs/last_execution.txt"

        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write(today)
            print("Arquivo criado: last_execution.txt")
        else:
            with open(file_path, "r") as file:
                last_execution_date = file.read()

            if last_execution_date == today:
                print("O programa já foi executado hoje. Tente novamente amanhã.")
                sys.exit()

        with open(file_path, "w") as file:
            file.write(today)

    def initialize_cards(self):
        # Escolhe aleatoriamente três cartas do array "cartas"
        selected_cards = random.sample(cartas, 3)

        # Inicializa as cartas viradas para baixo
        self.selected_card = None
        for i, label in enumerate(self.card_labels):
            card = selected_cards[i]
            label.setPixmap(QPixmap("srcs/cartas/back.png"))
            label.card_info = card

    def card_clicked(self, card_index):
        # Lida com o evento de clique em uma carta
        if self.selected_card is None:
            # Reproduz o efeito sonoro
            self.sound_effect.play()
            label = self.card_labels[card_index]
            card = label.card_info
            label.setPixmap(QPixmap(card["imagem"]))
            self.card_name_label.setText(card["nome"])
            self.card_meaning_label.setText(card["significado"])
            self.selected_card = card


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tarot_app = Jirachi()
    tarot_app.show()
    sys.exit(app.exec_())
