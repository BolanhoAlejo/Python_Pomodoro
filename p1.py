import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from hilo_1s import Hilo1s

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tiempo_trabajo = 15
        self.tiempo_descanso = 5
        self.segundos = 0
        self.vueltas = 0
        self.descanso = False
        self.init_ui()
        self.init_style()
        self.init_layout()
        self.init_threads()

    def init_ui(self):
        self.label_segundos = QLabel('0', self)
        self.label_vueltas_titulo = QLabel('Vueltas:', self)
        self.label_vueltas = QLabel('0', self)
        self.label_estado = QLabel('Esperando...', self)
        self.button_comenzar = QPushButton('Comenzar', self)
        self.button_pausa = QPushButton('Pausa', self)
        self.button_reset = QPushButton('Reset', self)
        self.button_comenzar.clicked.connect(self.comenzar_reloj)
        self.button_pausa.clicked.connect(self.pausar_reloj)
        self.button_reset.clicked.connect(self.reset_reloj)

    def init_layout(self):
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.label_segundos)

        layout_vuelta = QHBoxLayout()
        layout_vuelta.addWidget(self.label_vueltas_titulo)
        layout_vuelta.addWidget(self.label_vueltas)
        layout_principal.addLayout(layout_vuelta)

        layout_estado = QHBoxLayout()
        layout_estado.addWidget(self.label_estado)
        layout_principal.addLayout(layout_estado)

        layout_button = QHBoxLayout()
        layout_button.addWidget(self.button_comenzar)
        layout_button.addWidget(self.button_pausa)
        layout_button.addWidget(self.button_reset)
        layout_principal.addLayout(layout_button)

        widget = QWidget()
        widget.setLayout(layout_principal)
        self.setCentralWidget(widget)

    def init_style(self):
        self.setStyleSheet("""
           QWidget {
             background-color: #333333;
             color: white;
             font-family: 'Verdana';
             font-size: 14px;
           }
        """)
        self.seconts_run_style = """
           font-size: 80px;
           font-weight: bold;
           qproperty-alignment: AlignCenter;
           color: #32CD32;
           background-color:transparent;
        """
        self.seconts_pause_style = """
           font-size: 80px;
           font-weight: bold;
           qproperty-alignment: AlignCenter;
           color: #FF4500;
           background-color:transparent;
        """
        self.seconts_descanso_style = """
           font-size: 80px;
           font-weight: bold;
           qproperty-alignment: AlignCenter;
           color: #FFC107;
           background-color:transparent;
        """
        button_style = """
          QPushButton {
            background-color: #555555;
            border: 2px solid #777777;
            border-radius: 10px;
            padding: 10px;
            color: white;
            font-weight: bold;
          }
          QPushButton:hover {
            background-color: #777777;
            border-color: white;
          }
        """
        text_style = """
           font-size: 18px;
           font-weight: bold;
           qproperty-alignment: AlignLeft;
           color: white;
        """
        contador_style = """
           color: #FFFFFF;
           font-family: 'Verdana';
           font-size: 24px;
           font-weight: bold;
           qproperty-alignment: AlignRight;
           padding-left: 5px;
        """

        self.label_segundos.setStyleSheet(self.seconts_run_style)
        self.button_comenzar.setStyleSheet(button_style)
        self.button_pausa.setStyleSheet(button_style)
        self.button_reset.setStyleSheet(button_style)
        self.label_vueltas_titulo.setStyleSheet(text_style)
        self.label_vueltas.setStyleSheet(contador_style)
        self.label_estado.setStyleSheet(text_style)
    def init_threads(self):
        self.hilo_1s = Hilo1s()
        self.hilo_1s.beep.connect(self.beep_1s)

    def actualizar_segundos(self):
        self.label_segundos.setText(f'{self.segundos}')

    def sumar_segundo(self):
        self.segundos += 1
        if self.descanso:
          limite = self.tiempo_descanso
        else:
          limite = self.tiempo_trabajo
        if self.segundos > limite:
          self.cambiar_fase()
        self.actualizar_segundos()

    def cambiar_fase(self):
        self.segundos = 0
        self.descanso = not self.descanso
        if self.descanso:
          self.vueltas += 1
          self.label_vueltas.setText(str(self.vueltas))
          self.label_estado.setText('Descansando.')
          self.label_segundos.setStyleSheet(self.seconts_descanso_style)
        else:
          self.label_estado.setText('Trabajando.')
          self.label_segundos.setStyleSheet(self.seconts_run_style)

    def comenzar_reloj(self):
        if not self.hilo_1s.isRunning():
          self.hilo_1s.start()
        if self.descanso:
          self.label_estado.setText('Descansando.')
          self.label_segundos.setStyleSheet(self.seconts_descanso_style)
        else:
          self.label_estado.setText('Trabajando.')
          self.label_segundos.setStyleSheet(self.seconts_run_style)

    def pausar_reloj(self):
        if self.hilo_1s.isRunning():
          self.hilo_1s.stop()
          self.label_estado.setText('Pausado.')
          self.label_segundos.setStyleSheet(self.seconts_pause_style)

    def reset_reloj(self):
        self.hilo_1s.stop()
        self.segundos = 0
        self.label_vueltas.setText("0")
        self.actualizar_segundos()
        self.label_estado.setText('Esperando...')
        self.label_segundos.setStyleSheet(self.seconts_run_style)

    @pyqtSlot(bool)
    def beep_1s(self, value):
        self.sumar_segundo()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
