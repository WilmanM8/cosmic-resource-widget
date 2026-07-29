# COSMIC Resource Monitor

Este es un widget circular (desklet) para entornos de escritorio Linux, diseñado para mostrar el uso y temperatura de CPU, memoria RAM y GPU en tiempo real. 

Está optimizado especialmente para el nuevo escritorio COSMIC, usando GtkLayerShell para integrarse como una capa del escritorio, aunque funciona en cualquier compositor compatible con Wayland y X11.

## Características
- Monitoreo en tiempo real de CPU (con temperatura).
- Monitoreo de memoria RAM (muestra el consumo en GB y porcentaje).
- Monitoreo de GPU (detecta automáticamente controladores NVIDIA, AMD e Intel).
- Arrastre suave compatible tanto con Wayland como con X11.
- Panel de configuración visual para ajustar tamaños, espaciado, colores, fuentes y la posición del widget.
- Diseño ligero en Python que lee directamente las métricas del sistema, evitando consumo innecesario de procesador.

## Requisitos
Para ejecutar este widget necesitas tener instaladas las dependencias de GTK3 y Layer Shell en tu sistema.

En sistemas basados en Debian, Ubuntu o Pop!_OS puedes instalarlas con:
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1 python3-venv
```

## Instalación
Clona el repositorio, entra en la carpeta y ejecuta el script de instalación:
```bash
chmod +x install.sh
./install.sh
```
El instalador creará un entorno virtual de Python, descargará las dependencias necesarias y creará los accesos directos en tu menú de aplicaciones para que puedas abrir el widget y su configurador fácilmente.

## Uso
Una vez instalado:
- Abre "COSMIC Resource Monitor" desde tu menú de aplicaciones para iniciar el widget.
- Puedes mover el widget por el escritorio haciendo clic izquierdo y arrastrándolo.
- Haz clic derecho sobre el widget para abrir el menú contextual. Desde allí puedes abrir la ventana de configuración o cerrar el monitor.
