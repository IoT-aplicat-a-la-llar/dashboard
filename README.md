# Monitor de Sensores Ambientales

Este repositorio contiene el código fuente y la documentación técnica del sistema de monitorización ambiental, organizado en diferentes carpetas según el tipo de contenido.

## Índice de Carpetas

- [`ui/`](./ui): Contiene la interfaz gráfica de usuario desarrollada con PyQt6.
  - [`widgets/`](./ui/widgets): Incluye los widgets personalizados para cada tipo de sensor:
    - `thermometer_widget.py`: Widget para visualizar la temperatura
    - `humidity_widget.py`: Widget para visualizar la humedad
    - `pressure_widget.py`: Widget para visualizar la presión atmosférica
    - `air_quality_widget.py`: Widget para visualizar la calidad del aire
    - `noise_widget.py`: Widget para visualizar el nivel de ruido
  - `main_window.py`: Ventana principal que integra todos los widgets

- [`config/`](./config): Archivos de configuración del sistema:
  - Configuración de la interfaz de usuario
  - Parámetros de los sensores
  - Rangos y umbrales de alerta

- [`docs/`](./docs): Documentación técnica del proyecto:
  - Especificaciones de los sensores
  - Diagramas de conexión
  - Guías de instalación y uso

Este repositorio tiene como objetivo proporcionar una solución completa para la monitorización ambiental, integrando diferentes tipos de sensores en una interfaz gráfica moderna y fácil de usar. 

¡¡ IMPORTANTE!! Demomento ejecutar el test_ui.py. Comunicación en desarrollo.
