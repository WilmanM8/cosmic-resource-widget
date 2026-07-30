# COSMIC Resource Monitor
<img width="358" height="342" alt="imagen" src="https://github.com/user-attachments/assets/793f94e3-dddd-4131-a59e-2df374c6a776" />

<img width="501" height="690" alt="imagen" src="https://github.com/user-attachments/assets/a4627a5f-f1aa-4afd-b82e-f92e567445d5" />

<img width="501" height="690" alt="imagen" src="https://github.com/user-attachments/assets/79e8437e-20b8-4310-8463-5ed7d0fb7733" />

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

*(For the Spanish version, scroll down / Para la versión en español, desplázate hacia abajo)*

## 🇬🇧 English

This is a circular desktop widget for Linux systems, designed to display CPU, RAM, and GPU consumption and temperature in real-time.

It uses GTK3 and GtkLayerShell to integrate directly as a desktop layer. Although it is designed and optimized for the COSMIC desktop environment, it works seamlessly on other Wayland and X11 compositors.

### Key Features
- CPU Monitoring: displays usage percentage and current temperature.
- RAM Monitoring: displays consumption in gigabytes and usage percentage.
- GPU Monitoring: automatically detects NVIDIA, AMD, and Intel graphics cards. For AMD and Intel cards, it directly reads kernel sensors (sysfs), avoiding slow secondary processes.
- Smooth on-screen movement: includes optimized drag support for Wayland and X11 sessions.
- Configuration Interface: graphical window to change colors, sizes, fonts, spacing, and geometric layout of the circles.
- Optimized Design: minimal resource consumption through fast system polling.

### Prerequisites
Before installing, ensure you have the GTK3 introspection libraries and Layer Shell installed on your system.

For Debian, Ubuntu, or Pop!_OS based distributions, run in your terminal:
```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1 python3-venv
```

If you use Arch Linux, you can install the equivalents using pacman:
```bash
sudo pacman -S python-gobject gtk3 gtk-layer-shell python-virtualenv
```

### Step-by-Step Installation
Follow these steps in your terminal to install the widget in your user account:

1. Clone this repository to your computer:
   ```bash
   git clone https://github.com/WilmanM8/cosmic-resource-widget.git
   ```

2. Enter the project folder:
   ```bash
   cd cosmic-resource-widget
   ```

3. Give execution permissions to the installer and run it:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

The script will create a Python virtual environment, install the necessary libraries (like `psutil` and `pycairo`), and set up shortcuts in your user application menu.

### Usage
Once the installation is complete, you can control the widget as follows:

- **Start the monitor:** Search for "COSMIC Resource Monitor" in your application menu to start the widget. It will also be configured to start automatically on login.
- **Move the widget:** Left-click on any part of the widget and drag it to your preferred screen position. The position will be saved automatically.
- **Configure:** Right-click on the widget and select "Configurar Recursos" (Configure Resources) to open the visual settings panel.
- **Close:** Right-click and select "Cerrar Monitor" (Close Monitor) or click the corresponding button in the configuration window.

### Uninstallation
If you want to completely remove the widget and its configuration files from your system, you can run the following commands:

```bash
# Stop the process if it is active
pkill -f resource_widget.py

# Remove installation folder and shortcuts
rm -rf ~/.local/share/cosmic-resource-widget
rm -f ~/.local/share/applications/cosmic-resource-widget.desktop
rm -f ~/.local/share/applications/cosmic-resource-config.desktop
rm -f ~/.config/autostart/cosmic-resource-widget.desktop

# Optional: remove user configuration file
rm -rf ~/.config/cosmic-resource-widget
```

---

## 🇪🇸 Español

Este es un widget de escritorio circular para sistemas Linux, diseñado para mostrar el consumo y temperatura de CPU, memoria RAM y GPU en tiempo real. 

Utiliza GTK3 y GtkLayerShell para integrarse directamente como una capa del escritorio. Aunque está diseñado y optimizado pensando en el entorno COSMIC, funciona sin problemas en otros compositores compatibles con Wayland y X11.

### Características principales
- Monitoreo de CPU: muestra el porcentaje de uso y su temperatura actual.
- Monitoreo de RAM: muestra el consumo en gigabytes y el porcentaje de uso.
- Monitoreo de GPU: detecta de forma automática tarjetas de video NVIDIA, AMD e Intel. Para tarjetas AMD e Intel lee directamente los sensores del kernel (sysfs), evitando el uso de procesos secundarios lentos.
- Movimiento fluido en pantalla: incluye soporte de arrastre optimizado para sesiones Wayland y X11.
- Interfaz de configuración: ventana gráfica para cambiar colores, tamaños, tipos de letra, espaciado y la distribución geométrica de los círculos.
- Diseño optimizado: consumo mínimo de recursos mediante consultas rápidas del sistema.

### Requisitos previos
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

### Instalación paso a paso
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

### Modo de uso
Una vez completada la instalación, puedes controlar el widget de la siguiente forma:

- **Iniciar el monitor:** Busca "COSMIC Resource Monitor" en tu menú de aplicaciones para iniciar el widget. También se configurará para arrancar automáticamente al iniciar sesión.
- **Mover el widget:** Haz clic izquierdo sobre cualquier parte del widget y arrástralo a la posición de la pantalla que prefieras. La posición se guardará de forma automática.
- **Configurar:** Haz clic derecho sobre el widget y selecciona la opción "Configurar Recursos" para abrir el panel de ajustes visuales.
- **Cerrar:** Haz clic derecho y selecciona "Cerrar Monitor" o pulsa el botón correspondiente en la ventana de configuración.

### Desinstalación
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
