from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QTimer, QPointF
from core.shape_manager import DraggableRectItem

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_handler = None
        self.shape_manager = None
        self.width_box = None
        self.height_box = None
        self.pixmap_item = None

        self._zoom_step = 1.25

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setFocusPolicy(Qt.StrongFocus)

        self.arrow_timer = QTimer(self)
        self.arrow_timer.timeout.connect(self.move_selected_item)
        self.move_direction = QPointF(0, 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton and self.image_handler and self.image_handler.image:
            scene_pos = self.mapToScene(event.pos())

            width = self.width_box.value()
            height = self.height_box.value()

            max_w = self.image_handler.image.width - scene_pos.x()
            max_h = self.image_handler.image.height - scene_pos.y()

            width = min(width, max_w)
            height = min(height, max_h)

            if width <= 0 or height <= 0:
                print("Rectángulo fuera de límite")
                return

            rect = DraggableRectItem(scene_pos.x(), scene_pos.y(), width, height, self.pixmap_item, self.shape_manager)
            self.scene().addItem(rect)
            self.shape_manager.add_shape(rect)
        else:
            super().mousePressEvent(event)

    def wheelEvent(self, event):
        if not self.image_handler or not self.image_handler.image:
            return

        if event.modifiers() == Qt.ControlModifier:
            event.accept()
            old_pos = self.mapToScene(event.pos())

            if event.angleDelta().y() > 0:
                zoom_factor = self._zoom_step
            else:
                zoom_factor = 1 / self._zoom_step

            self.scale(zoom_factor, zoom_factor)

            new_pos = self.mapToScene(event.pos())
            delta = new_pos - old_pos
            self.translate(delta.x(), delta.y())
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        selected_items = self.scene().selectedItems()

        if event.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right] and selected_items:
            step = 1
            dx, dy = 0, 0

            if event.key() == Qt.Key_Up:
                dy = -step
            elif event.key() == Qt.Key_Down:
                dy = step
            elif event.key() == Qt.Key_Left:
                dx = -step
            elif event.key() == Qt.Key_Right:
                dx = step

            self.move_direction = QPointF(dx, dy)
            self.move_selected_item()  
            self.arrow_timer.start(30)

        elif event.key() == Qt.Key_Delete and selected_items:
            for item in selected_items:
                self.scene().removeItem(item)
                if item in self.shape_manager.shapes:
                    self.shape_manager.shapes.remove(item)


        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            self.arrow_timer.stop()


    def move_selected_item(self):
        selected_items = self.scene().selectedItems()
        if not selected_items:
            return

        dx, dy = self.move_direction.x(), self.move_direction.y()
        for item in selected_items:
            new_pos = item.pos() + QPointF(dx, dy)
            item.setPos(new_pos)
