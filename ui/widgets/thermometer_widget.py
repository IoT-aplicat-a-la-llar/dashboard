"""
Widget personalizado para mostrar un termómetro con un círculo exterior
que se rellena según la temperatura.
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QFont
from PyQt6.QtCore import Qt, QRect, QRectF

class ThermometerWidget(QWidget):
    def __init__(self, parent=None):
        """
        Inicializa un widget de termómetro personalizado.
        
        Args:
            parent (QWidget, optional): Widget padre
        """
        super().__init__(parent)
        self.setMinimumSize(180, 180)  # Tamaño mínimo del widget
        
        # Valores por defecto
        self.value = 25.0
        self.min_value = 0.0
        self.max_value = 40.0
        
        # Definir los colores del termómetro
        self._setup_colors()
        
        # Título vacío (ya se muestra en el contenedor)
        self.title = ""
        
        # Hacer que el widget sea transparente
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def _setup_colors(self):
        """Configura los colores del termómetro."""
        # Colores para la temperatura
        self.cold_color = QColor("#3498db")    # Azul para frío
        self.normal_color = QColor("#2ecc71")  # Verde para normal
        self.warm_color = QColor("#f39c12")    # Naranja para cálido
        self.hot_color = QColor("#e74c3c")     # Rojo para calor
        
        # Color del texto y fondo
        self.text_color = QColor("#FFFFFF")    # Blanco
        self.bg_color = QColor(0, 0, 0, 0)     # Transparente
        
    def set_value(self, value):
        """
        Establece el valor de temperatura actual.
        
        Args:
            value (float): Valor de temperatura
        """
        self.value = max(self.min_value, min(value, self.max_value))
        self.update()  # Actualizar el widget
        
    def set_range(self, min_value, max_value):
        """
        Establece el rango de temperatura.
        
        Args:
            min_value (float): Valor mínimo
            max_value (float): Valor máximo
        """
        self.min_value = min_value
        self.max_value = max_value
        self.update()
        
    def paintEvent(self, event):
        """
        Dibuja el widget del termómetro.
        
        Args:
            event: Evento de pintura
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calcular dimensiones
        width = self.width()
        height = self.height()
        size = min(width, height - 40)  # Reducir un poco la altura para dejar espacio al valor
        
        # Centrar el dibujo (un poco más arriba para dejar espacio abajo)
        painter.translate(width/2, (height/2) - 10)
        
        # Dibujar el círculo exterior
        self._draw_circle_progress(painter, size * 0.8)
        
        # Dibujar el termómetro interior
        self._draw_thermometer(painter, size * 0.55)
        
        # Dibujar el valor de temperatura (abajo)
        self._draw_temperature_value(painter, size)
    
    def _draw_title(self, painter, width, height):
        """Función vacía ya que el título ahora está en el contenedor."""
        pass  # No dibujar nada
    
    def _get_temperature_color(self):
        """
        Determina el color según la temperatura actual.
        
        Returns:
            QColor: Color correspondiente a la temperatura
        """
        if self.value < 20:
            return self.cold_color  # Azul para frío
        elif self.value <= 25:
            return self.normal_color  # Verde para normal
        elif self.value <= 28:
            return self.warm_color  # Naranja para cálido
        else:
            return self.hot_color  # Rojo para calor
    
    def _draw_circle_progress(self, painter, size):
        """
        Dibuja el círculo exterior que muestra el progreso de temperatura.
        
        Args:
            painter (QPainter): Objeto pintor
            size (float): Tamaño del círculo
        """
        # Calcular el porcentaje de la temperatura en el rango
        percentage = (self.value - self.min_value) / (self.max_value - self.min_value)
        
        # Calcular el color en función de la temperatura (usando los mismos umbrales que en main_window.py)
        color = self._get_temperature_color()
            
        # Establecer el grosor del círculo
        penWidth = size * 0.08  # Aumentamos el grosor para que sea más visible
        
        # Dibujar el círculo de fondo (solo contorno)
        painter.setPen(QPen(QColor(80, 80, 80, 180), penWidth))
        painter.setBrush(Qt.BrushStyle.NoBrush)  # Sin relleno
        painter.drawEllipse(QRectF(-size/2 + penWidth/2, -size/2 + penWidth/2,
                             size - penWidth, size - penWidth))
        
        # Dibujar el arco de progreso (solo contorno)
        painter.setPen(QPen(color, penWidth, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        
        # Calculamos el ángulo inicial (-90 grados) y el ángulo de barrido
        start_angle = int(-90 * 16)  # En QPainter los ángulos se multiplican por 16 y deben ser enteros
        span_angle = int(-percentage * 360 * 16)  # Convertir a entero
        
        # Convertir QRectF a QRect para drawArc
        rect = QRect(
            int(-size/2 + penWidth/2), 
            int(-size/2 + penWidth/2),
            int(size - penWidth), 
            int(size - penWidth)
        )
        
        # Dibujamos solo el arco (sin relleno)
        painter.drawArc(rect, start_angle, span_angle)
    
        # Dibujar el círculo interior (fondo transparente)
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))  # Completamente transparente
        painter.setPen(QPen(color, 1))  # Borde fino del color de la temperatura
        painter.drawEllipse(QRectF(-size * 0.4, -size * 0.4, size * 0.8, size * 0.8))
    
    def _draw_thermometer(self, painter, size):
        """
        Dibuja el termómetro interior.
        
        Args:
            painter (QPainter): Objeto pintor
            size (float): Tamaño del termómetro
        """
        # Calcular el porcentaje de temperatura
        percentage = (self.value - self.min_value) / (self.max_value - self.min_value)
        
        # Definir dimensiones del termómetro
        thermWidth = size * 0.2
        thermHeight = size * 0.6
        bulbRadius = thermWidth / 2
        
        # Dibujar el tubo del termómetro
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.setBrush(QBrush(QColor(220, 220, 220)))
        
        # Rectángulo para el tubo
        rect = QRectF(-thermWidth/2, -thermHeight/2, thermWidth, thermHeight)
        painter.drawRoundedRect(rect, thermWidth/4, thermWidth/4)
        
        # Dibujar el bulbo
        bulbRect = QRectF(-bulbRadius, thermHeight/2 - bulbRadius*2, 
                           bulbRadius*2, bulbRadius*2)
        painter.drawEllipse(bulbRect)
        
        # Calcular la altura del mercurio
        mercuryHeight = thermHeight * percentage
        
        # Establecer el color del mercurio
        color = self._get_temperature_color()
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(color))
        
        # Dibujar mercurio en el tubo
        mercuryRect = QRectF(-thermWidth/2 + 4, -thermHeight/2 + thermHeight - mercuryHeight + 4, 
                              thermWidth - 8, mercuryHeight - 8)
        painter.drawRoundedRect(mercuryRect, (thermWidth-8)/4, (thermWidth-8)/4)
        
        # Dibujar mercurio en el bulbo
        painter.drawEllipse(QRectF(-bulbRadius + 2, thermHeight/2 - bulbRadius*2 + 2, 
                                    bulbRadius*2 - 4, bulbRadius*2 - 4))
        
    def _draw_temperature_value(self, painter, size):
        """
        Dibuja el valor numérico de la temperatura.
        
        Args:
            painter (QPainter): Objeto pintor
            size (float): Tamaño de referencia
        """
        font = QFont()
        font.setPointSize(20)  # Reducido de 26 a 20
        font.setBold(True)
        painter.setFont(font)
        
        # Determinar el color según la temperatura
        color = self._get_temperature_color()
        
        painter.setPen(color)
        
        # Dibujar el valor DEBAJO del termómetro
        text = f"{self.value:.1f} °C"
        
        # Rectángulo para el texto en la parte inferior
        rect = QRect(-int(size/2), int(size * 0.4), int(size), int(size * 0.2))
        
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text) 