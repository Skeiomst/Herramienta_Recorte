from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QSizePolicy, QLabel, QSpinBox, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget, QGridLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF
from core.image_handler import ImageHandler
from core.shape_manager import ShapeManager, DraggableRectItem
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recorte por Figuras")
        self.setGeometry(100, 100, 1000, 700)
        self.image_handler = ImageHandler()
        self.shape_manager = ShapeManager()

        self._zoom = 0
        self._zoom_step = 1.25
        self._default_transform = None

        self.pixmap_item = None

        self.init_ui()

    def init_ui(self):
        top_layout = QGridLayout()

        self.load_btn = QPushButton("Cargar Imagen")
        self.load_btn.clicked.connect(self.load_image)
        top_layout.addWidget(self.load_btn, 0, 0)

        width_label = QLabel("Ancho:")
        width_label.setFixedWidth(50)
        width_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_layout.addWidget(width_label, 0, 1)
        self.width_box = QSpinBox()
        self.width_box.setRange(1, 1000)
        self.width_box.setValue(640)
        top_layout.addWidget(self.width_box, 0, 2)

        height_label = QLabel("Ancho:")
        height_label.setFixedWidth(50)
        height_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_layout.addWidget(height_label, 0, 3)
        self.height_box = QSpinBox()
        self.height_box.setRange(1, 1000)
        self.height_box.setValue(640)
        top_layout.addWidget(self.height_box, 0, 4)

        self.save_btn = QPushButton("Guardar Recortes")
        self.save_btn.clicked.connect(self.save_crops)
        top_layout.addWidget(self.save_btn, 0, 5)

        self.reset_zoom_btn = QPushButton("Resetear Zoom")
        self.reset_zoom_btn.clicked.connect(self.reset_zoom)
        top_layout.addWidget(self.reset_zoom_btn, 0, 6)

        top_layout.setSpacing(10)
        top_layout.setContentsMargins(10, 5, 10, 5)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFocusPolicy(Qt.StrongFocus)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.view)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self._default_transform = self.view.transform()

    def reset_zoom(self):
        self.view.setTransform(self._default_transform)
        self._zoom = 0


    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecciona una imagen", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image_handler.load_image(path)
            pixmap = QPixmap(path)
            self.scene.clear()
            self.pixmap_item = self.scene.addPixmap(pixmap)
            self.scene.addPixmap(pixmap)
            self.shape_manager.clear_shapes()
            self.view.setSceneRect(QRectF(pixmap.rect()))
            self.original_name = os.path.splitext(os.path.basename(path))[0]
            self.setWindowTitle(f"Recorte por Figuras - {self.original_name}")

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton and self.image_handler.image:
            pos = self.view.mapToScene(event.pos())
            width = self.width_box.value()
            height = self.height_box.value()

            max_w = self.image_handler.image.width - pos.x()
            max_h = self.image_handler.image.height - pos.y()

            width = min(width, max_w)
            height = min(height, max_h)

            if width <= 0 or height <= 0:
                # print("Rectángulo fuera del límite.")
                return

            rect = DraggableRectItem(pos.x(), pos.y(), width, height, self.pixmap_item, self.shape_manager)
            self.scene.addItem(rect)
            self.shape_manager.add_shape(rect)



    def save_crops(self):
        if not self.image_handler.image:
            return

        folder = QFileDialog.getExistingDirectory(self, "Selecciona carpeta para guardar")
        if not folder:
            return

        count = self.shape_manager.save_all_shapes(self.image_handler, folder)

        QMessageBox.information(self, "Recortes guardados", f"Se guardaron {count} recortes exitosamente.")

    def keyPressEvent(self, event):
        selected_items = self.scene.selectedItems()
        if event.key() == Qt.Key_Delete and selected_items:
            for item in selected_items:
                self.scene.removeItem(item)
                if item in self.shape_manager.shapes:
                    self.shape_manager.shapes.remove(item)

    def wheelEvent(self, event):
        if not self.image_handler.image:
            return

        if event.modifiers() == Qt.ControlModifier:
            old_pos = self.view.mapToScene(event.pos())

            if event.angleDelta().y() > 0:
                zoom_factor = self._zoom_step
                self._zoom += 1
            else:
                zoom_factor = 1 / self._zoom_step
                self._zoom -= 1

            self.view.scale(zoom_factor, zoom_factor)

            new_pos = self.view.mapToScene(event.pos())
            delta = new_pos - old_pos
            self.view.translate(delta.x(), delta.y())