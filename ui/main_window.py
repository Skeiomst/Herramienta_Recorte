from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QPushButton, QSizePolicy, QLabel, QSpinBox,
    QGraphicsScene, QVBoxLayout, QWidget, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import (Qt, QRectF, QPointF, QTimer)
import os

from core.image_handler import ImageHandler
from core.shape_manager import ShapeManager
from ui.custom_graphics_view import CustomGraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recorte por Figuras v1.1.0")
        self.setGeometry(100, 100, 1000, 700)

        self.image_handler = ImageHandler()
        self.shape_manager = ShapeManager()

        self._default_transform = None
        self.original_name = ""

        self.init_ui()

    def init_ui(self):
        top_layout = QGridLayout()

        # Botón: Cargar imagen
        self.load_btn = QPushButton("Cargar Imagen")
        self.load_btn.clicked.connect(self.load_image)
        top_layout.addWidget(self.load_btn, 0, 0)

        # Ancho
        width_label = QLabel("Ancho:")
        width_label.setFixedWidth(50)
        width_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_layout.addWidget(width_label, 0, 1)
        self.width_box = QSpinBox()
        self.width_box.setRange(1, 1000)
        self.width_box.setValue(640)
        top_layout.addWidget(self.width_box, 0, 2)

        # Alto
        height_label = QLabel("Alto:")
        height_label.setFixedWidth(50)
        height_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_layout.addWidget(height_label, 0, 3)
        self.height_box = QSpinBox()
        self.height_box.setRange(1, 1000)
        self.height_box.setValue(640)
        top_layout.addWidget(self.height_box, 0, 4)

        # Guardar recortes
        self.save_btn = QPushButton("Guardar Recortes")
        self.save_btn.clicked.connect(self.save_crops)
        top_layout.addWidget(self.save_btn, 0, 5)

        # Resetear zoom
        self.reset_zoom_btn = QPushButton("Resetear Zoom")
        self.reset_zoom_btn.clicked.connect(self.reset_zoom)
        top_layout.addWidget(self.reset_zoom_btn, 0, 6)

        top_layout.setSpacing(10)
        top_layout.setContentsMargins(10, 5, 10, 5)

        # Escena y vista personalizada
        self.scene = QGraphicsScene()
        self.view = CustomGraphicsView()
        self.view.setScene(self.scene)
        self.view.setFocusPolicy(Qt.StrongFocus)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)

        # Asociar dependencias
        self.view.image_handler = self.image_handler
        self.view.shape_manager = self.shape_manager
        self.view.width_box = self.width_box
        self.view.height_box = self.height_box

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.view)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self._default_transform = self.view.transform()

    def reset_zoom(self):
        self.view.setTransform(self._default_transform)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecciona una imagen", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image_handler.load_image(path)
            pixmap = QPixmap(path)
            self.scene.clear()

            self.pixmap_item = self.scene.addPixmap(pixmap)
            self.view.pixmap_item = self.pixmap_item

            self.shape_manager.clear_shapes()
            self.view.setSceneRect(QRectF(pixmap.rect()))
            self.original_name = os.path.splitext(os.path.basename(path))[0]
            self.setWindowTitle(f"Recorte por Figuras v1.1.0 - {self.original_name}")

            self.view.setFocus()


    def save_crops(self):
        if not self.image_handler.image:
            return

        folder = QFileDialog.getExistingDirectory(self, "Selecciona carpeta para guardar")
        if not folder:
            return

        count = self.shape_manager.save_all_shapes(self.image_handler, folder)
        QMessageBox.information(self, "Recortes guardados", f"Se guardaron {count} recortes exitosamente.")

    