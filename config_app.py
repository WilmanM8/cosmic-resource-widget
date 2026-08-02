import sys
import json
import os
# pyrefly: ignore [missing-import]
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
# pyrefly: ignore [missing-import]
from gi.repository import Gtk, Gdk, Pango, PangoCairo

CONFIG_DIR = os.path.expanduser("~/.config/cosmic-resource-widget")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def rgb_to_gdk(rgb_str):
    rgba = Gdk.RGBA()
    if rgba.parse(rgb_str):
        return rgba
    return Gdk.RGBA(0,0,0,1)

class ConfigApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Configuración de Recursos COSMIC")
        self.set_default_size(500, 700)
        self.set_border_width(20)
        self.apply_css()

        self.config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.config = json.load(f)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(vbox)
        self.add(scroll)

        # --- CPU Colors ---
        vbox.pack_start(Gtk.Label(label="<b>Colores de CPU</b>", use_markup=True), False, False, 0)
        self.cpu_fg_btn = self.add_color_control(vbox, "Color Principal (Progreso):", "cpu_fg_color", "#00ffcc")
        self.cpu_bg_btn = self.add_color_control(vbox, "Color de Fondo (Anillo base):", "cpu_bg_color", "#1a1a2e")
        
        vbox.pack_start(Gtk.Separator(), False, False, 5)
        
        # --- RAM Colors ---
        vbox.pack_start(Gtk.Label(label="<b>Colores de RAM</b>", use_markup=True), False, False, 0)
        self.ram_fg_btn = self.add_color_control(vbox, "Color Principal (Progreso):", "ram_fg_color", "#ff00cc")
        self.ram_bg_btn = self.add_color_control(vbox, "Color de Fondo (Anillo base):", "ram_bg_color", "#1a1a2e")

        vbox.pack_start(Gtk.Separator(), False, False, 5)

        # --- GPU Colors ---
        vbox.pack_start(Gtk.Label(label="<b>Colores de GPU</b>", use_markup=True), False, False, 0)
        self.gpu_fg_btn = self.add_color_control(vbox, "Color Principal (Progreso):", "gpu_fg_color", "#00ccff")
        self.gpu_bg_btn = self.add_color_control(vbox, "Color de Fondo (Anillo base):", "gpu_bg_color", "#1a1a2e")

        vbox.pack_start(Gtk.Separator(), False, False, 5)

        # --- Tamaños ---
        vbox.pack_start(Gtk.Label(label="<b>Tamaños y Estructura</b>", use_markup=True), False, False, 0)
        self.cpu_size_spin = self.add_size_control(vbox, "Tamaño Círculo CPU (px):", "cpu_size", 155)
        self.ram_size_spin = self.add_size_control(vbox, "Tamaño Círculo RAM (px):", "ram_size", 155)
        self.gpu_size_spin = self.add_size_control(vbox, "Tamaño Círculo GPU (px):", "gpu_size", 155)
        self.ring_spin = self.add_size_control(vbox, "Grosor del Anillo (px):", "ring_width", 8)
        self.spacing_spin = self.add_size_control(vbox, "Espaciado entre Círculos (px):", "spacing", 10)
        
        # Posición de la GPU
        vbox.pack_start(Gtk.Label(label="<b>Posición de la GPU</b>", use_markup=True), False, False, 0)
        
        pos_grid = Gtk.Grid()
        pos_grid.set_column_spacing(15)
        pos_grid.set_row_spacing(10)
        
        self.btn_tl = Gtk.RadioButton.new_with_label_from_widget(None, "↖ Arriba Izquierda")
        self.btn_tr = Gtk.RadioButton.new_with_label_from_widget(self.btn_tl, "↗ Arriba Derecha")
        self.btn_bl = Gtk.RadioButton.new_with_label_from_widget(self.btn_tl, "↙ Abajo Izquierda")
        self.btn_br = Gtk.RadioButton.new_with_label_from_widget(self.btn_tl, "↘ Abajo Derecha")
        
        current_orient = self.config.get("orientation", "bottom-right")
        # Compatibilidad con configs anteriores
        if current_orient == "izquierda": current_orient = "bottom-left"
        elif current_orient in ("arriba", "abajo", "derecha"): current_orient = "bottom-right"

        if current_orient == "top-left": self.btn_tl.set_active(True)
        elif current_orient == "top-right": self.btn_tr.set_active(True)
        elif current_orient == "bottom-left": self.btn_bl.set_active(True)
        else: self.btn_br.set_active(True)

        self.btn_tl.connect("toggled", self.on_changed)
        self.btn_tr.connect("toggled", self.on_changed)
        self.btn_bl.connect("toggled", self.on_changed)
        self.btn_br.connect("toggled", self.on_changed)

        pos_grid.attach(self.btn_tl, 0, 0, 1, 1)
        pos_grid.attach(self.btn_tr, 1, 0, 1, 1)
        pos_grid.attach(self.btn_bl, 0, 1, 1, 1)
        pos_grid.attach(self.btn_br, 1, 1, 1, 1)

        vbox.pack_start(pos_grid, False, False, 0)

        vbox.pack_start(Gtk.Separator(), False, False, 5)

        # --- Fuente ---
        vbox.pack_start(Gtk.Label(label="<b>Tipografía</b>", use_markup=True), False, False, 0)
        
        hbox_font = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=7)
        hbox_font.pack_start(Gtk.Label(label="Familia de Fuente:"), False, False, 0)
        self.font_combo = Gtk.ComboBoxText()
        
        font_map = PangoCairo.font_map_get_default()
        families = sorted([f.get_name() for f in font_map.list_families()])
        for family in families:
            self.font_combo.append_text(family)
            
        current_font = self.config.get("font_family", "Inter")
        if current_font in families:
            self.font_combo.set_active(families.index(current_font))
            
        self.font_combo.connect("changed", self.on_changed)
        hbox_font.pack_start(self.font_combo, True, True, 0)
        vbox.pack_start(hbox_font, False, False, 0)
        
        self.font_size_spin = self.add_size_control(vbox, "Tamaño de Número (pt):", "font_size", 14)
        self.letter_spacing_spin = self.add_size_control(vbox, "Espaciado entre Letras (px):", "letter_spacing", 2)
        self.text_color_btn = self.add_color_control(vbox, "Color del Texto:", "text_color", "#ffffff")

        vbox.pack_start(Gtk.Separator(), False, False, 10)

        close_btn = Gtk.Button(label="Cerrar Monitor de Recursos")
        close_btn.get_style_context().add_class("close-monitor-button")
        close_btn.connect("clicked", self.on_close_widget)
        vbox.pack_start(close_btn, False, False, 10)

    def add_color_control(self, container, label, config_key, default_hex):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(Gtk.Label(label=label), False, False, 0)
        btn = Gtk.ColorButton()
        btn.set_use_alpha(False)
        btn.set_rgba(rgb_to_gdk(self.config.get(config_key, default_hex)))
        btn.connect("color-set", self.on_changed)
        hbox.pack_start(btn, False, False, 0)
        container.pack_start(hbox, False, False, 0)
        return btn

    def add_size_control(self, container, label_text, config_key, default_val):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(Gtk.Label(label=label_text), False, False, 0)
        spin = Gtk.SpinButton.new_with_range(-50, 1000, 1)
        spin.set_value(int(self.config.get(config_key, default_val)))
        spin.connect("value-changed", self.on_changed)
        hbox.pack_start(spin, False, False, 0)
        container.pack_start(hbox, False, False, 0)
        return spin

    def on_changed(self, widget):
        # Guardamos todos los valores actuales
        def get_hex(btn):
            c = btn.get_rgba()
            return f"#{int(c.red*255):02x}{int(c.green*255):02x}{int(c.blue*255):02x}"
            
        self.config["cpu_fg_color"] = get_hex(self.cpu_fg_btn)
        self.config["cpu_bg_color"] = get_hex(self.cpu_bg_btn)
        self.config["ram_fg_color"] = get_hex(self.ram_fg_btn)
        self.config["ram_bg_color"] = get_hex(self.ram_bg_btn)
        self.config["gpu_fg_color"] = get_hex(self.gpu_fg_btn)
        self.config["gpu_bg_color"] = get_hex(self.gpu_bg_btn)
        
        self.config["text_color"] = get_hex(self.text_color_btn)
        
        self.config["cpu_size"] = int(self.cpu_size_spin.get_value())
        self.config["ram_size"] = int(self.ram_size_spin.get_value())
        self.config["gpu_size"] = int(self.gpu_size_spin.get_value())
        self.config["ring_width"] = int(self.ring_spin.get_value())
        self.config["spacing"] = int(self.spacing_spin.get_value())
        self.config["font_size"] = int(self.font_size_spin.get_value())
        self.config["letter_spacing"] = int(self.letter_spacing_spin.get_value())
        
        active_font = self.font_combo.get_active_text()
        if active_font:
            self.config["font_family"] = active_font
            
        if self.btn_tl.get_active():
            self.config["orientation"] = "top-left"
        elif self.btn_tr.get_active():
            self.config["orientation"] = "top-right"
        elif self.btn_bl.get_active():
            self.config["orientation"] = "bottom-left"
        else:
            self.config["orientation"] = "bottom-right"
        
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    def on_close_widget(self, button):
        os.system("pkill -f resource_widget.py")
        os.system("pkill -f cosmic-resource-widget-rs")

    def apply_css(self):
        try:
            screen = Gdk.Screen.get_default()
            if screen is not None:
                css = b"""
                .close-monitor-button {
                    background-image: none;
                    background-color: #000000;
                    color: #ffffff;
                    border: 2px solid #808080;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                .close-monitor-button:hover {
                    background-image: none;
                    background-color: #d3d3d3;
                    color: #000000;
                    border: 2px solid #000000;
                }
                """
                provider = Gtk.CssProvider()
                provider.load_from_data(css)
                Gtk.StyleContext.add_provider_for_screen(
                    screen,
                    provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el CSS personalizado ({e})", file=sys.stderr)

if __name__ == '__main__':
    win = ConfigApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
