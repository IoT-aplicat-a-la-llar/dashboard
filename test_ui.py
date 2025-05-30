"""
Prueba de la interfaz gráfica con el termómetro.
Este script ejecuta solo la interfaz gráfica sin conectarse al broker MQTT.
Útil para pruebas de diseño y desarrollo.
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.logger import setup_logger
import os

# Configurar logger para el módulo de prueba
logger = setup_logger(__name__)

def main():
    """
    Función principal que inicia la aplicación de prueba.
    Solo muestra la interfaz gráfica sin conectar al broker MQTT.
    """
    # Informar al usuario
    logger.info("Iniciando modo de prueba de UI (sin conexión MQTT)")
    
    # Configurar el plugin de Qt para entorno de escritorio
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    
    # Crear la aplicación
    app = QApplication(sys.argv)
    
    try:
        # Crear y mostrar la ventana principal
        logger.info("Creando interfaz gráfica...")
        window = MainWindow()
        window.show()
        
        # Ejecutar la aplicación
        logger.info("Interfaz lista. Los datos son simulados.")
        return app.exec()
    except Exception as e:
        logger.error(f"Error al iniciar la aplicación de prueba: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())