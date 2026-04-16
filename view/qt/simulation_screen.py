from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QSpinBox,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSignal, Qt
from view.qt.ui_parts import CardFrame, PrimaryButton


class SimulationScreen(QWidget):
    run_simulation_requested = pyqtSignal(str, int)
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top_y = 210
        card_w = min(900, self.width() - 80)
        card_h = min(420, self.height() - top_y - 50)

        card_w = max(700, card_w)
        card_h = max(320, card_h)

        x = (self.width() - card_w) // 2
        self.card.setGeometry(x, top_y, card_w, card_h)

    def _build_ui(self):
        self.card = CardFrame(self)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(34, 28, 34, 28)
        layout.setSpacing(22)

        title = QLabel("Monte Carlo Scenario-Based Simulation")
        title.setStyleSheet("""
            QLabel {
                color: #704F14;
                font-size: 28px;
                font-weight: 700;
            }
        """)
        layout.addWidget(title)

        subtitle = QLabel("Select a scenario and number of iterations to simulate accident risk outcomes.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 16px;
            }
        """)
        layout.addWidget(subtitle)

        scenario_label = QLabel("Scenario")
        scenario_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 18px;
                font-weight: 700;
            }
        """)
        layout.addWidget(scenario_label)

        self.scenario_combo = QComboBox()
        self.scenario_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.scenario_combo.setMinimumHeight(52)
        self.scenario_combo.setStyleSheet("""
            QComboBox {
                background: white;
                border: 1px solid #AFAFAF;
                border-radius: 18px;
                padding: 0 16px;
                font-size: 16px;
                color: #434343;
            }
            QComboBox::drop-down {
                border: none;
                width: 34px;
            }
        """)
        layout.addWidget(self.scenario_combo)

        iterations_label = QLabel("Iterations")
        iterations_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 18px;
                font-weight: 700;
            }
        """)
        layout.addWidget(iterations_label)

        self.iterations_spin = QSpinBox()
        self.iterations_spin.setRange(100, 10000)
        self.iterations_spin.setSingleStep(100)
        self.iterations_spin.setValue(1000)
        self.iterations_spin.setMinimumHeight(52)
        self.iterations_spin.setStyleSheet("""
            QSpinBox {
                background: white;
                border: 1px solid #AFAFAF;
                border-radius: 18px;
                padding: 0 16px;
                font-size: 16px;
                color: #434343;
            }
        """)
        layout.addWidget(self.iterations_spin)

        button_row = QHBoxLayout()
        button_row.setSpacing(14)

        self.back_button = QPushButton("Back")
        self.back_button.setMinimumHeight(54)
        self.back_button.setStyleSheet("""
            QPushButton {
                background: #353434;
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: 600;
                padding: 0 22px;
            }
        """)
        self.back_button.clicked.connect(self.back_requested.emit)

        self.run_button = PrimaryButton("Run Simulation")
        self.run_button.clicked.connect(self._emit_simulation)

        button_row.addWidget(self.back_button)
        button_row.addStretch()
        button_row.addWidget(self.run_button)

        layout.addSpacing(8)
        layout.addLayout(button_row)
        layout.addStretch()

    def set_scenarios(self, scenarios: list[str]):
        self.scenario_combo.clear()
        self.scenario_combo.addItems(scenarios)

    def _emit_simulation(self):
        scenario = self.scenario_combo.currentText()
        iterations = int(self.iterations_spin.value())
        self.run_simulation_requested.emit(scenario, iterations)