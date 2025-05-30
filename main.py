"""
Archivo principal de la aplicación de domótica.
Inicia la interfaz gráfica y el cliente MQTT.
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from mqtt_client import MQTTClient
from utils.logger import setup_logger
import os

# Configurar logger para el módulo principal
logger = setup_logger(__name__)

def main():
    """
    Función principal que inicia la aplicación.
    
    Establece la interfaz gráfica, inicia el cliente MQTT
    y conecta los componentes.
    """
    # Configurar el plugin de Qt para entorno de escritorio
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    
    # Crear la aplicación
    app = QApplication(sys.argv)
    
    try:
        # Crear la ventana principal
        logger.info("Iniciando la interfaz gráfica...")
        window = MainWindow()
        
        # Crear el cliente MQTT
        logger.info("Creando cliente MQTT...")
        mqtt_client = MQTTClient(on_data_received=window.update_sensor_values)
        
        try:
            # Conectar al broker MQTT
            logger.info("Conectando al broker MQTT...")
            mqtt_client.connect()
            
            # Mostrar la ventana
            window.show()
            
            # Ejecutar la aplicación y capturar el código de salida
            exit_code = app.exec()
            
            # Desconectar el cliente MQTT antes de salir
            logger.info("Desconectando cliente MQTT...")
            mqtt_client.disconnect()
            
            # Salir con el código de salida
            sys.exit(exit_code)
            
        except Exception as e:
            logger.error(f"Error al conectar al broker MQTT: {e}")
            
            # Mostrar un mensaje de error en la ventana
            window.show_error_message("Error de conexión", 
                                      f"No se pudo conectar al broker MQTT: {e}")
            
            # Mostrar la ventana de todos modos para permitir la interacción
            window.show()
            sys.exit(app.exec())
            
    except Exception as e:
        logger.error(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 