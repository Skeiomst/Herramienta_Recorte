from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QPointF, QRectF
import os

class ShapeManager:
    def __init__(self):
        self.shapes = []

    def add_shape(self, rect_item):
        self.shapes.append(rect_item)

    def clear_shapes(self):
        self.shapes.clear()

    def save_all_shapes(self, image_handler, folder_path):
        original_name = os.path.splitext(os.path.basename(image_handler.path))[0]
        output_dir = os.path.join(folder_path, original_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i, shape in enumerate(self.shapes):
            pos = shape.pos()
            size = shape.rect().size()

            x = int(pos.x())
            y = int(pos.y())
            w = int(size.width())
            h = int(size.height())

            crop = image_handler.crop(x, y, w, h)

            filename = f"{original_name}_recorte_{i+1}.jpg"
            crop.save(os.path.join(output_dir, filename))

        return len(self.shapes)



class DraggableRectItem(QGraphicsRectItem):
    def __init__(self, x, y, w, h, pixmap_item, shape_manager):
        super().__init__(0, 0, w, h)
        self.pixmap_item = pixmap_item
        self.setPos(x, y)
        self.shape_manager = shape_manager

        self.setBrush(QBrush(QColor(0, 255, 0, 50)))
        self.setPen(QPen(Qt.green, 2))
        self.setFlags(
            QGraphicsRectItem.ItemIsMovable |
            QGraphicsRectItem.ItemIsSelectable |
            QGraphicsRectItem.ItemSendsGeometryChanges |
            QGraphicsRectItem.ItemIsFocusable
        )
        self.setAcceptHoverEvents(True)

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            new_pos = value
            if not self.scene() or not self.pixmap_item:
                return new_pos

            image_rect = self.pixmap_item.sceneBoundingRect()
            rect_size = self.rect().size()

            new_x = new_pos.x()
            new_y = new_pos.y()

            new_x = min(max(new_x, image_rect.left()), image_rect.right() - rect_size.width())
            new_y = min(max(new_y, image_rect.top()), image_rect.bottom() - rect_size.height())

            return QPointF(new_x, new_y)

        return super().itemChange(change, value)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            scene = self.scene()
            if scene:
                scene.removeItem(self)
            if self.shape_manager and self in self.shape_manager.shapes:
                self.shape_manager.shapes.remove(self)

