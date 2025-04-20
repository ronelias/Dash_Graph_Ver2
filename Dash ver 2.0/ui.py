from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QLineEdit,
    QTextEdit, QTableWidget, QTableWidgetItem, QStatusBar, QLabel,
    QWidget, QSplitter, QSizePolicy, QHBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
from gpt_handler import generate_code_from_prompt
from helpers import load_csv_file, display_dataframe, apply_df_filter
from PyQt5.QtGui import QIcon
import os
from eda import run_eda
import webbrowser
import logging
import re

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame()
        self.original_df = pd.DataFrame()
        self.current_theme = "light"
        self.setWindowTitle("DashGraph")
        self.setGeometry(100, 100, 1700, 775)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        controls_layout = QVBoxLayout()

        # Top bar with theme icon
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        self.theme_button = QPushButton("🌓")
        self.theme_button.setObjectName("themeToggleBtn")
        self.theme_button.clicked.connect(self.toggle_theme)
        top_bar.addWidget(self.theme_button)
        controls_layout.addLayout(top_bar)

        # ────────────── Load Section ──────────────
        load_label = QLabel("Load Data:")
        load_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        controls_layout.addWidget(load_label)

        self.load_button = QPushButton("📂 Load CSV")
        self.load_button.setToolTip("Load a CSV file into the table")
        self.load_button.clicked.connect(self.load_csv)
        controls_layout.addWidget(self.load_button)
        controls_layout.addSpacing(15)

        # ────────────── Filter and Graph Section in Grid ──────────────
        grid_layout = QGridLayout()

        filter_label = QLabel("Filter Data:")
        filter_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        grid_layout.addWidget(filter_label, 0, 0, 1, 2)

        self.filter_input = QTextEdit()
        self.filter_input.setPlaceholderText("e.g., Age > 30 and Country == 'US'")
        self.filter_input.setMinimumHeight(70)
        

        self.filter_button = QPushButton("🔍 Apply")
        self.filter_button.clicked.connect(self.apply_filter)
        self.reset_filter_button = QPushButton("🔄 Reset")
        self.reset_filter_button.clicked.connect(self.reset_filter)

        grid_layout.addWidget(self.filter_input, 1, 0, 2, 1)
        grid_layout.addWidget(self.filter_button, 1, 1)
        grid_layout.addWidget(self.reset_filter_button, 2, 1)

        graph_label = QLabel("Describe Graph:")
        graph_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        grid_layout.addWidget(graph_label, 3, 0, 1, 2)

        self.nl_input = QTextEdit()
        self.nl_input.setPlaceholderText("e.g., show average age per country as a bar chart")
        self.graph_button = QPushButton("📊 Generate")
        self.graph_button.clicked.connect(self.generate_graph)
        self.graph_button.setMinimumHeight(100)

        grid_layout.addWidget(self.nl_input, 4, 0)
        grid_layout.addWidget(self.graph_button, 4, 1)

        controls_layout.addLayout(grid_layout)
        controls_layout.addSpacing(15)

        # ────────────── EDA Section ──────────────
        eda_label = QLabel("Advanced EDA:")
        eda_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        controls_layout.addWidget(eda_label)

        self.eda_button = QPushButton("🧠 Smart EDA Summary")
        self.eda_button.setMinimumHeight(48)
        self.eda_button.clicked.connect(self.run_eda_summary)
        controls_layout.addWidget(self.eda_button)

        controls_layout.addStretch()
        control_widget = QWidget()
        control_widget.setLayout(controls_layout)

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(control_widget)
        splitter.addWidget(self.table)
        splitter.setSizes([350, 900])

        main_layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.load_theme("light")

    def load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if path:
            try:
                self.df = load_csv_file(path)
                self.original_df = self.df.copy()

                if self.df.empty or self.df.shape[1] == 0:
                    self.status.showMessage("⚠️ Loaded dataset has no columns.", 5000)
                    return

                display_dataframe(self.df, self.table)
                self.status.showMessage(f"✅ Loaded: {path}", 5000)
            except Exception as e:
                logger.exception("CSV load failed")
                self.status.showMessage(f"❌ Failed to load: {e}", 5000)

    def apply_filter(self):
        try:
            expr = self.filter_input.toPlainText().strip()
            query_cols = re.findall(r"\\b[a-zA-Z_][a-zA-Z0-9_]*\\b", expr)
            for col in query_cols:
                if col not in self.df.columns:
                    self.status.showMessage(f"❌ Unknown column in filter: '{col}'", 5000)
                    return

            self.df = apply_df_filter(self.df, expr)
            display_dataframe(self.df, self.table)
            self.status.showMessage("✅ Filter applied", 3000)
        except Exception as e:
            logger.exception("Filter application failed")
            self.status.showMessage(f"❌ Filter error: {e}", 5000)

    def reset_filter(self):
        self.df = self.original_df.copy()
        display_dataframe(self.df, self.table)
        self.status.showMessage("🔄 Filters reset", 3000)

    def generate_graph(self):
        prompt = self.nl_input.toPlainText().strip()
        if not prompt:
            self.status.showMessage("⚠️ No prompt provided", 3000)
            return
        try:
            code = generate_code_from_prompt(prompt, self.df)
            exec_globals = {"df": self.df, "plt": plt}
            exec(code, exec_globals)
            plt.savefig("last_generated_plot.png", bbox_inches="tight")
            plt.show()
            self.status.showMessage("✅ Graph generated and saved", 3000)
        except Exception as e:
            logger.exception("Graph generation failed")
            self.status.showMessage(f"❌ Graph error: {e}", 5000)

    def save_last_plot(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Graph As", "", "PNG Image (*.png)")
        if file_path:
            try:
                from shutil import copyfile
                copyfile("last_generated_plot.png", file_path)
                self.status.showMessage(f"✅ Graph saved to {file_path}", 4000)
            except Exception as e:
                logger.exception("Saving plot failed")
                self.status.showMessage(f"❌ Save failed: {e}", 5000)

    def toggle_theme(self):
        self.load_theme("dark" if self.current_theme == "light" else "light")

    def load_theme(self, theme_name: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        qss_path = os.path.join(base_dir, "styles", f"{theme_name}.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as file:
                self.setStyleSheet(file.read())
            self.current_theme = theme_name
        else:
            self.status.showMessage(f"❌ Theme file not found: {qss_path}", 5000)

    def run_eda_summary(self):
        if self.df.empty:
            self.status.showMessage("⚠️ No data loaded for EDA", 4000)
            return
        try:
            report_path = run_eda(self.df)
            self.status.showMessage(f"✅ EDA saved to {report_path}", 3000)
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
        except Exception as e:
            logger.exception("EDA generation failed")
            self.status.showMessage(f"❌ EDA error: {e}", 5000)