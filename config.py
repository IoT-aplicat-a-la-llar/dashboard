"""
Archivo de configuración para el proyecto de domótica.
"""

# Configuración MQTT
MQTT_CONFIG = {
    "broker": "localhost",
    "port": 1883,
    "topic": "casa/sensores",
    "username": "Home_Assitan",
    "password": "1234",
    "keepalive": 60
}

# Configuración de colores
COLORS = {
    "background": "#1a1a1a",       # Negro profundo para el fondo
    "widget": "#2d2d2d",          # Gris oscuro para widgets
    "text": "#3498db",            # Azul claro para texto
    "accent": "#2980b9",          # Azul más oscuro para acentos
    "button": "#e74c3c",          # Rojo para botones
    "button_hover": "#c0392b",    # Rojo más oscuro para hover
    "button_text": "#FFFFFF",     # Texto blanco para botones
    "error": "#FF4444"            # Rojo para errores/salir
}

# Configuración de la interfaz
UI_CONFIG = {
    "window_title": "Domótica - Control Central",
    "window_style": """
        QMainWindow {
            background-color: #1a1a1a;
        }
        QWidget {
            background-color: #1a1a1a;
        }
    """,
    "label_style": f"""
        QLabel {{
            color: {COLORS["text"]};
            font-size: 24px;
            font-weight: bold;
            background-color: {COLORS["background"]};
        }}
    """,
    "title_style": """
        QLabel {
            color: #ffffff;
            font-size: 32px;
            font-weight: bold;
            background-color: transparent;
        }
    """,
    "icon_style": f"""
        QLabel {{
            color: {COLORS["text"]};
            font-size: 48px;
            background-color: {COLORS["background"]};
        }}
    """,
    "widget_style": f"""
        QWidget {{
            background-color: {COLORS["background"]};
            border-radius: 10px;
            padding: 10px;
        }}
    """,
    "exit_button_style": """
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 5px;
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }
    """,
    "margin": 20,
    "spacing": 20,
    "sensor_style": """
        QWidget {
            background-color: #2d2d2d;
            border-radius: 10px;
        }
    """
}

# Configuración de los sensores
SENSORS = {
    "Temperatura": {
        "name": "Temperatura",
        "unit": "°C",
        "min_value": 15,
        "max_value": 35,
        "warning_threshold": 30,
        "critical_threshold": 35,
        "color": "#e74c3c"  # Rojo
    },
    "Humedad": {
        "name": "Humedad",
        "unit": "%",
        "min_value": 30,
        "max_value": 70,
        "warning_threshold": 60,
        "critical_threshold": 70,
        "color": "#3498db"  # Azul
    },
    "Presión": {
        "name": "Presión",
        "unit": "hPa",
        "min_value": 980,
        "max_value": 1020,
        "warning_threshold": 1010,
        "critical_threshold": 1020,
        "color": "#2ecc71"  # Verde
    },
    "Calidad_Aire": {
        "name": "Calidad de Aire",
        "unit": "IAQ",
        "min_value": 0,
        "max_value": 500,
        "warning_threshold": 150,
        "critical_threshold": 300,
        "color": "#9b59b6"  # Púrpura
    },
    "Ruido": {
        "name": "Nivel de Ruido",
        "unit": "dB",
        "min_value": 30,
        "max_value": 90,
        "warning_threshold": 60,
        "critical_threshold": 80,
        "color": "#f1c40f"  # Amarillo
    }
} 