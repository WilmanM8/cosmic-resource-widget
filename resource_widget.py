import gi
import json
import os
import math
import cairo

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk, Gdk, GtkLayerShell, GLib, Gio, Pango, PangoCairo
from resource_api import get_system_stats

CONFIG_DIR = os.path.expanduser("~/.config/cosmic-resource-widget")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DEFAULT_CONFIG = {
    "margin_x": 50,
    "margin_y": 50,
    "ring_width": 8,
    "cpu_size": 155,
    "ram_size": 155,
    "gpu_size": 155,
    "spacing": 10,
    "letter_spacing": 2,
    "font_family": "Inter",
    "font_size": 14,
    "text_color": "#ffffff",
    "cpu_fg_color": "#00ffcc",
    "cpu_bg_color": "#1a1a2e",
    "ram_fg_color": "#ff00cc",
    "ram_bg_color": "#1a1a2e",
    "gpu_fg_color": "#00ccff",
    "gpu_bg_color": "#1a1a2e",
    "orientation": "bottom-right"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(data)
            return config
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def hex_to_rgb(hex_code):
    h = hex_code.lstrip('#')
    if len(h) != 6: return (1, 1, 1)
    return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))


class ResourceCircle(Gtk.DrawingArea):
    """Círculo segmentado futurista con 14 secciones."""
    NUM_SEGMENTS = 14

    def __init__(self, label, config):
        super().__init__()
        self.label = label
        self.config = config
        self.percent = 0.0
        self.temp = 0.0
        self.extra_info = ""
        self.set_app_paintable(True)

    def update_data(self, percent, temp=0.0, extra_info=""):
        self.percent = percent
        self.temp = temp
        self.extra_info = extra_info
        self.queue_draw()

    def do_draw(self, cr):
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        ring_width = self.config.get("ring_width", 8)
        center_x = width / 2.0
        center_y = height / 2.0
        # Dejar margen suficiente para que nada se salga
        margin = ring_width / 2.0 + 4
        radius = min(width, height) / 2.0 - margin

        if radius <= 0:
            return False

        key = self.label.lower()
        bg_rgb = hex_to_rgb(self.config.get(f"{key}_bg_color", "#1a1a2e"))
        fg_rgb = hex_to_rgb(self.config.get(f"{key}_fg_color", "#00ffcc"))
        text_color = hex_to_rgb(self.config.get("text_color", "#ffffff"))
        font_family = self.config.get("font_family", "Inter")

        # --- Dibujar 14 segmentos ---
        n = self.NUM_SEGMENTS
        # Ángulo total por segmento (incluyendo hueco)
        segment_total = (2 * math.pi) / n
        # Hueco entre segmentos (3 grados en radianes)
        gap_angle = 3.0 * math.pi / 180.0
        dash_angle = segment_total - gap_angle

        # Cuántos segmentos iluminar según el porcentaje
        lit = int(round((self.percent / 100.0) * n))

        cr.set_line_width(ring_width)
        cr.set_line_cap(cairo.LINE_CAP_BUTT)

        for i in range(n):
            start = -math.pi / 2 + i * segment_total + gap_angle / 2
            end = start + dash_angle

            if i < lit:
                # Glow LED: 3 capas expandiéndose con opacidad decreciente
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
                for glow_w, glow_a in [(ring_width + 16, 0.06), (ring_width + 10, 0.10), (ring_width + 4, 0.18)]:
                    cr.set_line_width(glow_w)
                    cr.set_source_rgba(fg_rgb[0], fg_rgb[1], fg_rgb[2], glow_a)
                    cr.arc(center_x, center_y, radius, start, end)
                    cr.stroke()
                # Segmento activo sólido
                cr.set_line_cap(cairo.LINE_CAP_BUTT)
                cr.set_line_width(ring_width)
                cr.set_source_rgba(fg_rgb[0], fg_rgb[1], fg_rgb[2], 0.95)
                cr.arc(center_x, center_y, radius, start, end)
                cr.stroke()
            else:
                # Segmento inactivo
                cr.set_source_rgba(bg_rgb[0], bg_rgb[1], bg_rgb[2], 0.5)
                cr.arc(center_x, center_y, radius, start, end)
                cr.stroke()

        # --- Fondo Borroso (Blur) ---
        inner_radius = radius - ring_width / 2.0

        cr.save()
        cr.arc(center_x, center_y, inner_radius, 0, 2 * math.pi)
        cr.clip()

        # Base semitransparente para que el compositor (Wayland) pueda aplicar el blur
        cr.set_source_rgba(0.10, 0.10, 0.13, 0.40)
        cr.paint()

        cr.restore()

        # Borde sutil
        cr.arc(center_x, center_y, inner_radius, 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.06)
        cr.set_line_width(0.8)
        cr.stroke()

        # --- Texto dentro del círculo ---
        # Usamos el diámetro del cuadrado inscrito en el círculo interno
        usable_size = inner_radius * math.sqrt(2)

        # Tamaños de fuente proporcionales al espacio interno usable
        main_font_size = max(10, int(usable_size * 0.30))
        label_font_size = max(8, int(usable_size * 0.16))
        temp_font_size = max(7, int(usable_size * 0.13))

        # Crear layouts con letter-spacing
        letter_sp = self.config.get("letter_spacing", 2)
        letter_sp_pango = int(letter_sp * Pango.SCALE)

        attrs = Pango.AttrList()
        attrs.insert(Pango.attr_letter_spacing_new(letter_sp_pango))

        font_main = Pango.FontDescription(f"{font_family} Bold {main_font_size}")
        font_label = Pango.FontDescription(f"{font_family} Bold {label_font_size}")
        font_temp = Pango.FontDescription(f"{font_family} {temp_font_size}")

        # Layout etiqueta (CPU / RAM / GPU)
        layout_label = self.create_pango_layout("")
        layout_label.set_font_description(font_label)
        layout_label.set_attributes(attrs)
        layout_label.set_text(self.label, -1)
        lw, lh = layout_label.get_pixel_size()

        # Layout porcentaje
        layout_pct = self.create_pango_layout("")
        layout_pct.set_font_description(font_main)
        layout_pct.set_attributes(attrs)
        layout_pct.set_text(f"{int(self.percent)}%", -1)
        pw, ph = layout_pct.get_pixel_size()

        # Layout temperatura / info
        temp_text = f"{int(self.temp)}°C" if self.temp > 0 else self.extra_info
        layout_temp = self.create_pango_layout("")
        layout_temp.set_font_description(font_temp)
        layout_temp.set_attributes(attrs)
        layout_temp.set_text(temp_text if temp_text else "", -1)
        tw_t, th_t = layout_temp.get_pixel_size()

        # Calcular posición vertical centrada
        line_gap = 2
        total_h = lh + line_gap + ph
        if temp_text:
            total_h += line_gap + th_t

        y_cursor = center_y - total_h / 2.0

        # Dibujar etiqueta con color del anillo
        cr.move_to(center_x - lw / 2.0, y_cursor)
        cr.set_source_rgba(fg_rgb[0], fg_rgb[1], fg_rgb[2], 0.9)
        PangoCairo.show_layout(cr, layout_label)
        y_cursor += lh + line_gap

        # Dibujar porcentaje en blanco
        cr.move_to(center_x - pw / 2.0, y_cursor)
        cr.set_source_rgba(text_color[0], text_color[1], text_color[2], 1.0)
        PangoCairo.show_layout(cr, layout_pct)
        y_cursor += ph + line_gap

        # Dibujar temperatura / info más tenue
        if temp_text:
            cr.move_to(center_x - tw_t / 2.0, y_cursor)
            cr.set_source_rgba(text_color[0], text_color[1], text_color[2], 0.6)
            PangoCairo.show_layout(cr, layout_temp)

        return False


