from datetime import datetime
from pathlib import Path
import sys
from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QColor, QGuiApplication, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QWidget


class SnippingTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.BypassWindowManagerHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.showFullScreen()
        self.setCursor(Qt.CursorShape.CrossCursor)

        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_selecting = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.is_selecting = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            self.end_point = event.pos()
            self.is_selecting = False
            self.capture_region()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()

    def paintEvent(self, event):
        painter = QPainter(self)

        # draw semi-transparent grey overlay across the entire screen
        overlay_color = QColor(0, 0, 0, 100)
        painter.fillRect(self.rect(), overlay_color)

        if self.is_selecting:
            rect = QRect(self.start_point, self.end_point).normalized()

            # cut out the selected region to reveal original screen opacity
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, Qt.GlobalColor.transparent)

            # draw grey border around the cut region
            painter.setCompositionMode(
                QPainter.CompositionMode.CompositionMode_SourceOver
            )
            pen = QPen(QColor(128, 128, 128), 2)
            painter.setPen(pen)
            painter.drawRect(rect)

    def capture_region(self):
        rect = QRect(self.start_point, self.end_point).normalized()
        if rect.width() > 0 and rect.height() > 0:
            self.hide()
            QApplication.processEvents()

            screen = QGuiApplication.primaryScreen()
            pixmap = screen.grabWindow(
                0, rect.x(), rect.y(), rect.width(), rect.height()
            )

            QGuiApplication.clipboard().setPixmap(pixmap)

            downloads_dir = Path.home() / "Downloads"
            date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = downloads_dir / f"Screenshot-{date_str}.png"
            pixmap.save(str(file_path), "PNG")

        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    snipper = SnippingTool()
    snipper.show()
    sys.exit(app.exec())
