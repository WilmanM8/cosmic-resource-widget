#!/bin/bash

echo "=========================================="
echo " Instalando COSMIC Resource Monitor..."
echo "=========================================="

sudo apt update
sudo apt install -y python3-gi gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1 python3-venv

INSTALL_DIR="$HOME/.local/share/cosmic-resource-widget"
echo "-> Copiando archivos a $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp resource_widget.py config_app.py resource_api.py "$INSTALL_DIR/"

echo "-> Configurando entorno virtual de Python..."
cd "$INSTALL_DIR"
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install psutil pycairo

echo "-> Creando accesos directos..."
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"

cat <<EOF > "$APPS_DIR/cosmic-resource-widget.desktop"
[Desktop Entry]
Name=COSMIC Resource Monitor
Comment=Monitor de recursos circular para el escritorio
Exec=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/resource_widget.py
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=Utility;System;
EOF

cat <<EOF > "$APPS_DIR/cosmic-resource-config.desktop"
[Desktop Entry]
Name=Configuración de Recursos COSMIC
Comment=Ajustar anillos y colores del monitor
Exec=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/config_app.py
Icon=preferences-desktop
Terminal=false
Type=Application
Categories=Utility;Settings;
EOF

AUTOSTART_DIR="$HOME/.config/autostart"
mkdir -p "$AUTOSTART_DIR"
cp "$APPS_DIR/cosmic-resource-widget.desktop" "$AUTOSTART_DIR/"

echo "=========================================="
echo " ¡Instalación Completada con Éxito!"
echo "=========================================="
