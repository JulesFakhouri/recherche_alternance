import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QLineEdit, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
import db

class JobSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Suivi de Recherche d'Emploi/Stage/Alternance")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.initUI()

    def initUI(self):
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Tous", "En attente", "Oui", "Non"])

        self.job_type_combo = QComboBox()
        self.job_type_combo.addItems(["Tous", "Stage", "Alternance", "Emploi"])

        self.company_name_input = QLineEdit()
        self.job_title_input = QLineEdit()
        self.job_link_input = QLineEdit()
        self.job_text_input = QTextEdit()

        self.filter_button = QPushButton("Filtrer")
        self.filter_button.clicked.connect(self.load_entries)

        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked connect(self.save_entry)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Type", "État", "Date", "Entreprise", "Poste", "Lien", "Texte", "Actions"])

        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Type d'annonce:"))
        form_layout.addWidget(self.job_type_combo)
        form_layout.addWidget(QLabel("État:"))
        form_layout.addWidget(self.status_combo)
        form_layout.addWidget(QLabel("Nom de l'entreprise:"))
        form_layout.addWidget(self.company_name_input)
        form_layout.addWidget(QLabel("Nom du poste:"))
        form_layout.addWidget(self.job_title_input)
        form_layout.addWidget(QLabel("Lien de l'annonce:"))
        form_layout.addWidget(self.job_link_input)
        form_layout.addWidget(QLabel("Texte de l'annonce:"))
        form_layout.addWidget(self.job_text_input)
        form_layout.addWidget(self.filter_button)
        form_layout.addWidget(self.save_button)
        layout.addLayout(form_layout)

        layout.addWidget(self.table)

        self.central_widget.setLayout(layout)

        self.load_entries()

    def load_entries(self):
        job_type = self.job_type_combo.currentText()
        status = self.status_combo.currentText()
        company_name = self.company_name_input.text()

        conn = db.create_database()
        entries = db.fetch_filtered_job_entries(conn, job_type, status, company_name)
        self.table.setRowCount(0)
        for entry in entries:
            self.add_entry_to_table(entry)
        conn.close()

    def save_entry(self):
        job_type = self.job_type_combo.currentText()
        status = self.status_combo.currentText()
        company_name = self.company_name_input.text()
        job_title = self.job_title_input.text()
        job_link = self.job_link_input.text()
        job_text = self.job_text_input.toPlainText()

        conn = db.create_database()
        db.insert_job_entry(conn, job_type, status, None, company_name, job_title, job_link, job_text)
        conn.close()
        self.load_entries()

    def add_entry_to_table(self, entry):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)

        for col, data in enumerate(entry[1:]):
            item = QTableWidgetItem(str(data))
            self.table.setItem(rowPosition, col, item)

        edit_button = QPushButton("Modifier")
        delete_button = QPushButton("Supprimer")
        edit_button.clicked.connect(lambda _, r=rowPosition: self.edit_entry(r))
        delete_button.clicked.connect(lambda _, r=rowPosition: self.delete_entry(r))

        self.table.setCellWidget(rowPosition, 7, edit_button)
        self.table.setCellWidget(rowPosition, 8, delete_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JobSearchApp()
    window.show()
    sys.exit(app.exec())
