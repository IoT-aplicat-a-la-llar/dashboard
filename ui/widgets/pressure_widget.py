"""
Widget personalizado para mostrar la presión atmosférica con un barómetro visual.
"""
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QFont, QLinearGradient, QRadialGradient
from PyQt6.QtCore import Qt, QRect, QRectF, QPointF, QTimer, QSize, pyqtProperty
import math

class PressureWidget(QWidget):
    def __init__(self, min_value=980, max_value=1020, parent=None):
        super().__init__(parent)
        
        # Valores por defecto
        self.value = 1010.0
        self.min_value = min_value
        self.max_value = max_value
        self.title = ""  # Se mostrará en contenedor principal
        self.unit = "hPa"
        
        # Transiciones y animación
        self.needle_angle = self._calculate_angle()
        self.target_angle = self.needle_angle
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._update_animation)
        self.animation_timer.start(16)  # ~60fps
        
        # Colores - Volver a configuración original
        self.low_color = QColor("#3498db")    # Azul para presión baja
        self.normal_color = QColor("#2ecc71") # Verde para presión normal
        self.high_color = QColor("#e74c3c")   # Rojo para presión alta
        self.background_color = QColor("#2d2d2d")
        self.text_color = QColor("#FFFFFF")
        
        # Categorías de presión (hPa)
        self.low_threshold = 1000.0
        self.high_threshold = 1015.0
        
        # Configurar el widget
        self.setMinimumSize(180, 180)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    def set_value(self, value):
        """Establece el valor de presión y actualiza la UI."""
        if value == self.value:
            return
            
        self.value = value
        self.target_angle = self._calculate_angle()
        self.update()
        
    def _calculate_angle(self):
        """Calcula el ángulo de la aguja según el valor de presión."""
        # Mapear el rango de presión (min_value-max_value) a un ángulo (240 grados, de -120 a 120)
        return self._pressure_to_angle(self.value)
        
    def _pressure_to_angle(self, pressure):
        """Convierte un valor de presión a ángulo en grados para la aguja (invertido)."""
        # INVERTIDO: Mapear presión a ángulo en sentido contrario
        norm_value = (pressure - self.min_value) / (self.max_value - self.min_value)
        # Invertimos el ángulo: 980 ahora apunta a +120 y 1020 apunta a -120
        angle = 120 - (norm_value * 240)
        return angle
        
    def _update_animation(self):
        """Actualiza la animación de la aguja."""
        if abs(self.needle_angle - self.target_angle) < 0.1:
            self.needle_angle = self.target_angle
        else:
            # Animación suave con easing
            self.needle_angle += (self.target_angle - self.needle_angle) * 0.1
            self.update()
    
    def paintEvent(self, event):
        """Dibuja el barómetro."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Dibujar el fondo
        self._draw_background(painter, width, height)
        
        # Dibujar el dial del barómetro
        self._draw_dial(painter, width, height)
        
        # Dibujar la aguja
        self._draw_needle(painter, width, height)
        
        # Dibujar marcas de valor
        self._draw_markers(painter, width, height)
        
        # Dibujar el texto del valor
        self._draw_text(painter, width, height)
        
        painter.end()
        
    def _draw_background(self, painter, width, height):
        """Dibuja el fondo del barómetro."""
        # Fondo circular con degradado para efecto 3D
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.45
        
        gradient = QRadialGradient(center_x, center_y, radius)
        gradient.setColorAt(0, QColor(65, 65, 65))
        gradient.setColorAt(1, QColor(45, 45, 45))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y), radius, radius)
        
        # Borde del barómetro
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawEllipse(QPointF(center_x, center_y), radius, radius)
        
    def _draw_dial(self, painter, width, height):
        """Dibuja el dial con las zonas de presión."""
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.4
        
        # Dibujar arco para cada zona (240 grados total, desde -120 a 120)
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Volver a la configuración original para las zonas de color
        # Calcular ángulos para las zonas
        min_angle = -120  # Izquierda (presión baja)
        max_angle = 120   # Derecha (presión alta)
        
        # Calcular ángulos para los umbrales
        low_angle = min_angle + ((self.low_threshold - self.min_value) / 
                                (self.max_value - self.min_value)) * 240
        high_angle = min_angle + ((self.high_threshold - self.min_value) / 
                                 (self.max_value - self.min_value)) * 240
        
        # Zona baja (azul) - izquierda
        painter.setBrush(QBrush(self.low_color))
        painter.drawPie(
            int(center_x - radius), 
            int(center_y - radius), 
            int(radius * 2), 
            int(radius * 2),
            int(min_angle * 16),
            int((low_angle - min_angle) * 16)
        )
        
        # Zona normal (verde) - centro
        painter.setBrush(QBrush(self.normal_color))
        painter.drawPie(
            int(center_x - radius), 
            int(center_y - radius), 
            int(radius * 2), 
            int(radius * 2),
            int(low_angle * 16),
            int((high_angle - low_angle) * 16)
        )
        
        # Zona alta (roja) - derecha
        painter.setBrush(QBrush(self.high_color))
        painter.drawPie(
            int(center_x - radius), 
            int(center_y - radius), 
            int(radius * 2), 
            int(radius * 2),
            int(high_angle * 16),
            int((max_angle - high_angle) * 16)
        )
        
        # Círculo interior para dar efecto de profundidad
        inner_radius = radius * 0.85
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawEllipse(QPointF(center_x, center_y), inner_radius, inner_radius)
        
    def _draw_needle(self, painter, width, height):
        """Dibuja la aguja del barómetro."""
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.35
        
        # SOLUCIÓN: Usar directamente el valor real para determinar el color
        # Esto asegura que el color de la aguja coincida con las zonas del dial
        if self.value < self.low_threshold:
            needle_color = self.low_color
        elif self.value < self.high_threshold:
            needle_color = self.normal_color
        else:
            needle_color = self.high_color
            
        # Calcular punto final de la aguja basado en el ángulo
        angle_rad = self.needle_angle * 3.14159 / 180
        end_x = center_x + radius * 0.8 * math.cos(angle_rad)
        end_y = center_y + radius * 0.8 * math.sin(angle_rad)
        
        # Dibujar la aguja con mayor grosor para mejor visibilidad
        painter.setPen(QPen(needle_color, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(int(center_x), int(center_y), int(end_x), int(end_y))
        
        # Eje central (círculo pequeño)
        painter.setBrush(QBrush(needle_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y), 6, 6)
        
    def _draw_markers(self, painter, width, height):
        """Dibuja las marcas y etiquetas alrededor del dial (con números invertidos)."""
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.4
        
        # Configurar fuente
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        
        # Dibujar marcas principales y etiquetas con posiciones invertidas:
        # 980 a la derecha, 1020 a la izquierda (mantenemos los colores originales)
        for i, value in enumerate([self.min_value, 1000, 1010, self.max_value]):
            # Calcular ángulo para este valor (INVERTIDO)
            norm_value = (value - self.min_value) / (self.max_value - self.min_value)
            angle = 120 - (norm_value * 240)  # Invertido: 0 → +120, 1 → -120
            angle_rad = angle * 3.14159 / 180
            
            # Dibujar línea de marca con mayor grosor para mejor visibilidad
            inner_x = center_x + (radius * 0.8) * math.cos(angle_rad)
            inner_y = center_y + (radius * 0.8) * math.sin(angle_rad)
            outer_x = center_x + radius * math.cos(angle_rad)
            outer_y = center_y + radius * math.sin(angle_rad)
            
            painter.setPen(QPen(QColor(220, 220, 220), 2.5))
            painter.drawLine(int(inner_x), int(inner_y), int(outer_x), int(outer_y))
            
            # Dibujar etiqueta
            text_x = center_x + (radius * 1.15) * math.cos(angle_rad)
            text_y = center_y + (radius * 1.15) * math.sin(angle_rad)
            
            painter.setPen(self.text_color)
            text_rect = QRectF(text_x - 20, text_y - 10, 40, 20)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(int(value)))
        
        # Dibujar marcas menores con mayor visibilidad (también invertidas)
        for i in range(10):
            value = self.min_value + (i * (self.max_value - self.min_value) / 10)
            norm_value = (value - self.min_value) / (self.max_value - self.min_value)
            angle = 120 - (norm_value * 240)  # Invertido
            angle_rad = angle * 3.14159 / 180
            
            # Saltar las marcas principales
            if value in [self.min_value, 1000, 1010, self.max_value]:
                continue
                
            inner_x = center_x + (radius * 0.85) * math.cos(angle_rad)
            inner_y = center_y + (radius * 0.85) * math.sin(angle_rad)
            outer_x = center_x + radius * math.cos(angle_rad)
            outer_y = center_y + radius * math.sin(angle_rad)
            
            painter.setPen(QPen(QColor(180, 180, 180), 1.5))
            painter.drawLine(int(inner_x), int(inner_y), int(outer_x), int(outer_y))
            
    def _draw_text(self, painter, width, height):
        """Dibuja el valor de presión en una cabina central."""
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.18  # Reducir el tamaño de la cabina central
        
        # Dibujar la cabina central (círculo con efecto metálico)
        # Gradiente radial para efecto metálico
        metal_gradient = QRadialGradient(center_x - radius/3, center_y - radius/3, radius*2)
        metal_gradient.setColorAt(0, QColor(80, 80, 80))
        metal_gradient.setColorAt(0.5, QColor(60, 60, 60))
        metal_gradient.setColorAt(1, QColor(40, 40, 40))
        
        # Dibujar el círculo metálico de fondo
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.setBrush(QBrush(metal_gradient))
        painter.drawEllipse(QPointF(center_x, center_y), radius, radius)
        
        # Dibujar un borde interno para dar efecto de profundidad
        painter.setPen(QPen(QColor(30, 30, 30), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(center_x, center_y), radius-2, radius-2)
        
        # Valor numérico grande en el centro
        value_font = QFont()
        value_font.setPointSize(14)  # Reducir tamaño para la cabina más pequeña
        value_font.setBold(True)
        painter.setFont(value_font)
        
        # Determinar color según el valor real de presión (no según el ángulo)
        if self.value < self.low_threshold:
            value_color = self.low_color
        elif self.value < self.high_threshold:
            value_color = self.normal_color
        else:
            value_color = self.high_color
            
        # Dibujar sombra sutil para dar profundidad
        shadow_color = QColor(0, 0, 0, 100)
        painter.setPen(shadow_color)
        value_shadow_rect = QRectF(center_x - radius + 2, center_y - 10 + 2, radius * 2, 20)
        painter.drawText(value_shadow_rect, Qt.AlignmentFlag.AlignCenter, f"{self.value:.1f}")
        
        # Dibujar el valor
        painter.setPen(value_color)
        value_rect = QRectF(center_x - radius, center_y - 10, radius * 2, 20)
        painter.drawText(value_rect, Qt.AlignmentFlag.AlignCenter, f"{self.value:.1f}")
        
        # Unidad en la parte inferior de la cabina
        unit_font = QFont()
        unit_font.setPointSize(8)  # Fuente más pequeña para la unidad
        painter.setFont(unit_font)
        painter.setPen(QColor(200, 200, 200))  # Gris claro
        
        unit_rect = QRectF(center_x - radius, center_y + 3, radius * 2, 14)
        painter.drawText(unit_rect, Qt.AlignmentFlag.AlignCenter, self.unit)
        
        # Dibujar "ventana" de la cabina con efecto de reflejo
        highlight_pen = QPen(QColor(255, 255, 255, 30), 1)  # Línea más fina
        painter.setPen(highlight_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawArc(
            int(center_x - radius + 3), 
            int(center_y - radius + 3),
            int((radius-3) * 2), 
            int((radius-3) * 2), 
            45 * 16, 
            180 * 16
        )
        
    def sizeHint(self):
        """Tamaño preferido para el widget."""
        return QSize(200, 200) 