"""
Ventana principal de la aplicación.
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QGridLayout, QMessageBox, QDialog, QTextEdit, QLineEdit
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QFont, QPainter, QBrush, QPen, QColor, QRadialGradient
from config import UI_CONFIG, SENSORS
from ui.widgets.thermometer_widget import ThermometerWidget
from ui.widgets.sensor_widget import SensorWidget
from ui.widgets.humidity_widget import HumidityWidget
from ui.widgets.pressure_widget import PressureWidget
from ui.widgets.air_quality_widget import AirQualityWidget
from ui.widgets.noise_widget import NoiseWidget
import random
import math

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.setWindowTitle("Monitor de Temperatura")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
            }
        """)
        
        # Configurar la ventana para pantalla completa sin barra de título
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # Sin marco de ventana
            Qt.WindowType.WindowStaysOnTopHint |  # Mantener siempre visible
            Qt.WindowType.Tool  # Evitar que aparezca en la barra de tareas
        )
        
        # Configurar el widget central para que se expanda
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central_widget)
        
        self.config = UI_CONFIG
        
        # Configurar UI
        self._setup_ui()
        
        # Timer para actualizar sensores
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sensor_values)
        self.timer.start(200)  # Ralentizar a 200ms para movimientos más suaves
        
        # Mostrar en pantalla completa después de configurar todo
        self.showFullScreen()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        # Crear widget central
        central_widget = self.centralWidget()
        central_widget.setStyleSheet("background-color: #1a1a1a;")
        
        # Crear layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)  # Reducir aún más el espaciado
        main_layout.setContentsMargins(5, 5, 5, 5)  # Reducir aún más los márgenes
        
        # Layout para el botón de salir
        top_layout = QHBoxLayout()
        
        # Espacio vacío a la izquierda
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Botón de salida
        exit_button = QPushButton("X")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_button.setFixedSize(25, 25)  # Reducir aún más el tamaño del botón
        exit_button.clicked.connect(self.close)
        
        top_layout.addWidget(spacer)
        top_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        main_layout.addLayout(top_layout)
        
        # Usar un grid layout para toda la interfaz (2x3)
        content_grid = QGridLayout()
        content_grid.setSpacing(5)  # Reducir aún más el espaciado entre widgets
        
        # Definir tamaños mínimos para hacer todas las celdas iguales
        for col in range(3):
            content_grid.setColumnMinimumWidth(col, 260)  # Ajustar para 800px de ancho
        for row in range(2):
            content_grid.setRowMinimumHeight(row, 220)  # Ajustar para 480px de alto
        
        # Configurar el grid para que se expanda
        content_grid.setColumnStretch(0, 1)
        content_grid.setColumnStretch(1, 1)
        content_grid.setColumnStretch(2, 1)
        content_grid.setRowStretch(0, 1)
        content_grid.setRowStretch(1, 1)
        
        # Definir estilos comunes para todos los widgets
        title_style = """
            color: #3498db;
            font-size: 16px;
            font-weight: bold;
            background-color: transparent;
            padding: 1px;
        """
        
        status_style = """
            color: white;
            font-size: 14px;
            font-weight: bold;
            background-color: transparent;
            padding: 1px;
        """
        
        # Definir estilos y configuraciones comunes para contenedores
        container_style = """
            QWidget {
                background-color: rgba(40, 40, 40, 0.7);
                border: none;
                border-radius: 8px;
            }
        """
        
        container_margins = 5  # Reducir aún más los márgenes
        container_spacing = 3  # Reducir aún más el espaciado
        
        # Contenedor para el termómetro (primera celda)
        thermometer_container = QWidget()
        thermometer_container.setStyleSheet(container_style)
        thermometer_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Layout para el termómetro
        thermometer_layout = QVBoxLayout(thermometer_container)
        thermometer_layout.setContentsMargins(container_margins, container_margins, container_margins, container_margins)
        thermometer_layout.setSpacing(container_spacing)
        
        # Título "Temperatura" en la parte superior
        temperature_title = QLabel("Temperatura")
        temperature_title.setStyleSheet(title_style)
        temperature_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Crear y configurar el termómetro
        self.thermometer = ThermometerWidget()
        self.thermometer.set_range(10, 40)
        self.thermometer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Estado en la parte inferior
        self.temperature_status = QLabel("Estado: Normal")
        self.temperature_status.setStyleSheet(status_style)
        self.temperature_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Añadir los elementos al layout en el orden correcto
        thermometer_layout.addWidget(temperature_title)
        thermometer_layout.addWidget(self.thermometer)
        thermometer_layout.addWidget(self.temperature_status)
        
        # Añadir el termómetro al grid
        content_grid.addWidget(thermometer_container, 0, 0)
        
        # Crear widgets de sensores
        self.sensor_widgets = {}
        
        # Almacenar las posiciones para cada widget
        positions = []
        
        # Posiciones base para grid 2x3
        for row in range(2):
            for col in range(3):
                if not (row == 0 and col == 0):  # Primera posición ya ocupada por el termómetro
                    positions.append((row, col))
        
        # Contador para los sensores
        sensor_count = 0
        
        # Crear el widget para la temperatura pero no mostrarlo (ya se muestra en el termómetro)
        # y usar un widget especial para la humedad
        for sensor_id, sensor_info in SENSORS.items():
            if sensor_id == "Temperatura":
                continue
            
            # Para humedad, usar el widget personalizado
            if sensor_id == "Humedad":
                # Crear contenedor individual para el sensor de humedad
                sensor_container = QWidget()
                sensor_container.setStyleSheet(container_style)
                
                # Layout para el sensor - con márgenes reducidos
                sensor_container_layout = QVBoxLayout(sensor_container)
                sensor_container_layout.setContentsMargins(container_margins, container_margins, container_margins, container_margins)
                sensor_container_layout.setSpacing(container_spacing)
                
                # Título "Humedad" en la parte superior
                humidity_title = QLabel("Humedad")
                humidity_title.setStyleSheet(title_style)
                humidity_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Añadir widget de humedad
                widget = HumidityWidget(
                    min_value=sensor_info['min_value'],
                    max_value=sensor_info['max_value'],
                    parent=self
                )
                
                # Guardar referencia
                self.sensor_widgets[sensor_id] = widget
                
                # Estado en la parte inferior
                self.humidity_status = QLabel("Estado: Normal")
                self.humidity_status.setStyleSheet(status_style)
                self.humidity_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Añadir los elementos al layout en el orden correcto
                sensor_container_layout.addWidget(humidity_title)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                sensor_container_layout.addWidget(widget)
                sensor_container_layout.addWidget(self.humidity_status)
                
                # Obtener la siguiente posición disponible
                if positions:
                    row, col = positions.pop(0)
                    content_grid.addWidget(sensor_container, row, col)
                
                # Actualizar contador
                sensor_count += 1
                
                continue
            
            # Para presión, usar el widget personalizado
            if sensor_id == "Presión":
                # Crear contenedor individual para el sensor de presión
                sensor_container = QWidget()
                sensor_container.setStyleSheet(container_style)
                
                # Layout para el sensor
                sensor_container_layout = QVBoxLayout(sensor_container)
                sensor_container_layout.setContentsMargins(container_margins, container_margins, container_margins, container_margins)
                sensor_container_layout.setSpacing(container_spacing)
                
                # Título "Presión" en la parte superior
                pressure_title = QLabel("Presión")
                pressure_title.setStyleSheet(title_style)
                pressure_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Añadir widget de presión
                widget = PressureWidget(
                    min_value=sensor_info['min_value'],
                    max_value=sensor_info['max_value'],
                    parent=self
                )
                
                # Guardar referencia
                self.sensor_widgets[sensor_id] = widget
                
                # Estado en la parte inferior
                self.pressure_status = QLabel("Estado: Normal")
                self.pressure_status.setStyleSheet(status_style)
                self.pressure_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Añadir los elementos al layout en el orden correcto
                sensor_container_layout.addWidget(pressure_title)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                sensor_container_layout.addWidget(widget)
                sensor_container_layout.addWidget(self.pressure_status)
                
                # Obtener la siguiente posición disponible
                if positions:
                    row, col = positions.pop(0)
                    content_grid.addWidget(sensor_container, row, col)
                
                # Actualizar contador
                sensor_count += 1
                
                continue
                
            elif sensor_id == "Calidad_Aire":
                # Crear contenedor individual para el sensor
                sensor_container = QWidget()
                sensor_container.setStyleSheet(container_style)
                
                # Layout para el sensor
                sensor_container_layout = QVBoxLayout(sensor_container)
                sensor_container_layout.setContentsMargins(container_margins, container_margins, container_margins, container_margins)
                sensor_container_layout.setSpacing(container_spacing)
                
                # Título "Calidad del Aire" en la parte superior
                air_quality_title = QLabel("Calidad del Aire")
                air_quality_title.setStyleSheet(title_style)
                air_quality_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Añadir widget de calidad del aire
                widget = AirQualityWidget(parent=self)
                widget.set_range(sensor_info['min_value'], sensor_info['max_value'])
                
                # Guardar referencia
                self.sensor_widgets[sensor_id] = widget
                
                # Estado en la parte inferior
                self.air_quality_status = QLabel("Estado: Buena")
                self.air_quality_status.setStyleSheet(status_style)
                self.air_quality_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Añadir los elementos al layout en el orden correcto
                sensor_container_layout.addWidget(air_quality_title)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                sensor_container_layout.addWidget(widget)
                sensor_container_layout.addWidget(self.air_quality_status)
                
                # Obtener la siguiente posición disponible
                if positions:
                    row, col = positions.pop(0)
                    content_grid.addWidget(sensor_container, row, col)
                
                # Actualizar contador
                sensor_count += 1
                
                continue
            
            # Para ruido, usar el widget personalizado
            elif sensor_id == "Ruido":
                # Crear contenedor individual para el sensor de ruido
                sensor_container = QWidget()
                sensor_container.setStyleSheet(container_style)
                
                # Layout para el sensor
                sensor_container_layout = QVBoxLayout(sensor_container)
                sensor_container_layout.setContentsMargins(container_margins, container_margins, container_margins, container_margins)
                sensor_container_layout.setSpacing(container_spacing)
                
                # Título "Nivel de Ruido" en la parte superior
                noise_title = QLabel("Nivel de Ruido")
                noise_title.setStyleSheet(title_style)
                noise_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Añadir widget de ruido
                widget = NoiseWidget(
                    min_value=sensor_info['min_value'],
                    max_value=sensor_info['max_value'],
                    parent=self
                )
                
                # Guardar referencia
                self.sensor_widgets[sensor_id] = widget
                
                # Estado en la parte inferior
                self.noise_status = QLabel("Estado: Normal")
                self.noise_status.setStyleSheet(status_style)
                self.noise_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Añadir los elementos al layout en el orden correcto
                sensor_container_layout.addWidget(noise_title)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                sensor_container_layout.addWidget(widget)
                sensor_container_layout.addWidget(self.noise_status)
                
                # Obtener la siguiente posición disponible
                if positions:
                    row, col = positions.pop(0)
                    content_grid.addWidget(sensor_container, row, col)
                
                # Actualizar contador
                sensor_count += 1
                
                continue
            
            # Crear contenedor individual para cada sensor
            sensor_container = QWidget()
            sensor_container.setStyleSheet(container_style)
            
            # Layout para el sensor
            sensor_container_layout = QVBoxLayout(sensor_container)
            sensor_container_layout.setContentsMargins(container_margins, container_margins, container_margins, container_margins)
            sensor_container_layout.setSpacing(container_spacing)
            
            # Crear widget para el sensor
            widget = SensorWidget(
                sensor_id=sensor_id,
                sensor_type=sensor_id,
                title=sensor_info['name'],
                unit=sensor_info['unit'],
                min_value=sensor_info['min_value'],
                max_value=sensor_info['max_value'],
                parent=self
            )
            
            # Guardar referencia
            self.sensor_widgets[sensor_id] = widget
            
            # Añadir el widget al contenedor
            sensor_container_layout.addWidget(widget)
            
            # Obtener la siguiente posición disponible
            if positions:
                row, col = positions.pop(0)
                content_grid.addWidget(sensor_container, row, col)
            
            # Actualizar contador
            sensor_count += 1
        
        # Crear un botón para IA
        ia_container = QWidget()
        ia_container.setStyleSheet("""
            QWidget {
                background-color: rgba(155, 89, 182, 0.2);  /* Aumentar un poco la opacidad */
                border: none;
                border-radius: 20px;
                background: qradialgradient(cx:0.5, cy:0.5, radius: 0.8, fx:0.5, fy:0.5,
                                           stop:0 rgba(155, 89, 182, 0.3),
                                           stop:1 rgba(155, 89, 182, 0.2));
            }
            QWidget:hover {
                background-color: rgba(155, 89, 182, 0.3);  /* Aumentar opacidad en hover */
                border: none;
                background: qradialgradient(cx:0.5, cy:0.5, radius: 0.8, fx:0.5, fy:0.5,
                                          stop:0 rgba(155, 89, 182, 0.4),
                                          stop:1 rgba(155, 89, 182, 0.3));
            }
        """)
        ia_container.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Establecer tamaño mínimo para todo el contenedor
        ia_container.setMinimumSize(240, 240)  # Aumentar un poco el tamaño mínimo para acomodar mejor el texto
        
        # Hacer que el contenedor sea clickeable
        ia_container.mousePressEvent = lambda event: self.handle_ai_button_click(ia_container)
        
        # Layout para el botón de IA
        ia_layout = QVBoxLayout(ia_container)
        ia_layout.setContentsMargins(20, 25, 20, 30)  # Reducir margen superior y aumentar inferior para balancear el texto más grande
        ia_layout.setSpacing(25)  # Mantener el espaciado entre elementos
        
        class AiCircleWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setMinimumSize(140, 140)  # Aumentar aún más el tamaño del círculo
                self.active = False
                self.animation_counter = 0
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_animation)
                self.timer.start(100)
                
            def update_animation(self):
                self.animation_counter += 1
                if self.animation_counter > 30:
                    self.animation_counter = 0
                self.update()
                
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                # Tamaño y centro
                width = self.width()
                height = self.height()
                center_x = width / 2
                center_y = height / 2
                
                # Dibujar círculo exterior
                gradient = QRadialGradient(center_x, center_y, width/2 - 5)
                gradient.setColorAt(0, QColor(155, 89, 182, 150))  # Morado semi-transparente en centro
                gradient.setColorAt(1, QColor(155, 89, 182, 255))  # Morado sólido en bordes
                
                painter.setPen(QPen(QColor(155, 89, 182), 2))
                painter.setBrush(QBrush(gradient))
                painter.drawEllipse(QPointF(center_x, center_y), width/2 - 5, height/2 - 5)
                
                # Dibujar círculo interior (fondo oscuro)
                painter.setBrush(QBrush(QColor(26, 26, 26)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPointF(center_x, center_y), width/2 - 15, height/2 - 15)
                
                # Dibujar ondas de voz animadas
                painter.setPen(QPen(QColor(155, 89, 182), 3))  # Aumentar grosor de las líneas
                
                # Calcular altura de ondas basado en animación
                wave_heights = []
                for i in range(3):
                    # Calcular la altura con una función senoidal dependiente del contador
                    phase = (self.animation_counter / 30.0) * 2 * 3.14159 + i * 2.1
                    height = 15 + 20 * abs(math.sin(phase))  # Aumentar altura para hacerlas más visibles
                    wave_heights.append(height)
                
                # Dibujar ondas
                bar_width = 6  # Aumentar ancho de las barras
                bar_spacing = 9  # Aumentar espaciado entre barras
                total_width = (len(wave_heights) * bar_width) + ((len(wave_heights) - 1) * bar_spacing)
                start_x = center_x - (total_width / 2)
                
                for i, height in enumerate(wave_heights):
                    x = start_x + (i * (bar_width + bar_spacing))
                    y = center_y - (height / 2)
                    painter.drawLine(QPointF(x, y), QPointF(x, y + height))
        
        # Crear el widget del círculo de IA
        ai_circle = AiCircleWidget()
        
        # Texto descriptivo
        ia_description = QLabel("Pregúntame\nlo que necesites")  # Agregar salto de línea para mejor legibilidad
        ia_description.setStyleSheet("""
            color: rgba(155, 89, 182, 1.0);  /* Color más sólido para mejor legibilidad */
            background-color: transparent;
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 0.5px;  /* Aumentar espaciado entre letras para mejorar legibilidad */
        """)
        ia_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ia_description.setWordWrap(True)
        
        # Añadir elementos al layout con espaciado extra para compensar la falta de título
        ia_layout.addStretch(1)  # Usar 1 en lugar de 0.5 para el espacio superior
        ia_layout.addWidget(ai_circle, 0, Qt.AlignmentFlag.AlignCenter)
        ia_layout.addWidget(ia_description)
        ia_layout.addStretch(2)  # Aumentar el espacio inferior proporcionalmente
        
        # Colocar el botón de IA en la última posición disponible
        if positions:
            row, col = positions.pop(0)
            content_grid.addWidget(ia_container, row, col)
        
        # Agregar el grid de contenido al layout principal
        main_layout.addLayout(content_grid)
        
        # Ajustar el tamaño de la ventana para que coincida con la resolución
        self.setFixedSize(800, 480)
    
    def update_sensor_values(self, data=None):
        """
        Actualiza los valores de los sensores.
        Si data es None, genera valores aleatorios para pruebas.
        
        Args:
            data (dict, optional): Diccionario con los datos de los sensores
        """
        # Inicializar valores si no existen
        if not hasattr(self, 'prev_temp_value'):
            self.prev_temp_value = 24.0  # Valor inicial razonable
        if not hasattr(self, 'prev_humidity_value'):
            self.prev_humidity_value = 45.0  # Valor inicial razonable
        if not hasattr(self, 'prev_pressure_value'):
            self.prev_pressure_value = 1010.0  # Valor inicial razonable
        if not hasattr(self, 'prev_air_quality_value'):
            self.prev_air_quality_value = 50.0  # Valor inicial razonable
        if not hasattr(self, 'prev_noise_value'):
            self.prev_noise_value = 45.0  # Valor inicial razonable
        
        # Modo de prueba - crear oscilaciones para ver los cambios de estado
        # Para presión atmosférica: crear ciclos que crucen los umbrales (1000 y 1015)
        if not hasattr(self, 'test_mode'):
            self.test_mode = True
            self.cycle_counter = 0
            self.pressure_cycle = 0
            self.temp_cycle = 0
            
        # Incrementar contador de ciclo general
        self.cycle_counter += 1
        
        # RALENTIZAR: Actualizar la presión solo cada 5 ciclos
        if self.cycle_counter % 5 == 0:
            self.pressure_cycle += 1
            
            # Ciclo completo cada ~80 actualizaciones
            # Un ciclo completo cada ~16 segundos (80 x 200ms)
            cycle_position = self.pressure_cycle % 80
            
            # Si estamos en la primera mitad del ciclo, aumenta; en la segunda, disminuye
            if cycle_position < 40:
                # Subiendo: de 995 a 1025 más lentamente
                pressure_value = 995 + (cycle_position * 0.75)  # 0.75 hPa por paso
            else:
                # Bajando: de 1025 a 995 más lentamente
                reverse_position = 80 - cycle_position
                pressure_value = 995 + (reverse_position * 0.75)
        else:
            # Mantener el valor anterior si no toca actualizar
            pressure_value = self.prev_pressure_value
            
        # Ciclo para temperatura (solo actualizar cada 10 ciclos)
        if self.cycle_counter % 10 == 0:
            self.temp_cycle += 1
            # Ciclo completo cada ~120 actualizaciones (24 segundos)
            temp_cycle_position = self.temp_cycle % 120
            
            # Crear ciclo de temperatura que atraviese todos los umbrales
            if temp_cycle_position < 30:
                # Subiendo de 18 a 22 (Frío a Normal)
                temp_value = 18 + (temp_cycle_position * 0.13)
            elif temp_cycle_position < 60:
                # Subiendo de 22 a 27 (Normal a Cálido)
                temp_value = 22 + ((temp_cycle_position - 30) * 0.17)
            elif temp_cycle_position < 90:
                # Subiendo de 27 a 32 (Cálido a Calor)
                temp_value = 27 + ((temp_cycle_position - 60) * 0.17)
            else:
                # Bajando de 32 a 18 (Calor a Frío)
                temp_value = 32 - ((temp_cycle_position - 90) * 0.47)
            
            temp_value = round(temp_value, 1)
        else:
            # Mantener el valor anterior si no toca actualizar
            temp_value = self.prev_temp_value
            
        # Generar nuevos valores para los demás sensores (con pequeños cambios aleatorios)
        humidity_value = round(self.prev_humidity_value + random.uniform(-0.1, 0.1), 1)
        air_quality_value = round(self.prev_air_quality_value + random.uniform(-0.1, 0.1), 1)
        noise_value = round(self.prev_noise_value + random.uniform(-0.1, 0.1), 1)
        
        # Mantener dentro de rangos razonables
        temp_value = max(18.0, min(32.0, temp_value))
        humidity_value = max(20.0, min(80.0, humidity_value))
        pressure_value = round(max(995.0, min(1025.0, pressure_value)), 1)
        air_quality_value = max(0.0, min(100.0, air_quality_value))
        noise_value = max(30.0, min(90.0, noise_value))
        
        # Guardar los valores actuales como previos para la próxima actualización
        self.prev_temp_value = temp_value
        self.prev_humidity_value = humidity_value
        self.prev_pressure_value = pressure_value
        self.prev_air_quality_value = air_quality_value
        self.prev_noise_value = noise_value
        
        # Actualizar valores en los widgets
        self.thermometer.set_value(temp_value)
        
        # Actualizar el estado de temperatura
        if temp_value < 20:
            status = "Frío"
            status_color = "#3498db"  # Azul
        elif temp_value <= 25:
            status = "Normal"
            status_color = "#2ecc71"  # Verde
        elif temp_value <= 28:
            status = "Cálido"
            status_color = "#f39c12"  # Naranja
        else:
            status = "Calor"
            status_color = "#e74c3c"  # Rojo
        
        # Actualizar el texto de estado
        self.temperature_status.setText(f"Estado: {status}")
        self.temperature_status.setStyleSheet(f"""
            color: {status_color};
            font-size: 16px;
            font-weight: bold;
            background-color: transparent;
            padding: 2px;
        """)
        
        # Actualizar todos los sensores
        for sensor_id, widget in self.sensor_widgets.items():
            if sensor_id == "Temperatura":
                widget.set_value(temp_value)
            elif sensor_id == "Humedad":
                widget.set_value(humidity_value)
                
                # Actualizar el estado de humedad
                if humidity_value < 30:
                    status = "Seco"
                    status_color = "#e74c3c"  # Rojo
                elif humidity_value <= 50:
                    status = "Normal"
                    status_color = "#2ecc71"  # Verde
                elif humidity_value <= 60:
                    status = "Húmedo"
                    status_color = "#3498db"  # Azul
                else:
                    status = "Muy húmedo"
                    status_color = "#9b59b6"  # Púrpura
                
                # Actualizar el texto de estado
                self.humidity_status.setText(f"Estado: {status}")
                self.humidity_status.setStyleSheet(f"""
                    color: {status_color};
                    font-size: 16px;
                    font-weight: bold;
                    background-color: transparent;
                    padding: 2px;
                """)
            
            elif sensor_id == "Presión":
                widget.set_value(pressure_value)
                
                # Actualizar el estado de presión
                if pressure_value < 1000:
                    status = "Baja"
                    status_color = "#3498db"  # Azul para presión baja
                elif pressure_value <= 1015:
                    status = "Normal"
                    status_color = "#2ecc71"  # Verde para presión normal
                else:
                    status = "Alta"
                    status_color = "#e74c3c"  # Rojo para presión alta
                
                # Si existe el campo de estado para presión, actualizarlo
                if hasattr(self, 'pressure_status'):
                    self.pressure_status.setText(f"Estado: {status}")
                    self.pressure_status.setStyleSheet(f"""
                        color: {status_color};
                        font-size: 16px;
                        font-weight: bold;
                        background-color: transparent;
                        padding: 2px;
                    """)
            
            elif sensor_id == "Calidad_Aire":
                widget.set_value(air_quality_value)
                
                # Actualizar el estado de calidad del aire
                if air_quality_value < 50:
                    status = "Excelente"
                    status_color = "#2ecc71"  # Verde
                elif air_quality_value < 100:
                    status = "Buena"
                    status_color = "#3498db"  # Azul
                elif air_quality_value < 150:
                    status = "Moderada"
                    status_color = "#f39c12"  # Naranja
                elif air_quality_value < 300:
                    status = "Mala"
                    status_color = "#e74c3c"  # Rojo
                else:
                    status = "Peligrosa"
                    status_color = "#8e44ad"  # Morado
                
                # Actualizar el texto de estado
                self.air_quality_status.setText(f"Estado: {status}")
                self.air_quality_status.setStyleSheet(f"""
                    color: {status_color};
                    font-size: 16px;
                    font-weight: bold;
                    background-color: transparent;
                    padding: 2px;
                """)
            
            elif sensor_id == "Ruido":
                widget.set_value(noise_value)
                
                # Actualizar el estado de ruido
                if noise_value < 60:
                    status = "Bajo"
                    status_color = "#f1c40f"  # Amarillo
                elif noise_value < 80:
                    status = "Moderado"
                    status_color = "#f39c12"  # Naranja
                else:
                    status = "Alto"
                    status_color = "#e74c3c"  # Rojo
                
                # Actualizar el texto de estado
                self.noise_status.setText(f"Estado: {status}")
                self.noise_status.setStyleSheet(f"""
                    color: {status_color};
                    font-size: 16px;
                    font-weight: bold;
                    background-color: transparent;
                    padding: 2px;
                """)
    
    def show_error_message(self, title, message):
        """
        Muestra un mensaje de error en una ventana emergente.
        
        Args:
            title (str): Título de la ventana
            message (str): Mensaje de error a mostrar
        """
        error_box = QMessageBox(self)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_box.exec()
    
    def handle_ai_button_click(self, button_widget):
        """
        Maneja el evento de clic en el botón de IA.
        
        Args:
            button_widget: El widget del botón que fue presionado
        """
        # Efecto visual de presionar el botón
        button_widget.setStyleSheet("""
            background-color: rgba(155, 89, 182, 0.4);
            border: none;
            border-radius: 20px;
            background: qradialgradient(cx:0.5, cy:0.5, radius: 0.8, fx:0.5, fy:0.5,
                                       stop:0 rgba(155, 89, 182, 0.5),
                                       stop:1 rgba(155, 89, 182, 0.4));
        """)
        
        # Restaurar el estilo original después de 150ms
        QTimer.singleShot(150, lambda: button_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(155, 89, 182, 0.2);
                border: none;
                border-radius: 20px;
                background: qradialgradient(cx:0.5, cy:0.5, radius: 0.8, fx:0.5, fy:0.5,
                                           stop:0 rgba(155, 89, 182, 0.3),
                                           stop:1 rgba(155, 89, 182, 0.2));
            }
            QWidget:hover {
                background-color: rgba(155, 89, 182, 0.3);
                border: none;
                background: qradialgradient(cx:0.5, cy:0.5, radius: 0.8, fx:0.5, fy:0.5,
                                          stop:0 rgba(155, 89, 182, 0.4),
                                          stop:1 rgba(155, 89, 182, 0.3));
            }
        """))
        
        # Crear un diálogo personalizado
        dialog = QDialog(self)
        dialog.setWindowTitle("Asistente Virtual")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #9b59b6;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: rgba(155, 89, 182, 0.8);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(155, 89, 182, 1.0);
            }
        """)
        
        # Layout principal
        layout = QVBoxLayout(dialog)
        
        # Área de chat
        chat_area = QTextEdit()
        chat_area.setReadOnly(True)
        chat_area.setPlaceholderText("Escribe tu pregunta aquí...")
        layout.addWidget(chat_area)
        
        # Área de entrada
        input_layout = QHBoxLayout()
        input_field = QLineEdit()
        input_field.setPlaceholderText("Escribe tu mensaje...")
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #9b59b6;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        
        send_button = QPushButton("Enviar")
        input_layout.addWidget(input_field)
        input_layout.addWidget(send_button)
        layout.addLayout(input_layout)
        
        # Función para procesar el mensaje
        def process_message():
            message = input_field.text().strip()
            if message:
                # Añadir mensaje del usuario
                chat_area.append(f"<p style='color: #9b59b6;'><b>Tú:</b> {message}</p>")
                
                # Procesar la respuesta según el mensaje
                response = self.process_ai_response(message)
                
                # Añadir respuesta del asistente
                chat_area.append(f"<p style='color: #ffffff;'><b>Asistente:</b> {response}</p>")
                
                # Limpiar campo de entrada
                input_field.clear()
                
                # Desplazar al final
                chat_area.verticalScrollBar().setValue(
                    chat_area.verticalScrollBar().maximum()
                )
        
        # Conectar eventos
        send_button.clicked.connect(process_message)
        input_field.returnPressed.connect(process_message)
        
        # Mostrar mensaje inicial
        chat_area.append("<p style='color: #ffffff;'><b>Asistente:</b> ¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?</p>")
        
        # Mostrar el diálogo
        dialog.exec()