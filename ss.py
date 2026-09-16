import sys
import time
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QColor, QGuiApplication, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget


class WindowsNativeButtonBar(QWidget):
    def __init__(self, main_snipper):
        super().__init__()
        self.main_snipper = main_snipper

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setFixedHeight(36)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        self.setStyleSheet("""
            QWidget {
                background-color: #1f1f1f;
                border: 1px solid #333333;
                border-radius: 6px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3b3b3b;
                border-radius: 4px;
                min-width: 28px;
                min-height: 28px;
                max-width: 28px;
                max-height: 28px;
                font-size: 13px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #383838;
                border-color: #454545;
            }
            QPushButton:pressed {
                background-color: #242424;
                color: #cccccc;
            }
            QPushButton#close_btn:hover {
                background-color: #c42b1c;
                border-color: #c42b1c;
            }
            QPushButton#close_btn:pressed {
                background-color: #a82315;
            }
        """)

        self.copy_btn = QPushButton("📋", self)
        self.save_btn = QPushButton("💾", self)
        self.close_btn = QPushButton("✕", self)
        self.close_btn.setObjectName("close_btn")

        layout.addWidget(self.copy_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.close_btn)

        self.copy_btn.clicked.connect(self.main_snipper.action_copy)
        self.save_btn.clicked.connect(self.main_snipper.action_save_and_copy)
        self.close_btn.clicked.connect(self.main_snipper.action_close)


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
        self.selection_done = False
        self.selected_rect = QRect()

        self.button_bar = WindowsNativeButtonBar(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.selection_done:
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.is_selecting = True

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            t_release = time.perf_counter()
            print(f"[TEST] Mouse released at {t_release:.4f}s")

            self.is_selecting = False
            self.selected_rect = QRect(self.start_point, event.pos()).normalized()

            if self.selected_rect.width() > 5 and self.selected_rect.height() > 5:
                self.selection_done = True
                self.setCursor(Qt.CursorShape.ArrowCursor)

                bw, bh = 110, 36
                rx, ry = self.selected_rect.right(), self.selected_rect.bottom()

                bx = rx - bw
                by = (
                    ry + 6
                    if ry + bh + 6 <= self.height()
                    else self.selected_rect.top() - bh - 6
                )

                # Position and show the independent top-level button window instantly
                self.button_bar.setGeometry(bx, by, bw, bh)
                self.button_bar.show()

                t_shown = time.perf_counter()
                print(
                    f"[TEST] Buttons shown at {t_shown:.4f}s (delta: {(t_shown - t_release)*1000:.2f}ms)"
                )

            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        if self.is_selecting or self.selection_done:
            rect = (
                self.selected_rect
                if self.selection_done
                else QRect(self.start_point, self.end_point).normalized()
            )

            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, Qt.GlobalColor.transparent)

            painter.setCompositionMode(
                QPainter.CompositionMode.CompositionMode_SourceOver
            )
            painter.setPen(QPen(QColor(128, 128, 128), 2))
            painter.drawRect(rect)

    def grab_selection(self) -> QPixmap:
        self.button_bar.hide()
        self.hide()
        QApplication.processEvents()

        return QGuiApplication.primaryScreen().grabWindow(
            0,
            self.selected_rect.x(),
            self.selected_rect.y(),
            self.selected_rect.width(),
            self.selected_rect.height(),
        )

    def action_copy(self):
        pixmap = self.grab_selection()
        QGuiApplication.clipboard().setPixmap(pixmap)
        QApplication.quit()

    def action_save_and_copy(self):
        pixmap = self.grab_selection()
        QGuiApplication.clipboard().setPixmap(pixmap)

        downloads_dir = Path.home() / "Downloads"
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pixmap.save(str(downloads_dir / f"Screenshot-{date_str}.png"), "PNG")

        QApplication.quit()

    def action_close(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    snipper = SnippingTool()
    snipper.show()
    sys.exit(app.exec())
