"""
Widget personalizado para mostrar el nivel de ruido con un diseño de ecualizador
que visualiza el nivel de ruido a través de barras verticales y una barra lateral de intensidad.
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QFont, QLinearGradient
from PyQt6.QtCore import Qt, QRect, QRectF, QTimer, QPointF
import random
import math

class NoiseWidget(QWidget):
    def __init__(self, min_value=30, max_value=90, parent=None):
        super().__init__(parent)
        
        # Valores por defecto
        self.value = 50.0
        self.min_value = min_value
        self.max_value = max_value
        self.unit = "dB"
        
        # Colores con paleta moderna y coherente
        self.yellow_color = QColor("#f1c40f")    # Amarillo principal
        self.light_yellow = QColor("#f7dc6f")    # Amarillo claro para gradientes
        self.orange_color = QColor("#f39c12")    # Naranja para niveles medios
        self.red_color = QColor("#e74c3c")       # Rojo para niveles altos
        self.text_color = QColor("#FFFFFF")      # Blanco para texto
        self.bg_color = QColor(26, 26, 26, 0)    # Fondo transparente
        self.accent_color = QColor("#f1c40f")    # Amarillo como color de acento
        
        # Barras del ecualizador
        self.bars = []
        self.num_bars = 15  # Número de barras en el ecualizador
        self._generate_bars()
        
        # Timer para la animación
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)  # Actualizar cada 50ms
        
        # Tamaño mínimo
        self.setMinimumSize(180, 180)
    
    def _generate_bars(self):
        """Genera las barras del ecualizador según el nivel de ruido."""
        # Limpiar barras existentes
        self.bars = []
        
        # Calcular altura base para las barras basada en el valor de ruido normalizado
        normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        base_height = 0.2 + normalized_value * 0.6  # Entre 0.2 y 0.8 de altura máxima
        
        # Generar barras con diferentes alturas
        for i in range(self.num_bars):
            # Variación aleatoria sobre la altura base
            height_var = random.uniform(-0.15, 0.15)
            if i < 2 or i > self.num_bars - 3:  # Barras de los extremos más bajas
                height_var -= 0.2
            elif i > 4 and i < self.num_bars - 5:  # Barras centrales más altas
                height_var += 0.1
                
            # Altura final con restricciones
            height = max(0.05, min(0.95, base_height + height_var))
            
            # Ancho de la barra (fijo)
            width = 1.0 / (self.num_bars * 2)
            
            # Calcular color según nivel de ruido
            if self.value < 60:  # Nivel bajo
                bar_color = self.yellow_color
            elif self.value < 80:  # Nivel medio
                bar_color = self.orange_color
            else:  # Nivel alto
                bar_color = self.red_color
            
            # Añadir efecto de brillo según posición
            brightness = 100 + int(abs(i - self.num_bars/2) * 5)
            adjusted_color = bar_color.lighter(brightness)
            
            # Velocidad de cambio en la animación
            animation_speed = random.uniform(0.01, 0.05)
            
            # Añadir barra
            self.bars.append({
                'height': height,
                'width': width,
                'color': adjusted_color,
                'target_height': height,
                'animation_speed': animation_speed
            })
    
    def update_animation(self):
        """Actualiza la animación de las barras del ecualizador."""
        normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        
        # Actualizar cada barra
        for bar in self.bars:
            # Calcular nueva altura objetivo con variación aleatoria
            height_var = random.uniform(-0.15, 0.15)
            base_height = 0.2 + normalized_value * 0.6
            new_target = max(0.05, min(0.95, base_height + height_var))
            
            # Actualizar altura objetivo
            bar['target_height'] = new_target
            
            # Mover suavemente hacia la altura objetivo
            diff = bar['target_height'] - bar['height']
            bar['height'] += diff * bar['animation_speed']
        
        # Actualizar el widget
        self.update()
    
    def set_value(self, value):
        """Establece el valor de nivel de ruido."""
        prev_value = self.value
        self.value = max(self.min_value, min(value, self.max_value))
        
        # Regenerar las barras con cada cambio significativo
        if abs(prev_value - self.value) > 5:
            self._generate_bars()
        
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el widget de nivel de ruido."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dimensiones
        width = self.width()
        height = self.height()
        
        # Limpiar el fondo
        painter.fillRect(0, 0, width, height, self.bg_color)
        
        # Dibujar el panel oscuro para el ecualizador
        self._draw_panel(painter, width, height)
        
        # Dibujar barras del ecualizador
        self._draw_bars(painter, width, height)
        
        # Dibujar la barra de intensidad
        self._draw_intensity_bar(painter, width, height)
        
        # Dibujar valor central
        self._draw_central_value(painter, width, height)
    
    def _draw_panel(self, painter, width, height):
        """Dibuja el panel para el ecualizador."""
        # Dimensiones del panel
        margin = width * 0.07
        panel_width = width * 0.75
        panel_height = height - 2 * margin
        panel_x = margin
        panel_y = margin
        
        # Marco del panel
        frame_color = QColor(100, 100, 115)
        painter.setPen(QPen(frame_color, 3))
        painter.setBrush(QColor(20, 22, 26, 220))  # Color más oscuro para resaltar las barras
        panel_rect = QRectF(panel_x, panel_y, panel_width, panel_height)
        painter.drawRoundedRect(panel_rect, 5, 5)
        
        # Reflejo en el panel
        highlight_path = QPainterPath()
        highlight_path.addRoundedRect(
            QRectF(panel_x + 5, panel_y + 5, panel_width - 10, 15), 
            2, 2
        )
        
        highlight_gradient = QLinearGradient(
            panel_x + 5, panel_y + 5, 
            panel_x + 5, panel_y + 20
        )
        highlight_gradient.setColorAt(0, QColor(255, 255, 255, 60))
        highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(highlight_gradient)
        painter.drawPath(highlight_path)
        
        # Dibujar líneas horizontales de referencia (estilo ecualizador)
        painter.setPen(QPen(QColor(100, 100, 115, 40), 1, Qt.PenStyle.DotLine))
        
        # Líneas de referencia a diferentes alturas
        ref_lines = [0.25, 0.5, 0.75]
        for ref in ref_lines:
            y = panel_y + panel_height * (1 - ref)
            painter.drawLine(
                QPointF(panel_x + 5, y),
                QPointF(panel_x + panel_width - 5, y)
            )
    
    def _draw_bars(self, painter, width, height):
        """Dibuja las barras del ecualizador."""
        # Área segura para dibujar (dentro del panel)
        margin = width * 0.07
        panel_width = width * 0.75
        panel_height = height - 2 * margin
        panel_x = margin
        panel_y = margin
        
        # Área efectiva para las barras (con margen interno)
        bars_area_x = panel_x + panel_width * 0.05
        bars_area_y = panel_y + panel_height * 0.05
        bars_area_width = panel_width * 0.9
        bars_area_height = panel_height * 0.9
        
        # Espacio entre barras (20% del ancho disponible por barra)
        spacing = 0.2
        
        # Ancho efectivo por barra incluyendo espaciado
        total_width_per_bar = bars_area_width / self.num_bars
        bar_width = total_width_per_bar * (1 - spacing)
        
        # Dibujar cada barra
        for i, bar in enumerate(self.bars):
            # Calcular posición X
            x = bars_area_x + i * total_width_per_bar
            
            # Calcular altura y posición Y
            bar_height = bar['height'] * bars_area_height
            y = bars_area_y + bars_area_height - bar_height
            
            # Crear degradado vertical para la barra
            gradient = QLinearGradient(
                x, y, 
                x, y + bar_height
            )
            
            # Determinar color según nivel de ruido
            if self.value < 60:  # Nivel bajo
                top_color = self.yellow_color.lighter(130)
                bottom_color = self.yellow_color.darker(110)
            elif self.value < 80:  # Nivel medio
                top_color = self.orange_color.lighter(130)
                bottom_color = self.orange_color.darker(110)
            else:  # Nivel alto
                top_color = self.red_color.lighter(130)
                bottom_color = self.red_color.darker(110)
            
            # Configurar degradado
            gradient.setColorAt(0, top_color)
            gradient.setColorAt(1, bottom_color)
            
            # Dibujar barra con degradado
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(gradient)
            
            # Rectángulo de la barra con esquinas redondeadas
            bar_rect = QRectF(x, y, bar_width, bar_height)
            painter.drawRoundedRect(bar_rect, 2, 2)
            
            # Añadir brillo en la parte superior
            highlight_height = min(bar_height * 0.15, 3)
            if highlight_height > 1:
                highlight_rect = QRectF(x, y, bar_width, highlight_height)
                highlight_gradient = QLinearGradient(
                    x, y,
                    x, y + highlight_height
                )
                highlight_gradient.setColorAt(0, QColor(255, 255, 255, 180))
                highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
                
                painter.setBrush(highlight_gradient)
                painter.drawRoundedRect(highlight_rect, 2, 2)
    
    def _draw_intensity_bar(self, painter, width, height):
        """Dibuja la barra de intensidad a la derecha."""
        # Definir dimensiones de la barra
        margin = width * 0.07
        bar_width = width * 0.06
        bar_height = height - 2 * margin
        bar_x = width - margin - bar_width
        bar_y = margin
        
        # Escala de color con degradado según intensidad
        self.bar_gradient = QLinearGradient(bar_x, bar_y + bar_height, bar_x, bar_y)
        self.bar_gradient.setColorAt(0.0, QColor(241, 196, 15, 50))   # Amarillo claro (silencio)
        self.bar_gradient.setColorAt(0.3, QColor(241, 196, 15, 150))  # Amarillo (bajo)
        self.bar_gradient.setColorAt(0.6, QColor(243, 156, 18, 200))  # Naranja (medio)
        self.bar_gradient.setColorAt(0.8, QColor(230, 126, 34, 230))  # Naranja intenso (alto)
        self.bar_gradient.setColorAt(1.0, QColor(231, 76, 60, 255))   # Rojo (muy alto)
        
        # Contenedor de la barra con borde sutil
        painter.setBrush(QColor(40, 40, 50, 20))
        painter.setPen(QPen(QColor(100, 100, 120, 30), 1))
        bar_container = QRectF(bar_x-1, bar_y-1, bar_width+2, bar_height+2)
        painter.drawRoundedRect(bar_container, 4, 4)
        
        # Barra con bordes redondeados
        painter.setBrush(self.bar_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        bar_rect = QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRoundedRect(bar_rect, 3, 3)
        
        # Definir niveles de intensidad
        levels = [(0.2, "40dB"), (0.4, "55dB"), (0.6, "70dB"), (0.8, "85dB")]
        
        # Configurar fuente
        level_font = QFont()
        level_font.setPointSize(10)
        level_font.setBold(True)
        painter.setFont(level_font)
        
        for level, text in levels:
            y = bar_y + bar_height * (1 - level)
            
            # Dibujar línea con estilo minimalista
            painter.setPen(QPen(QColor(255, 255, 255, 150), 1))
            painter.drawLine(
                int(bar_x - 3), 
                int(y),
                int(bar_x), 
                int(y)
            )
            
            # Fondo para el texto para mejor contraste
            text_rect = QRectF(bar_x - 45, y - 9, 40, 18)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(0, 0, 0, 180))
            painter.drawRoundedRect(text_rect, 3, 3)
            
            # Dibujar texto de nivel
            painter.setPen(QColor(255, 255, 255, 240))
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, text)
        
        # Añadir marcas de mínimo y máximo con fondos
        # Fondo para valor mínimo
        min_rect = QRectF(bar_x - 45, bar_y + bar_height - 9, 40, 18)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 180))
        painter.drawRoundedRect(min_rect, 3, 3)
        
        # Fondo para valor máximo
        max_rect = QRectF(bar_x - 45, bar_y - 9, 40, 18)
        painter.drawRoundedRect(max_rect, 3, 3)
        
        # Textos de valores mínimo y máximo
        painter.setPen(QColor(255, 255, 255, 240))
        painter.drawText(
            min_rect, 
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, 
            f"{self.min_value}dB"
        )
        painter.drawText(
            max_rect, 
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, 
            f"{self.max_value}dB"
        )
        
        # Indicador de nivel actual
        normalized_value = 1 - (self.value - self.min_value) / (self.max_value - self.min_value)
        current_y = bar_y + bar_height * normalized_value
        
        # Determinar color según nivel
        if self.value < 60:
            indicator_color = self.yellow_color
        elif self.value < 80:
            indicator_color = self.orange_color
        else:
            indicator_color = self.red_color
            
        # Usar el color adecuado para el indicador
        painter.setPen(QPen(indicator_color, 2))
        painter.drawLine(
            int(bar_x - 5), 
            int(current_y), 
            int(bar_x + bar_width + 5),  # Extender la línea
            int(current_y)
        )
        
        # Dibujar círculo en el extremo para mejor visibilidad
        painter.setBrush(indicator_color)
        painter.drawEllipse(
            int(bar_x + bar_width + 5) - 4,
            int(current_y) - 4,
            8, 8
        )
    
    def _draw_central_value(self, painter, width, height):
        """Dibuja el valor del nivel de ruido centrado en la parte superior del panel."""
        # Dimensiones del panel
        margin = width * 0.07
        panel_width = width * 0.75
        panel_height = height - 2 * margin
        panel_x = margin
        panel_y = margin
        
        # Determinar color según nivel de ruido
        if self.value < 60:
            main_color = self.yellow_color  # Amarillo para nivel bajo
        elif self.value < 80:
            main_color = self.orange_color  # Naranja para nivel medio
        else:
            main_color = self.red_color     # Rojo para nivel alto
        
        # Dibujar texto del valor
        value_text = f"{self.value:.1f}{self.unit}"
        
        # Configurar fuente
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        painter.setFont(value_font)
        
        # Determinar la posición central del texto
        text_x = panel_x + panel_width / 2
        text_y = panel_y + panel_height * 0.15
        
        # Primero dibujar el fondo negro
        bg_rect = QRectF(
            text_x - 50,  # Reducido de 70 a 50
            text_y - 20,
            100,  # Reducido de 140 a 100
            40
        )
        
        # Dibujar fondo con color sólido para mejor contraste
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 200))  # Negro con mayor opacidad
        painter.drawRoundedRect(bg_rect, 10, 10)
        
        # Dibujar el texto centrado sobre el fondo
        painter.setPen(self.text_color)
        painter.drawText(
            bg_rect,
            Qt.AlignmentFlag.AlignCenter,
            value_text
        ) 