class ResourceWidget(Gtk.Window):
    def __init__(self):
        super().__init__()

        # Transparencia total
        self.set_visual(self.get_screen().get_rgba_visual())
        self.set_app_paintable(True)

        self.config = load_config()
        self.margin_x = self.config.get("margin_x", 50)
        self.margin_y = self.config.get("margin_y", 50)

        # Determinar si estamos en Wayland mediante GtkLayerShell
        self.is_wayland = GtkLayerShell.is_supported()

        if self.is_wayland:
            GtkLayerShell.init_for_window(self)
            GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BOTTOM)
            GtkLayerShell.set_namespace(self, "resource_widget")

            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, False)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, False)

            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, self.margin_x)
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, self.margin_y)
        else:
            # Fallback para X11 (Pop!_OS por defecto, etc.)
            self.set_type_hint(Gdk.WindowTypeHint.NORMAL)
            self.set_keep_below(True)
            self.set_decorated(False)
            self.set_skip_taskbar_hint(True)
            self.set_skip_pager_hint(True)
            self.set_accept_focus(False)
            self.stick()  # Lo mantiene en todos los escritorios virtuales (desklet real)
            self.move(self.margin_x, self.margin_y)

        # Soporte para arrastrar (Botón izquierdo = arrastrar, Botón derecho = menú)
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.BUTTON1_MOTION_MASK
        )
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_release)
        self.connect("motion-notify-event", self.on_motion_notify)

        self.dragging = False

        self.build_ui()
        self.setup_file_monitor()

        # Actualización de datos cada 1 segundo
        GLib.timeout_add(1000, self.update_data)

    def build_ui(self):
        # Limpiar widget anterior
        child = self.get_child()
        if child:
            self.remove(child)

        spacing = self.config.get("spacing", 10)
        cpu_size = self.config.get("cpu_size", 155)
        ram_size = self.config.get("ram_size", 155)
        gpu_size = self.config.get("gpu_size", 155)
        orientation = self.config.get("orientation", "bottom-right")
        
        # Compatibilidad con configs anteriores
        if orientation == "izquierda": orientation = "bottom-left"
        elif orientation in ("arriba", "abajo", "derecha"): orientation = "bottom-right"

        self.cpu_circle = ResourceCircle("CPU", self.config)
        self.cpu_circle.set_size_request(cpu_size, cpu_size)
        self.ram_circle = ResourceCircle("RAM", self.config)
        self.ram_circle.set_size_request(ram_size, ram_size)
        self.gpu_circle = ResourceCircle("GPU", self.config)
        self.gpu_circle.set_size_request(gpu_size, gpu_size)

        container = Gtk.Grid()
        container.set_column_spacing(spacing)
        container.set_row_spacing(spacing)
        container.set_valign(Gtk.Align.CENTER)
        container.set_halign(Gtk.Align.CENTER)

        if orientation == "top-left":
            container.attach(self.gpu_circle, 0, 0, 1, 1)
            container.attach(self.cpu_circle, 0, 1, 1, 1)
            container.attach(self.ram_circle, 1, 1, 1, 1)
        elif orientation == "top-right":
            container.attach(self.gpu_circle, 1, 0, 1, 1)
            container.attach(self.cpu_circle, 0, 1, 1, 1)
            container.attach(self.ram_circle, 1, 1, 1, 1)
        elif orientation == "bottom-left":
            container.attach(self.cpu_circle, 0, 0, 1, 1)
            container.attach(self.ram_circle, 1, 0, 1, 1)
            container.attach(self.gpu_circle, 0, 1, 1, 1)
        else: # "bottom-right" por defecto
            container.attach(self.cpu_circle, 0, 0, 1, 1)
            container.attach(self.ram_circle, 1, 0, 1, 1)
            container.attach(self.gpu_circle, 1, 1, 1, 1)

        self.add(container)
        self.show_all()

    def update_data(self):
        stats = get_system_stats()
        self.cpu_circle.update_data(stats['cpu'], stats['cpu_temp'])
        ram_info = f"{stats['ram_used_gb']}/{stats['ram_total_gb']}G"
        self.ram_circle.update_data(stats['ram'], extra_info=ram_info)
        self.gpu_circle.update_data(stats['gpu'], stats['gpu_temp'])
        return True

    def setup_file_monitor(self):
        try:
            gfile = Gio.File.new_for_path(CONFIG_FILE)
            self.monitor = gfile.monitor_file(Gio.FileMonitorFlags.NONE, None)
            self.monitor.connect("changed", self.on_config_changed)
        except Exception as e:
            print(f"Advertencia: No se pudo iniciar el monitoreo del archivo de configuración: {e}")

    def on_config_changed(self, monitor, file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT or event_type == Gio.FileMonitorEvent.CREATED:
            GLib.idle_add(self.reload_config)

    def reload_config(self):
        self.config = load_config()
        self.build_ui()
        return False

    def on_button_press(self, widget, event):
        if event.button == 1:
            self.dragging = True
            # Usar is_wayland guardado en __init__
            self.start_x = event.x if getattr(self, 'is_wayland', False) else event.x_root
            self.start_y = event.y if getattr(self, 'is_wayland', False) else event.y_root
            self.start_margin_x = self.margin_x
            self.start_margin_y = self.margin_y
        elif event.button == 3:
            self.show_context_menu(event)
        return True

    def show_context_menu(self, event):
        menu = Gtk.Menu()
        config_item = Gtk.MenuItem(label="⚙️ Configurar Recursos")
        config_item.connect("activate", lambda w: GLib.spawn_command_line_async("gtk-launch cosmic-resource-config"))
        menu.append(config_item)
        quit_item = Gtk.MenuItem(label="❌ Cerrar Monitor")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)
        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)

    def on_button_release(self, widget, event):
        if event.button == 1:
            if getattr(self, 'dragging', False):
                self.dragging = False
                self.config["margin_x"] = self.margin_x
                self.config["margin_y"] = self.margin_y
                save_config(self.config)
        return True

    def on_motion_notify(self, widget, event):
        if getattr(self, 'dragging', False):
            # Mismo cálculo para ambos: margen_inicio + delta desde el click
            if getattr(self, 'is_wayland', False):
                dx = event.x - self.start_x
                dy = event.y - self.start_y
            else:
                dx = event.x_root - self.start_x
                dy = event.y_root - self.start_y

            self.margin_x = max(0, int(self.start_margin_x + dx))
            self.margin_y = max(0, int(self.start_margin_y + dy))

            if getattr(self, 'is_wayland', False):
                GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, self.margin_x)
                GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, self.margin_y)
            else:
                self.move(self.margin_x, self.margin_y)
        return True

if __name__ == '__main__':
    win = ResourceWidget()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
