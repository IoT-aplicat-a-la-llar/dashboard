"""
Widget personalizado para mostrar la humedad con un diseño moderno
que incluye una ventana que se empaña según el nivel de humedad y una barra lateral de porcentaje.
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QFont, QLinearGradient, QRadialGradient
from PyQt6.QtCore import Qt, QRect, QRectF, QTimer, QPointF
import random
import math

class HumidityWidget(QWidget):
    def __init__(self, min_value=0, max_value=100, parent=None):
        super().__init__(parent)
        
        # Valores por defecto
        self.value = 50.0
        self.min_value = min_value
        self.max_value = max_value
        self.unit = "%"
        
        # Colores actualizados con paleta moderna y coherente
        self.blue_color = QColor("#3498db")      # Azul principal
        self.light_blue = QColor("#85c1e9")      # Azul claro para gradientes
        self.dark_blue = QColor("#2980b9")       # Azul oscuro para sombras
        self.text_color = QColor("#FFFFFF")      # Blanco para texto
        self.bg_color = QColor(26, 26, 26, 0)    # Fondo transparente
        self.accent_color = QColor("#3498db")    # Azul como color de acento
        
        # Puntos de empañamiento
        self.fog_points = []
        self._generate_fog_points()
        
        # Timer para la animación
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)  # Actualizar cada 50ms
        
        # Tamaño mínimo
        self.setMinimumSize(180, 180)
    
    def _generate_fog_points(self):
        """Genera las zonas de empañamiento orgánicas según el valor de humedad."""
        # Limpiar puntos existentes
        self.fog_points = []
        
        # Calcular número de zonas basado en el valor de humedad normalizado
        normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        zone_count = int(40 + normalized_value * 100)  # Entre 40 y 140 zonas según humedad
        
        # Generar zonas con formas orgánicas aleatorias
        for _ in range(zone_count):
            # Posición aleatoria (evitando los bordes y la barra de porcentaje)
            x = random.uniform(0.05, 0.75)
            y = random.uniform(0.05, 0.95)
            
            # Tamaño base para la forma orgánica
            base_size = random.uniform(0.02, 0.05 + normalized_value * 0.05)
            
            # Crear puntos para forma orgánica (de 4 a 8 puntos)
            vertices = random.randint(4, 8)
            points = []
            
            # Generar puntos alrededor de un círculo con variaciones aleatorias
            for i in range(vertices):
                angle = 2 * math.pi * i / vertices
                # Variar el radio para crear forma orgánica
                radius_var = random.uniform(0.7, 1.3) * base_size
                px = x + radius_var * math.cos(angle)
                py = y + radius_var * math.sin(angle)
                points.append((px, py))
            
            # Opacidad basada en la humedad
            opacity = random.uniform(0.2, 0.6) * normalized_value
            
            # Añadir zona orgánica
            self.fog_points.append({
                'x': x,
                'y': y,
                'points': points,
                'opacity': opacity,
            })
    
    def update_animation(self):
        """Actualiza la animación del empañamiento."""
        # Regenerar algunas zonas para dar efecto dinámico
        if random.random() < 0.1:  # 10% de probabilidad de actualizar algunas zonas
            normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
            for i in range(int(len(self.fog_points) * 0.05)):  # Actualizar 5% de las zonas
                if len(self.fog_points) > 0:
                    idx = random.randint(0, len(self.fog_points) - 1)
                    x = random.uniform(0.05, 0.75)
                    y = random.uniform(0.05, 0.95)
                    
                    # Tamaño base para la forma orgánica
                    base_size = random.uniform(0.02, 0.05 + normalized_value * 0.05)
                    
                    # Crear puntos para forma orgánica (de 4 a 8 puntos)
                    vertices = random.randint(4, 8)
                    points = []
                    
                    # Generar puntos alrededor de un círculo con variaciones aleatorias
                    for j in range(vertices):
                        angle = 2 * math.pi * j / vertices
                        # Variar el radio para crear forma orgánica
                        radius_var = random.uniform(0.7, 1.3) * base_size
                        px = x + radius_var * math.cos(angle)
                        py = y + radius_var * math.sin(angle)
                        points.append((px, py))
                    
                    self.fog_points[idx]['x'] = x
                    self.fog_points[idx]['y'] = y
                    self.fog_points[idx]['points'] = points
                    self.fog_points[idx]['opacity'] = random.uniform(0.2, 0.6) * normalized_value
        
        # Actualizar el widget
        self.update()
    
    def set_value(self, value):
        """Establece el valor de humedad."""
        prev_value = self.value
        self.value = max(self.min_value, min(value, self.max_value))
        
        # Regenerar los puntos con cada cambio significativo
        if abs(prev_value - self.value) > 5:
            self._generate_fog_points()
        
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el widget de humedad."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dimensiones
        width = self.width()
        height = self.height()
        
        # Limpiar el fondo
        painter.fillRect(0, 0, width, height, self.bg_color)
        
        # Dibujar la ventana
        self._draw_window(painter, width, height)
        
        # Dibujar el empañamiento
        self._draw_fogging(painter, width, height)
        
        # Dibujar la barra de porcentajes
        self._draw_percentage_bar(painter, width, height)
        
        # Dibujar valor central
        self._draw_central_value(painter, width, height)
    
    def _draw_window(self, painter, width, height):
        """Dibuja la ventana base."""
        # Dimensiones de la ventana
        margin = width * 0.07
        window_width = width * 0.75
        window_height = height - 2 * margin
        window_x = margin
        window_y = margin
        
        # Marco de la ventana
        frame_color = QColor(100, 100, 115)
        painter.setPen(QPen(frame_color, 3))
        painter.setBrush(QColor(20, 25, 35, 220))  # Color más oscuro para el vidrio para mejor contraste
        window_rect = QRectF(window_x, window_y, window_width, window_height)
        painter.drawRoundedRect(window_rect, 5, 5)
        
        # Reflejo en el vidrio
        highlight_path = QPainterPath()
        highlight_path.addRoundedRect(
            QRectF(window_x + 5, window_y + 5, window_width - 10, 15), 
            2, 2
        )
        
        highlight_gradient = QLinearGradient(
            window_x + 5, window_y + 5, 
            window_x + 5, window_y + 20
        )
        highlight_gradient.setColorAt(0, QColor(255, 255, 255, 80))
        highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(highlight_gradient)
        painter.drawPath(highlight_path)
    
    def _draw_fogging(self, painter, width, height):
        """Dibuja el efecto de empañamiento en la ventana."""
        # Área segura para dibujar (dentro de la ventana)
        margin = width * 0.07
        window_width = width * 0.75
        window_height = height - 2 * margin
        window_x = margin
        window_y = margin
        
        # Crear una capa de empañamiento general
        normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        
        # Dibujar una capa semi-transparente para simular empañamiento general
        fog_opacity = min(180, int(normalized_value * 200))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(220, 230, 250, fog_opacity))  # Color más claro y brillante
        
        fog_rect = QRectF(window_x + 2, window_y + 2, window_width - 4, window_height - 4)
        painter.drawRoundedRect(fog_rect, 3, 3)
        
        # Dibujar zonas de empañamiento orgánicas
        for point in self.fog_points:
            # Determinar opacidad según nivel de humedad
            fog_color = QColor(255, 255, 255, int(255 * point['opacity']))  # Blanco puro para gotas
            
            # Dibujar forma orgánica de empañamiento
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(fog_color)
            
            # Crear camino para forma orgánica
            path = QPainterPath()
            points = point['points']
            
            if len(points) > 0:
                # Calcular coordenadas reales para los puntos
                real_points = []
                for px, py in points:
                    real_x = window_x + px * window_width
                    real_y = window_y + py * window_height
                    real_points.append((real_x, real_y))
                
                # Iniciar el camino
                path.moveTo(QPointF(real_points[0][0], real_points[0][1]))
                
                # Añadir puntos usando curvas bezier para suavizar
                for i in range(1, len(real_points)):
                    # Punto actual
                    curr = real_points[i]
                    # Punto anterior
                    prev = real_points[i-1]
                    
                    # Punto control 1 (cerca del punto anterior)
                    cp1_x = prev[0] + (curr[0] - prev[0]) * 0.5
                    cp1_y = prev[1]
                    
                    # Punto control 2 (cerca del punto actual)
                    cp2_x = curr[0] - (curr[0] - prev[0]) * 0.5
                    cp2_y = curr[1]
                    
                    # Añadir curva
                    path.cubicTo(
                        QPointF(cp1_x, cp1_y),
                        QPointF(cp2_x, cp2_y),
                        QPointF(curr[0], curr[1])
                    )
                
                # Cerrar la forma
                last = real_points[-1]
                first = real_points[0]
                
                cp1_x = last[0] + (first[0] - last[0]) * 0.5
                cp1_y = last[1]
                
                cp2_x = first[0] - (first[0] - last[0]) * 0.5
                cp2_y = first[1]
                
                path.cubicTo(
                    QPointF(cp1_x, cp1_y),
                    QPointF(cp2_x, cp2_y),
                    QPointF(first[0], first[1])
                )
                
                # Dibujar la forma
                painter.drawPath(path)
    
    def _draw_percentage_bar(self, painter, width, height):
        """Dibuja la barra de porcentaje a la derecha."""
        # Definir dimensiones de la barra
        margin = width * 0.07
        bar_width = width * 0.06
        bar_height = height - 2 * margin
        bar_x = width - margin - bar_width
        bar_y = margin
        
        # Escala de color con degradado moderno
        bar_gradient = QLinearGradient(bar_x, bar_y + bar_height, bar_x, bar_y)
        bar_gradient.setColorAt(0.0, QColor(200, 240, 255, 50))   # Muy seco (casi transparente)
        bar_gradient.setColorAt(0.3, QColor(150, 210, 255, 120))  # Seco 
        bar_gradient.setColorAt(0.6, QColor(100, 180, 255, 170))  # Normal
        bar_gradient.setColorAt(0.8, QColor(60, 150, 255, 210))   # Húmedo
        bar_gradient.setColorAt(1.0, QColor(30, 120, 255, 255))   # Muy húmedo
        
        # Contenedor de la barra con borde sutil
        painter.setBrush(QColor(40, 40, 50, 20))
        painter.setPen(QPen(QColor(100, 100, 120, 30), 1))
        bar_container = QRectF(bar_x-1, bar_y-1, bar_width+2, bar_height+2)
        painter.drawRoundedRect(bar_container, 4, 4)
        
        # Barra con bordes redondeados
        painter.setBrush(bar_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        bar_rect = QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRoundedRect(bar_rect, 3, 3)
        
        # Definir niveles de porcentaje
        levels = [(0.2, "20%"), (0.4, "40%"), (0.6, "60%"), (0.8, "80%")]
        
        # Configurar fuente
        percent_font = QFont()
        percent_font.setPointSize(11)  # Aumentado de 9 a 11
        percent_font.setBold(True)
        painter.setFont(percent_font)
        
        for level, text in levels:
            y = bar_y + bar_height * (1 - level)
            
            # Dibujar línea con estilo minimalista
            painter.setPen(QPen(QColor(255, 255, 255, 190), 1))
            painter.drawLine(
                int(bar_x - 3), 
                int(y),
                int(bar_x), 
                int(y)
            )
            
            # Fondo para el texto para mejor contraste
            text_rect = QRectF(bar_x - 30, y - 9, 27, 18)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(0, 0, 0, 200))  # Negro más oscuro para mejor contraste
            painter.drawRoundedRect(text_rect, 3, 3)
            
            # Dibujar texto de porcentaje
            painter.setPen(QColor(255, 255, 255, 255))  # Texto completamente blanco para mejor contraste
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, text)
        
        # Añadir marcas de 0% y 100%
        # Fondo para 0%
        text_rect_0 = QRectF(bar_x - 30, bar_y + bar_height - 9, 27, 18)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 200))  # Negro más oscuro para mejor contraste
        painter.drawRoundedRect(text_rect_0, 3, 3)
        
        # Fondo para 100%
        text_rect_100 = QRectF(bar_x - 30, bar_y - 9, 27, 18)
        painter.drawRoundedRect(text_rect_100, 3, 3)
        
        # Texto de 0% y 100%
        painter.setPen(QColor(255, 255, 255, 255))
        painter.drawText(
            text_rect_0,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, 
            "0%"
        )
        painter.drawText(
            text_rect_100,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, 
            "100%"
        )
        
        # Indicador de nivel actual
        normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        current_y = bar_y + bar_height * (1 - normalized_value)
        
        # Usar color rojo para el indicador con mayor grosor para mejorar visibilidad
        red_color = QColor(230, 60, 60, 255)  # Rojo intenso
        painter.setPen(QPen(red_color, 3))  # Línea más gruesa (3px)
        
        # Dibujar línea indicadora más ancha
        painter.drawLine(
            int(bar_x - 5), 
            int(current_y), 
            int(bar_x + bar_width + 5), 
            int(current_y)
        )
        
        # Dibujar círculo en el extremo para mejor visibilidad
        painter.setBrush(red_color)
        painter.drawEllipse(
            int(bar_x + bar_width + 5) - 4,
            int(current_y) - 4,
            8, 8
        )
    
    def _draw_central_value(self, painter, width, height):
        """Dibuja el valor de humedad centrado en la ventana."""
        # Dimensiones de la ventana
        margin = width * 0.07
        window_width = width * 0.75
        window_height = height - 2 * margin
        window_x = margin
        window_y = margin
        
        # Calcular centro de la ventana
        center_x = window_x + window_width / 2
        center_y = window_y + window_height / 2
        
        # Determinar color según nivel de humedad
        normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        
        if normalized_value < 0.3:
            main_color = QColor("#3498db")  # Azul para seco
        elif normalized_value < 0.6:
            main_color = QColor("#2ecc71")  # Verde para normal
        else:
            main_color = QColor("#3498db")  # Azul para húmedo
        
        # Dibujar texto del valor
        value_text = f"{self.value:.1f}{self.unit}"
        
        # Configurar fuente
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        painter.setFont(value_font)
        
        # Crear un fondo negro más pequeño
        bg_rect = QRectF(
            center_x - 60,  # Reducido de 80 a 60
            center_y - 20,  # Mantenido
            120,  # Reducido de 160 a 120
            40   # Mantenido
        )
        
        # Dibujar fondo con color sólido para mejor contraste
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 200))
        painter.drawRoundedRect(bg_rect, 10, 10)
        
        # Dibujar contorno sutil para mejor definición
        painter.setPen(QPen(QColor(255, 255, 255, 40), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(bg_rect, 10, 10)
        
        # Dibujar texto principal con color más brillante dentro del rectángulo
        painter.setPen(QColor(255, 255, 255, 255))
        painter.drawText(bg_rect, Qt.AlignmentFlag.AlignCenter, value_text)
    
    def _draw_graph(self, painter, width, height):
        """Dibuja la gráfica de humedad."""
        # Configurar el panel de la gráfica
        margin = width * 0.07  # Aumentar el margen para dar más espacio a los números
        panel_width = width - (margin * 2)
        panel_height = height - (margin * 2)
        panel_x = margin
        panel_y = margin
        
        # Dibujar fondo del panel
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(45, 45, 45)))
        painter.drawRoundedRect(panel_x, panel_y, panel_width, panel_height, 5, 5)
        
        # Dibujar líneas de la cuadrícula
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        
        # Líneas horizontales
        for i in range(4):
            y = panel_y + (panel_height * (i + 1) / 5)
            painter.drawLine(panel_x, y, panel_x + panel_width, y)
        
        # Dibujar puntos y líneas de la gráfica
        if len(self.values) > 1:
            # Calcular puntos
            points = []
            for i, value in enumerate(self.values):
                x = panel_x + (i * panel_width / (len(self.values) - 1))
                y = panel_y + panel_height - ((value - self.min_value) / (self.max_value - self.min_value) * panel_height)
                points.append(QPointF(x, y))
            
            # Dibujar líneas
            painter.setPen(QPen(QColor(52, 152, 219), 2))
            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i + 1])
            
            # Dibujar puntos
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(52, 152, 219)))
            for point in points:
                painter.drawEllipse(point, 3, 3)
        
        # Dibujar números del eje Y
        painter.setPen(QPen(QColor(200, 200, 200)))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        
        # Ajustar la posición de los números para que no se corten
        text_x = panel_x - 60  # Aumentar el espacio a la izquierda
        text_width = 50  # Aumentar el ancho del área de texto
        
        for i in range(5):
            value = self.max_value - (i * (self.max_value - self.min_value) / 4)
            y = panel_y + (i * panel_height / 4)
            
            # Dibujar fondo negro para los números
            text = f"{int(value)}%"
            text_rect = painter.fontMetrics().boundingRect(text)
            text_x_pos = text_x - (text_width / 2)  # Centrar el texto en el área asignada
            text_y_pos = y + (text_rect.height() / 4)  # Ajustar la posición vertical
            
            # Dibujar el fondo negro
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawRect(text_x_pos - 5, text_y_pos - text_rect.height(), text_width, text_rect.height() + 5)
            
            # Dibujar el texto
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawText(text_x_pos, text_y_pos, text) 