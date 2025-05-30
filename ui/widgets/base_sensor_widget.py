"""
Clase base para todos los widgets de sensores.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from config import SENSORS

class BaseSensorWidget(QWidget):
    def __init__(self, sensor_id, sensor_type, title, unit, min_value, max_value, parent=None):
        """
        Inicializa un widget base para sensores.
        
        Args:
            sensor_id (str): Identificador único del sensor
            sensor_type (str): Tipo de sensor (debe existir en config.SENSORS)
            title (str): Título a mostrar
            unit (str): Unidad de medida
            min_value (float): Valor mínimo
            max_value (float): Valor máximo
            parent (QWidget, optional): Widget padre
        """
        super().__init__(parent)
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.title = title
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.value = 0.0
        
        # Obtener información del sensor de la configuración
        self.sensor_info = SENSORS.get(self.sensor_type, SENSORS["Temperatura"])
        
        # Habilitar transparencia
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Configurar el estilo del widget
        self._setup_styles()
        
        # Crear la estructura básica del widget
        self._create_widget_structure()
        
        # Actualizar información inicial
        self.update_sensor_info()
    
    def _setup_styles(self):
        """
        Configura los estilos básicos del widget.
        Puede ser sobreescrito por las clases hijas para personalización.
        """
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        # Establecer tamaño mínimo
        self.setMinimumSize(150, 100)
    
    def _create_widget_structure(self):
        """
        Crea la estructura básica del widget con layout y etiquetas.
        Puede ser sobreescrito por las clases hijas para personalización.
        """
        # Crear layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)
        
        # Título del sensor
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-size: 16px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Valor del sensor
        self.value_label = QLabel(f"0 {self.unit}")
        self.value_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Agregar widgets al layout
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.value_label)
    
    def set_value(self, value):
        """
        Establece el valor del sensor y actualiza la UI.
        
        Args:
            value (float): Nuevo valor
        """
        self.value = max(self.min_value, min(value, self.max_value))  # Limitar valor al rango
        self.update_sensor_info()
        
    def update_sensor_info(self):
        """
        Actualiza la información mostrada del sensor.
        Puede ser sobreescrito por las clases hijas para personalización.
        """
        # Formatear el valor con la unidad
        value_text = f"{self.value:.1f} {self.unit}"
        self.value_label.setText(value_text)
        
        # Actualizar color según umbrales
        if "warning_threshold" in self.sensor_info and "critical_threshold" in self.sensor_info:
            warning = self.sensor_info["warning_threshold"]
            critical = self.sensor_info["critical_threshold"]
            
            if self.value >= critical:
                color = "#e74c3c"  # Rojo
            elif self.value >= warning:
                color = "#f39c12"  # Naranja
            else:
                color = "#2ecc71"  # Verde
                
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: transparent;
                    border: 2px solid {color};
                    border-radius: 10px;
                }}
            """)
    
    def apply_rotation(self, angle: int):
        """
        Aplica rotación al contenido del widget.
        
        Args:
            angle (int): Ángulo de rotación en grados
        """
        if angle == 90:
            # Rotar todo el contenido 90 grados desde el centro
            self.setStyleSheet("""
                #contentWidget {
                    transform: rotate(90deg);
                    transform-origin: center center;
                    position: absolute;
                    left: 50%;
                    top: 50%;
                    margin-left: -50%;
                    margin-top: -50%;
                    width: 100%;
                    height: 100%;
                }
            """)
        else:
            # Restaurar orientación original
            self.setStyleSheet("""
                #contentWidget {
                    position: relative;
                    width: 100%;
                    height: 100%;
                }
            """)
    
    def get_color_for_value(self, value):
        """
        Determina el color correspondiente a un valor según los umbrales configurados.
        
        Args:
            value (float): Valor a evaluar
            
        Returns:
            str: Código de color hexadecimal
        """
        warning = self.sensor_info.get("warning_threshold")
        critical = self.sensor_info.get("critical_threshold")
        
        if warning is not None and critical is not None:
            if value >= critical:
                return "#e74c3c"  # Rojo
            elif value >= warning:
                return "#f39c12"  # Naranja
            else:
                return "#2ecc71"  # Verde
        
        # Valor por defecto si no hay umbrales
        return "#3498db"  # Azul 