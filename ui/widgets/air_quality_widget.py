"""
Widget personalizado para mostrar la calidad del aire.
"""
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QFont, QLinearGradient
from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer

class AirQualityWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuración inicial
        self.setMinimumSize(200, 200)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        
        # Valores iniciales
        self.value = 0
        self.min_value = 0
        self.max_value = 500
        self.title = "Calidad del Aire"
        
        # Colores para diferentes estados
        self.colors = {
            "excelente": QColor("#2ecc71"),  # Verde
            "buena": QColor("#3498db"),      # Azul
            "moderada": QColor("#f39c12"),   # Naranja
            "mala": QColor("#e74c3c"),       # Rojo
            "peligrosa": QColor("#8e44ad")   # Morado
        }
        
        # Efecto de animación
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update)
        self.animation_timer.start(50)  # Aumentar la velocidad de actualización
        
        # Partículas para la animación
        self.particles = []
        self.init_particles()
        
    def init_particles(self):
        """Inicializa las partículas para la animación."""
        import random
        for _ in range(30):  # Aumentar el número inicial de partículas
            self.particles.append({
                'x': random.uniform(0, 1),
                'y': random.uniform(0, 1),
                'size': random.uniform(2, 6),  # Reducir tamaño máximo
                'speed': random.uniform(0.002, 0.006),  # Aumentar velocidad
                'opacity': random.uniform(0.3, 0.7)  # Ajustar opacidad
            })
        
    def set_value(self, value):
        """Establece el valor actual."""
        self.value = max(self.min_value, min(self.max_value, value))
        self.update()
        
    def set_range(self, min_value, max_value):
        """Establece el rango de valores."""
        self.min_value = min_value
        self.max_value = max_value
        self.update()
        
    def get_color(self):
        """Obtiene el color basado en el valor actual."""
        if self.value < 50:
            return self.colors["excelente"]
        elif self.value < 100:
            return self.colors["buena"]
        elif self.value < 150:
            return self.colors["moderada"]
        elif self.value < 300:
            return self.colors["mala"]
        else:
            return self.colors["peligrosa"]
        
    def get_state(self):
        """Obtiene el estado actual basado en el valor."""
        if self.value < 50:
            return "Excelente"
        elif self.value < 100:
            return "Buena"
        elif self.value < 150:
            return "Moderada"
        elif self.value < 300:
            return "Mala"
        else:
            return "Peligrosa"
        
    def paintEvent(self, event):
        """Dibuja el widget."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Obtener dimensiones
        width = self.width()
        height = self.height()
        
        # Dibujar fondo
        self._draw_background(painter, width, height)
        
        # Dibujar partículas
        self._update_and_draw_particles(painter, width, height)
        
        # Dibujar barra de progreso
        self._draw_progress_bar(painter, width, height)
        
        # Dibujar texto
        self._draw_text(painter, width, height)
        
        painter.end()
        
    def _draw_background(self, painter, width, height):
        """Dibuja el fondo del widget."""
        # Fondo completamente transparente
        painter.fillRect(0, 0, width, height, QColor(0, 0, 0, 0))
        
    def _update_and_draw_particles(self, painter, width, height):
        """Actualiza y dibuja las partículas animadas."""
        import random
        
        current_color = self.get_color()
        alpha = int(min(255, 120 + (self.value / self.max_value) * 135))
        
        # Niveles de densidad de partículas basado en el valor
        particle_count = int(max(15, min(50, (self.value / self.max_value) * 50)))
        
        # Definir área de partículas (centrada horizontalmente, 65% de altura en el centro)
        particle_area_width = width * 0.8
        particle_area_height = height * 0.65
        particle_area_x = (width - particle_area_width) / 2
        particle_area_y = height * 0.175  # Centrado verticalmente
        
        # Añadir más partículas si es necesario
        while len(self.particles) < particle_count:
            self.particles.append({
                'x': random.uniform(0, 1),
                'y': 1.0,  # Comienza desde abajo
                'size': random.uniform(2, 6),  # Tamaños más pequeños para mayor fluidez
                'speed': random.uniform(0.002, 0.006),  # Mayor velocidad
                'opacity': random.uniform(0.3, 0.7)  # Opacidad más consistente
            })
            
        # Limitar el número de partículas
        self.particles = self.particles[:particle_count]
            
        for p in self.particles:
            # Mover partículas hacia arriba con delta más pequeño
            p['y'] -= p['speed']
            
            # Añadir movimiento horizontal suave
            p['x'] += random.uniform(-0.002, 0.002)
            p['x'] = max(0, min(1, p['x']))  # Mantener dentro de los límites
            
            # Si la partícula sale de la pantalla, reiniciarla
            if p['y'] < 0:
                p['y'] = 1.0
                p['x'] = random.uniform(0, 1)
                p['size'] = random.uniform(2, 6)
                
            # Dibujar partícula (aplicar el área definida)
            x = int(particle_area_x + (p['x'] * particle_area_width))
            y = int(particle_area_y + (p['y'] * particle_area_height))
            size = int(p['size'])
            
            particle_color = QColor(current_color)
            particle_color.setAlpha(int(p['opacity'] * alpha))
            
            painter.setBrush(QBrush(particle_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x, y, size, size)
            
    def _draw_progress_bar(self, painter, width, height):
        """Dibuja la barra de progreso de calidad del aire."""
        # Centrar y ajustar tamaño
        bar_width = width * 0.8
        bar_height = height * 0.08
        bar_x = (width - bar_width) / 2
        bar_y = height * 0.65  # Posición en espejo respecto al valor
        
        # Fondo de la barra
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(
            QRectF(bar_x, bar_y, bar_width, bar_height),
            bar_height/2, bar_height/2
        )
        
        # Progreso
        progress_width = (self.value / self.max_value) * bar_width
        
        # Gradiente para la barra de progreso
        gradient = QLinearGradient(0, 0, width, 0)
        gradient.setColorAt(0, self.colors["excelente"])
        gradient.setColorAt(0.2, self.colors["buena"])
        gradient.setColorAt(0.4, self.colors["moderada"])
        gradient.setColorAt(0.7, self.colors["mala"])
        gradient.setColorAt(1.0, self.colors["peligrosa"])
        
        painter.setBrush(QBrush(gradient))
        painter.drawRoundedRect(
            QRectF(bar_x, bar_y, progress_width, bar_height), 
            bar_height/2, bar_height/2
        )
        
        # Marcadores de nivel
        pen = QPen(QColor(200, 200, 200))
        pen.setWidth(1)
        painter.setPen(pen)
        
        levels = [50, 100, 150, 300]  # Umbrales de calidad
        for level in levels:
            level_x = bar_x + (level / self.max_value) * bar_width
            painter.drawLine(
                int(level_x), int(bar_y - 5),
                int(level_x), int(bar_y + bar_height + 5)
            )
            
    def _draw_text(self, painter, width, height):
        """Dibuja el texto del widget."""
        # Valor actual - Colocar en posición espejo respecto a la barra
        value_font = QFont()
        value_font.setPointSize(34)
        value_font.setBold(True)
        painter.setFont(value_font)
        
        # Color basado en el estado
        painter.setPen(self.get_color())
        
        # Posicionar el valor a la misma distancia del centro que la barra pero arriba
        value_rect = QRectF(0, height * 0.20, width, 50)  # Movido más arriba
        painter.drawText(value_rect, Qt.AlignmentFlag.AlignCenter, f"{int(self.value)}")
        
        # Unidad - Justo debajo del valor
        unit_font = QFont()
        unit_font.setPointSize(20)
        painter.setFont(unit_font)
        painter.setPen(QColor(200, 200, 200))
        
        unit_rect = QRectF(0, height * 0.20 + 45, width, 30)  # Ajustado para seguir al valor
        painter.drawText(unit_rect, Qt.AlignmentFlag.AlignCenter, "IAQ")