# COSMIC Resource Monitor
<img width="358" height="342" alt="imagen" src="https://github.com/user-attachments/assets/793f94e3-dddd-4131-a59e-2df374c6a776" />
<img width="501" height="690" alt="imagen" src="https://github.com/user-attachments/assets/a4627a5f-f1aa-4afd-b82e-f92e567445d5" />
<img width="501" height="690" alt="imagen" src="https://github.com/user-attachments/assets/79e8437e-20b8-4310-8463-5ed7d0fb7733" />

Este es un widget de escritorio circular para sistemas Linux, diseñado para mostrar el consumo y temperatura de CPU, memoria RAM y GPU en tiempo real. 

Utiliza GTK3 y GtkLayerShell para integrarse directamente como una capa del escritorio. Aunque está diseñado y optimizado pensando en el entorno COSMIC, funciona sin problemas en otros compositores compatibles con Wayland y X11.

## Características principales
- Monitoreo de CPU: muestra el porcentaje de uso y su temperatura actual.
- Monitoreo de RAM: muestra el consumo en gigabytes y el porcentaje de uso.
- Monitoreo de GPU: detecta de forma automática tarjetas de video NVIDIA, AMD e Intel. Para tarjetas AMD e Intel lee directamente los sensores del kernel (sysfs), evitando el uso de procesos secundarios lentos.
- Movimiento fluido en pantalla: incluye soporte de arrastre optimizado para sesiones Wayland y X11.
- Interfaz de configuración: ventana gráfica para cambiar colores, tamaños, tipos de letra, espaciado y la distribución geométrica de los círculos.
- Diseño optimizado: consumo mínimo de recursos mediante consultas rápidas del sistema.

## Requisitos previos
Antes de instalar, necesitas asegurarte de tener instaladas las librerías de introspección de GTK3 y Layer Shell en tu sistema.

Para distribuciones basadas en Debian, Ubuntu o Pop!_OS, ejecuta en tu terminal:
```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1 python3-venv
```

Si usas Arch Linux, puedes instalar los equivalentes utilizando pacman:
```bash
sudo pacman -S python-gobject gtk3 gtk-layer-shell python-virtualenv
```

## Instalación paso a paso
Sigue estos pasos en tu terminal para instalar el widget en tu cuenta de usuario:

1. Clona este repositorio en tu computadora:
   ```bash
   git clone https://github.com/WilmanM8/cosmic-resource-widget.git
   ```

2. Entra en la carpeta del proyecto:
   ```bash
   cd cosmic-resource-widget
   ```

3. Dale permisos de ejecución al instalador y ejecútalo:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

El script se encargará de crear un entorno virtual de Python, instalar las librerías necesarias (como `psutil` y `pycairo`) y configurar los accesos directos en tu menú de aplicaciones de usuario.

## Modo de uso
Una vez completada la instalación, puedes controlar el widget de la siguiente forma:

- **Iniciar el monitor:** Busca "COSMIC Resource Monitor" en tu menú de aplicaciones para iniciar el widget. También se configurará para arrancar automáticamente al iniciar sesión.
- **Mover el widget:** Haz clic izquierdo sobre cualquier parte del widget y arrástralo a la posición de la pantalla que prefieras. La posición se guardará de forma automática.
- **Configurar:** Haz clic derecho sobre el widget y selecciona la opción "Configurar Recursos" para abrir el panel de ajustes visuales.
- **Cerrar:** Haz clic derecho y selecciona "Cerrar Monitor" o pulsa el botón correspondiente en la ventana de configuración.

## Desinstalación
Si deseas eliminar por completo el widget y sus archivos de configuración de tu sistema, puedes ejecutar los siguientes comandos:

```bash
# Detener el proceso si está activo
pkill -f resource_widget.py

# Eliminar carpeta de instalación y accesos directos
rm -rf ~/.local/share/cosmic-resource-widget
rm -f ~/.local/share/applications/cosmic-resource-widget.desktop
rm -f ~/.local/share/applications/cosmic-resource-config.desktop
rm -f ~/.config/autostart/cosmic-resource-widget.desktop

# Opcional: eliminar el archivo de configuración del usuario
rm -rf ~/.config/cosmic-resource-widget
```
