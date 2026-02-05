"""
🗺️ GPS NAVIGATOR PRO - SISTEMA DE NAVEGACIÓN AVANZADO
═══════════════════════════════════════════════════════════════════

Autor: Oscar de la Torre
Versión: 2.0 PRO
Características:
  • Algoritmo de Dijkstra optimizado con cola de prioridad
  • Interfaz gráfica moderna con tema oscuro
  • Base de datos SQLite persistente
  • Visualización gráfica de rutas con NetworkX
  • Historial de búsquedas con exportación CSV
"""

import sqlite3
import heapq
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import networkx as nx
from datetime import datetime
import os
import csv
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════════════════════
# 🎨 CONFIGURACIÓN DE COLORES Y TEMAS
# ═══════════════════════════════════════════════════════════════════════════
class Theme:
    """Tema de colores para la aplicación (Modo oscuro moderno)"""
    
    # Colores de fondo
    BG_DARK = "#1a1a2e"        # Fondo principal (azul muy oscuro)
    BG_MEDIUM = "#16213e"      # Fondo secundario
    BG_LIGHT = "#0f3460"       # Fondo de elementos elevados
    BG_CARD = "#1f4068"        # Fondo de tarjetas
    
    # Colores de acento
    ACCENT_PRIMARY = "#e94560"    # Rojo/Rosa (acciones principales)
    ACCENT_SECONDARY = "#00d9ff"  # Cian (información)
    ACCENT_SUCCESS = "#00ff88"    # Verde (éxito)
    ACCENT_WARNING = "#ffd93d"    # Amarillo (advertencia)
    ACCENT_DANGER = "#ff6b6b"     # Rojo claro (peligro)
    
    # Colores de texto
    TEXT_PRIMARY = "#ffffff"      # Texto principal
    TEXT_SECONDARY = "#b8b8b8"    # Texto secundario
    TEXT_MUTED = "#6c757d"        # Texto desactivado
    
    # Fuentes
    FONT_TITLE = ("Segoe UI", 28, "bold")
    FONT_SUBTITLE = ("Segoe UI", 14)
    FONT_HEADING = ("Segoe UI", 12, "bold")
    FONT_BODY = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 9)
    FONT_MONO = ("Consolas", 10)


# ═══════════════════════════════════════════════════════════════════════════
# 📦 CLASES DE DATOS (DATACLASSES)
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class Ciudad:
    """Representa una ciudad en el sistema"""
    id: int
    nombre: str
    latitud: float
    longitud: float
    poblacion: int
    tipo: str


@dataclass
class Conexion:
    """Representa una conexión entre ciudades"""
    origen: str
    destino: str
    distancia: float
    tiempo: float
    tipo: str
    peaje: bool


@dataclass
class ResultadoRuta:
    """Resultado del cálculo de una ruta"""
    origen: str
    destino: str
    ruta: List[str]
    distancia_total: float
    tiempo_total_min: float
    tiempo_total_horas: float
    num_paradas: int
    velocidad_media: float


# ═══════════════════════════════════════════════════════════════════════════
# 💾 GESTOR DE BASE DE DATOS
# ═══════════════════════════════════════════════════════════════════════════
class DatabaseManager:
    """Gestor de base de datos SQLite con operaciones CRUD"""
    
    def __init__(self, db_name: str = "gps_system.db"):
        # Usar ruta absoluta en el mismo directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, db_name)
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Obtener conexión a la base de datos con row_factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self) -> None:
        """Inicializar esquema de base de datos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de ciudades (nodos)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nodos (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL UNIQUE,
                    latitud REAL,
                    longitud REAL,
                    poblacion INTEGER,
                    tipo TEXT CHECK(tipo IN ('capital', 'ciudad', 'pueblo'))
                )
            ''')
            
            # Tabla de conexiones (aristas)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS aristas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    origen TEXT NOT NULL,
                    destino TEXT NOT NULL,
                    distancia REAL NOT NULL CHECK(distancia > 0),
                    tiempo REAL NOT NULL CHECK(tiempo > 0),
                    tipo TEXT CHECK(tipo IN ('autovia', 'autopista', 'nacional', 'regional')),
                    peaje BOOLEAN DEFAULT 0,
                    unidireccional BOOLEAN DEFAULT 0
                )
            ''')
            
            # Historial de rutas calculadas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_rutas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    origen TEXT NOT NULL,
                    destino TEXT NOT NULL,
                    fecha_hora TEXT NOT NULL,
                    distancia_total REAL NOT NULL,
                    tiempo_total REAL NOT NULL,
                    ruta_nodos TEXT NOT NULL,
                    usuario TEXT DEFAULT 'Usuario'
                )
            ''')
            
            # Índices para mejor rendimiento
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_aristas_origen ON aristas(origen)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_aristas_destino ON aristas(destino)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_nodos_nombre ON nodos(nombre)')
            
            conn.commit()
    
    def get_all_cities(self) -> List[str]:
        """Obtener lista de todas las ciudades ordenadas"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM nodos ORDER BY nombre")
            return [row['nombre'] for row in cursor.fetchall()]
    
    def get_adjacency_list(self, use_distance: bool = True) -> Dict[str, List[Tuple[str, float]]]:
        """Obtener lista de adyacencia del grafo para Dijkstra"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT origen, destino, distancia, tiempo FROM aristas')
            
            graph: Dict[str, List[Tuple[str, float]]] = {}
            for row in cursor.fetchall():
                origen = row['origen']
                destino = row['destino']
                cost = row['distancia'] if use_distance else row['tiempo']
                
                if origen not in graph:
                    graph[origen] = []
                graph[origen].append((destino, cost))
                
                # Asegurar que el destino esté en el grafo
                if destino not in graph:
                    graph[destino] = []
            
            return graph
    
    def get_edge_map(self) -> Dict[Tuple[str, str], Tuple[float, float]]:
        """Obtener mapa de aristas con (distancia, tiempo) para cada conexión"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT origen, destino, distancia, tiempo FROM aristas')
            
            return {
                (row['origen'], row['destino']): (row['distancia'], row['tiempo'])
                for row in cursor.fetchall()
            }
    
    def save_route_history(self, origen: str, destino: str, 
                          distancia: float, tiempo: float, ruta: List[str]) -> None:
        """Guardar ruta calculada en el historial"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO historico_rutas 
                (origen, destino, fecha_hora, distancia_total, tiempo_total, ruta_nodos)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (origen, destino, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  distancia, tiempo, " → ".join(ruta)))
            conn.commit()
    
    def get_route_history(self, limit: int = 10) -> List[Tuple]:
        """Obtener historial de rutas recientes"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT origen, destino, fecha_hora, distancia_total, tiempo_total, ruta_nodos
                FROM historico_rutas ORDER BY fecha_hora DESC LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
    
    def clear_history(self) -> None:
        """Limpiar todo el historial de rutas"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historico_rutas")
            conn.commit()
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas del sistema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM nodos")
            total_cities = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM aristas")
            total_edges = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM historico_rutas")
            total_routes = cursor.fetchone()['count']
            
            cursor.execute("SELECT AVG(distancia_total) as avg FROM historico_rutas")
            avg_distance = cursor.fetchone()['avg'] or 0
            
            cursor.execute("SELECT AVG(tiempo_total) as avg FROM historico_rutas")
            avg_time = cursor.fetchone()['avg'] or 0
            
            return {
                'total_cities': total_cities,
                'total_edges': total_edges,
                'total_routes': total_routes,
                'avg_distance': avg_distance,
                'avg_time': avg_time
            }
    
    def create_sample_data(self) -> None:
        """Crear datos de ejemplo con ciudades españolas"""
        print("🗺️  Generando red de ciudades españolas...")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Limpiar tablas existentes
            cursor.execute("DELETE FROM aristas")
            cursor.execute("DELETE FROM nodos")
            
            # Red de ciudades españolas (35 ciudades principales)
            ciudades = [
                (1, "Madrid", 40.4168, -3.7038, 3223000, "capital"),
                (2, "Barcelona", 41.3851, 2.1734, 1620000, "ciudad"),
                (3, "Valencia", 39.4699, -0.3763, 791000, "ciudad"),
                (4, "Sevilla", 37.3891, -5.9845, 688000, "ciudad"),
                (5, "Zaragoza", 41.6488, -0.8891, 666000, "ciudad"),
                (6, "Málaga", 36.7213, -4.4214, 569000, "ciudad"),
                (7, "Murcia", 37.9922, -1.1307, 447000, "ciudad"),
                (8, "Bilbao", 43.2630, -2.9350, 345000, "ciudad"),
                (9, "Alicante", 38.3452, -0.4810, 332000, "ciudad"),
                (10, "Córdoba", 37.8882, -4.7794, 322000, "ciudad"),
                (11, "Valladolid", 41.6529, -4.7286, 299000, "ciudad"),
                (12, "Vigo", 42.2406, -8.7207, 295000, "ciudad"),
                (13, "Gijón", 43.5322, -5.6611, 271000, "ciudad"),
                (14, "Vitoria", 42.8467, -2.6716, 253000, "ciudad"),
                (15, "Granada", 37.1773, -3.5986, 233000, "ciudad"),
                (16, "Oviedo", 43.3623, -5.8491, 220000, "ciudad"),
                (17, "Pamplona", 42.8125, -1.6458, 198000, "ciudad"),
                (18, "Almería", 36.8402, -2.4679, 200000, "ciudad"),
                (19, "San Sebastián", 43.3183, -1.9812, 188000, "ciudad"),
                (20, "Santander", 43.4628, -3.8050, 172000, "ciudad"),
                (21, "Castellón", 39.9864, -0.0513, 171000, "ciudad"),
                (22, "Burgos", 42.3439, -3.6969, 176000, "ciudad"),
                (23, "Albacete", 38.9956, -1.8558, 172000, "ciudad"),
                (24, "Salamanca", 40.9644, -5.6631, 144000, "ciudad"),
                (25, "Logroño", 42.4667, -2.4500, 152000, "ciudad"),
                (26, "Huelva", 37.2583, -6.9508, 144000, "ciudad"),
                (27, "Ciudad Real", 38.9848, -3.9275, 75000, "ciudad"),
                (28, "Toledo", 39.8568, -4.0245, 84000, "ciudad"),
                (29, "Jaén", 37.7796, -3.7849, 113000, "ciudad"),
                (30, "Lleida", 41.6167, 0.6333, 138000, "ciudad"),
                (31, "Cádiz", 36.5350, -6.2975, 116000, "ciudad"),
                (32, "Tarragona", 41.1167, 1.2500, 132000, "ciudad"),
                (33, "Girona", 41.9833, 2.8167, 101000, "ciudad"),
                (34, "Badajoz", 38.8794, -6.9707, 150000, "ciudad"),
                (35, "Cáceres", 39.4765, -6.3722, 96000, "ciudad"),
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO nodos (id, nombre, latitud, longitud, poblacion, tipo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ciudades)
            
            # Conexiones de carretera (origen, destino, km, minutos, tipo, peaje)
            conexiones = [
                # Madrid - Hub central
                ("Madrid", "Barcelona", 621, 360, "autopista", 1),
                ("Madrid", "Valencia", 355, 210, "autovia", 0),
                ("Madrid", "Sevilla", 538, 325, "autopista", 1),
                ("Madrid", "Zaragoza", 325, 195, "autovia", 0),
                ("Madrid", "Toledo", 70, 42, "autovia", 0),
                ("Madrid", "Ciudad Real", 180, 110, "autovia", 0),
                ("Madrid", "Albacete", 250, 150, "autovia", 0),
                ("Madrid", "Burgos", 237, 142, "autovia", 0),
                ("Madrid", "Valladolid", 193, 116, "autovia", 0),
                ("Madrid", "Salamanca", 210, 125, "autovia", 0),
                ("Madrid", "Vigo", 600, 360, "autopista", 1),
                
                # Barcelona - Hub mediterráneo
                ("Barcelona", "Valencia", 349, 210, "autopista", 1),
                ("Barcelona", "Zaragoza", 296, 180, "autopista", 1),
                ("Barcelona", "Tarragona", 100, 60, "autopista", 0),
                ("Barcelona", "Girona", 100, 60, "autovia", 0),
                ("Barcelona", "Lleida", 150, 90, "autovia", 0),
                
                # Valencia - Costa mediterránea
                ("Valencia", "Alicante", 166, 100, "autopista", 1),
                ("Valencia", "Castellón", 65, 39, "autovia", 0),
                ("Valencia", "Albacete", 190, 114, "autovia", 0),
                
                # Sevilla - Hub andaluz
                ("Sevilla", "Córdoba", 138, 83, "autopista", 0),
                ("Sevilla", "Málaga", 205, 125, "autopista", 1),
                ("Sevilla", "Huelva", 92, 55, "autovia", 0),
                ("Sevilla", "Cádiz", 125, 75, "autovia", 0),
                ("Sevilla", "Badajoz", 200, 120, "autovia", 0),
                
                # Zaragoza - Conexiones
                ("Zaragoza", "Pamplona", 180, 108, "autovia", 0),
                ("Zaragoza", "Burgos", 234, 140, "autovia", 0),
                ("Zaragoza", "Lleida", 150, 90, "autovia", 0),
                
                # País Vasco - Norte
                ("Bilbao", "San Sebastián", 118, 71, "autopista", 0),
                ("Bilbao", "Vitoria", 66, 40, "autovia", 0),
                ("Bilbao", "Burgos", 159, 95, "autovia", 0),
                ("Bilbao", "Santander", 107, 65, "autovia", 0),
                
                # Asturias - Cantabria
                ("Oviedo", "Gijón", 28, 17, "autovia", 0),
                ("Oviedo", "Santander", 204, 125, "autovia", 0),
                ("Gijón", "Bilbao", 304, 182, "autovia", 0),
                
                # Castilla y León
                ("Valladolid", "Salamanca", 115, 70, "autovia", 0),
                ("Valladolid", "Burgos", 122, 73, "autovia", 0),
                
                # Andalucía interior
                ("Málaga", "Granada", 129, 77, "autovia", 0),
                ("Málaga", "Almería", 215, 129, "autopista", 1),
                ("Granada", "Jaén", 98, 59, "autovia", 0),
                ("Granada", "Almería", 167, 100, "autovia", 0),
                ("Córdoba", "Jaén", 105, 63, "autovia", 0),
                ("Córdoba", "Ciudad Real", 200, 120, "autovia", 0),
                
                # Levante
                ("Alicante", "Murcia", 78, 47, "autovia", 0),
                ("Murcia", "Albacete", 150, 90, "autovia", 0),
                ("Murcia", "Almería", 220, 130, "autopista", 1),
                
                # La Rioja - Navarra
                ("Pamplona", "Logroño", 90, 54, "autovia", 0),
                ("Logroño", "Burgos", 120, 72, "autovia", 0),
                
                # Extremadura
                ("Badajoz", "Cáceres", 90, 54, "autovia", 0),
                ("Cáceres", "Salamanca", 200, 120, "autovia", 0),
                
                # Toledo - Córdoba
                ("Toledo", "Ciudad Real", 120, 72, "autovia", 0),
                ("Toledo", "Córdoba", 300, 180, "autovia", 0),
            ]
            
            # Insertar conexiones bidireccionales
            for origen, destino, dist, tiempo, tipo, peaje in conexiones:
                # Dirección A → B
                cursor.execute('''
                    INSERT INTO aristas (origen, destino, distancia, tiempo, tipo, peaje)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (origen, destino, dist, tiempo, tipo, peaje))
                # Dirección B → A
                cursor.execute('''
                    INSERT INTO aristas (origen, destino, distancia, tiempo, tipo, peaje)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (destino, origen, dist, tiempo, tipo, peaje))
            
            conn.commit()
            print(f"✅ Creados: {len(ciudades)} ciudades, {len(conexiones) * 2} conexiones")


# ═══════════════════════════════════════════════════════════════════════════
# 🔍 ALGORITMO DE DIJKSTRA OPTIMIZADO
# ═══════════════════════════════════════════════════════════════════════════
class DijkstraRouter:
    """Implementación optimizada del algoritmo de Dijkstra con cola de prioridad"""
    
    def __init__(self, adjacency_list: Dict[str, List[Tuple[str, float]]]):
        self.graph = adjacency_list
    
    def find_shortest_path(self, start: str, end: str) -> Optional[Tuple[float, List[str]]]:
        """
        Encontrar el camino más corto entre dos nodos usando Dijkstra.
        
        Args:
            start: Nodo de origen
            end: Nodo de destino
            
        Returns:
            Tupla (costo_total, [lista_de_nodos]) o None si no hay ruta
        """
        if start not in self.graph:
            return None
        
        # Inicialización de estructuras
        distances = {node: float('inf') for node in self.graph}
        previous = {node: None for node in self.graph}
        distances[start] = 0
        
        # Cola de prioridad: (distancia, nodo)
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            # Saltar si ya fue visitado
            if current in visited:
                continue
            
            visited.add(current)
            
            # Si llegamos al destino, terminamos
            if current == end:
                break
            
            # Explorar vecinos
            for neighbor, weight in self.graph.get(current, []):
                if neighbor in visited:
                    continue
                
                # Asegurar que el vecino esté en las estructuras
                if neighbor not in distances:
                    distances[neighbor] = float('inf')
                    previous[neighbor] = None
                
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        # Verificar si se encontró ruta
        if end not in distances or distances[end] == float('inf'):
            return None
        
        # Reconstruir el camino
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        return distances[end], path


# ═══════════════════════════════════════════════════════════════════════════
# 🎨 WIDGETS PERSONALIZADOS
# ═══════════════════════════════════════════════════════════════════════════
class ModernButton(tk.Canvas):
    """Botón moderno con efectos hover y diseño personalizado"""
    
    def __init__(self, parent, text: str, command=None, 
                 bg: str = Theme.ACCENT_PRIMARY, 
                 fg: str = Theme.TEXT_PRIMARY,
                 width: int = 200, height: int = 40, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=Theme.BG_CARD, **kwargs)
        
        self.command = command
        self.bg_normal = bg
        self.bg_hover = self._lighten_color(bg, 20)
        self.bg_click = self._darken_color(bg, 20)
        self.fg = fg
        self.width = width
        self.height = height
        self.text = text
        
        self._draw_button(self.bg_normal)
        
        # Eventos
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _draw_button(self, bg_color: str):
        """Dibujar el botón con bordes redondeados"""
        self.delete("all")
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                                radius=10, fill=bg_color, outline="")
        self.create_text(self.width//2, self.height//2, text=self.text,
                        fill=self.fg, font=Theme.FONT_BODY)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Crear rectángulo con bordes redondeados"""
        points = [
            x1 + radius, y1, x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _lighten_color(self, color: str, percent: int) -> str:
        """Aclarar un color hexadecimal"""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = min(255, r + percent)
        g = min(255, g + percent)
        b = min(255, b + percent)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _darken_color(self, color: str, percent: int) -> str:
        """Oscurecer un color hexadecimal"""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = max(0, r - percent)
        g = max(0, g - percent)
        b = max(0, b - percent)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _on_enter(self, event):
        self._draw_button(self.bg_hover)
        self.config(cursor="hand2")
    
    def _on_leave(self, event):
        self._draw_button(self.bg_normal)
    
    def _on_click(self, event):
        self._draw_button(self.bg_click)
    
    def _on_release(self, event):
        self._draw_button(self.bg_hover)
        if self.command:
            self.command()


class ModernCard(tk.Frame):
    """Tarjeta con estilo moderno para agrupar contenido"""
    
    def __init__(self, parent, title: str = "", **kwargs):
        super().__init__(parent, bg=Theme.BG_CARD, **kwargs)
        
        if title:
            title_label = tk.Label(self, text=title, 
                                  font=Theme.FONT_HEADING,
                                  bg=Theme.BG_CARD, 
                                  fg=Theme.ACCENT_SECONDARY)
            title_label.pack(anchor="w", padx=15, pady=(15, 10))
            
            # Línea separadora
            separator = tk.Frame(self, height=2, bg=Theme.ACCENT_SECONDARY)
            separator.pack(fill="x", padx=15, pady=(0, 10))


class AnimatedLabel(tk.Label):
    """Label con capacidad de efectos de animación"""
    
    def __init__(self, parent, **kwargs):
        kwargs.setdefault('bg', Theme.BG_DARK)
        kwargs.setdefault('fg', Theme.TEXT_PRIMARY)
        super().__init__(parent, **kwargs)
        self._animation_id = None
    
    def flash(self, color: str = Theme.ACCENT_SUCCESS, duration: int = 500):
        """Efecto de flash temporal"""
        original_bg = self.cget('bg')
        self.config(bg=color)
        self.after(duration, lambda: self.config(bg=original_bg))


# ═══════════════════════════════════════════════════════════════════════════
# 🖥️ APLICACIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════
class GPSApp:
    """Aplicación GPS con interfaz gráfica moderna"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🗺️ GPS Navigator Pro - Dijkstra Algorithm")
        self.root.geometry("1400x900")
        self.root.configure(bg=Theme.BG_DARK)
        self.root.minsize(1200, 700)
        
        # Variables de control
        self.use_distance = tk.BooleanVar(value=True)
        self.show_graph_var = tk.BooleanVar(value=False)
        self.auto_calculate = tk.BooleanVar(value=False)
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        
        # Verificar y cargar datos
        cities = self.db.get_all_cities()
        if not cities:
            self.db.create_sample_data()
            cities = self.db.get_all_cities()
        
        self.cities = cities
        self._refresh_graph_data()
        
        # Construir interfaz
        self._setup_styles()
        self._build_ui()
        self._load_history()
        
        # Centrar ventana
        self._center_window()
    
    def _center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _refresh_graph_data(self):
        """Actualizar datos del grafo desde la BD"""
        self.graph_data = self.db.get_adjacency_list(self.use_distance.get())
        self.edge_map = self.db.get_edge_map()
        self.router = DijkstraRouter(self.graph_data)
        self.edge_count = sum(len(v) for v in self.graph_data.values())
    
    def _setup_styles(self):
        """Configurar estilos personalizados de ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilos de frames
        style.configure('Dark.TFrame', background=Theme.BG_DARK)
        style.configure('Card.TFrame', background=Theme.BG_CARD)
        
        # Estilos de labels
        style.configure('Dark.TLabel', 
                       background=Theme.BG_DARK, 
                       foreground=Theme.TEXT_PRIMARY)
        style.configure('Card.TLabel',
                       background=Theme.BG_CARD,
                       foreground=Theme.TEXT_PRIMARY)
        style.configure('Accent.TLabel',
                       background=Theme.BG_CARD,
                       foreground=Theme.ACCENT_SECONDARY,
                       font=Theme.FONT_HEADING)
        
        # Estilos de controles
        style.configure('Dark.TCombobox',
                       fieldbackground=Theme.BG_LIGHT,
                       background=Theme.BG_LIGHT,
                       foreground=Theme.TEXT_PRIMARY)
        style.configure('Dark.TRadiobutton',
                       background=Theme.BG_CARD,
                       foreground=Theme.TEXT_PRIMARY)
        style.configure('Dark.TCheckbutton',
                       background=Theme.BG_CARD,
                       foreground=Theme.TEXT_PRIMARY)
        
        # Estilos de notebook (pestañas)
        style.configure('Dark.TNotebook', background=Theme.BG_DARK)
        style.configure('Dark.TNotebook.Tab',
                       background=Theme.BG_MEDIUM,
                       foreground=Theme.TEXT_PRIMARY,
                       padding=[20, 10])
        style.map('Dark.TNotebook.Tab',
                 background=[('selected', Theme.ACCENT_PRIMARY)],
                 foreground=[('selected', Theme.TEXT_PRIMARY)])
    
    def _build_ui(self):
        """Construir toda la interfaz de usuario"""
        self._build_header()
        
        # Contenedor principal
        main_container = tk.Frame(self.root, bg=Theme.BG_DARK)
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Panel izquierdo (controles)
        left_panel = tk.Frame(main_container, bg=Theme.BG_DARK, width=320)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)
        
        self._build_route_panel(left_panel)
        self._build_config_panel(left_panel)
        self._build_actions_panel(left_panel)
        
        # Panel derecho (resultados)
        right_panel = tk.Frame(main_container, bg=Theme.BG_DARK)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self._build_results_panel(right_panel)
        
        # Barra de estado
        self._build_status_bar()
    
    def _build_header(self):
        """Construir encabezado de la aplicación"""
        header = tk.Frame(self.root, bg=Theme.BG_MEDIUM, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Logo y título
        title_frame = tk.Frame(header, bg=Theme.BG_MEDIUM)
        title_frame.pack(side="left", padx=30, pady=15)
        
        tk.Label(title_frame, text="🗺️", font=("Segoe UI", 32),
                bg=Theme.BG_MEDIUM, fg=Theme.ACCENT_PRIMARY).pack(side="left")
        
        text_frame = tk.Frame(title_frame, bg=Theme.BG_MEDIUM)
        text_frame.pack(side="left", padx=15)
        
        tk.Label(text_frame, text="GPS Navigator Pro",
                font=Theme.FONT_TITLE, bg=Theme.BG_MEDIUM,
                fg=Theme.TEXT_PRIMARY).pack(anchor="w")
        
        tk.Label(text_frame, text="Algoritmo de Dijkstra • Base de Datos SQLite",
                font=Theme.FONT_SMALL, bg=Theme.BG_MEDIUM,
                fg=Theme.TEXT_SECONDARY).pack(anchor="w")
        
        # Panel de información
        info_frame = tk.Frame(header, bg=Theme.BG_MEDIUM)
        info_frame.pack(side="right", padx=30, pady=15)
        
        self.cities_count_label = tk.Label(info_frame, 
                                          text=f"🏙️ {len(self.cities)} ciudades",
                                          font=Theme.FONT_BODY,
                                          bg=Theme.BG_MEDIUM, 
                                          fg=Theme.ACCENT_SUCCESS)
        self.cities_count_label.pack(anchor="e")
        
        self.edges_count_label = tk.Label(info_frame,
                                         text=f"🛣️ {self.edge_count} conexiones",
                                         font=Theme.FONT_BODY,
                                         bg=Theme.BG_MEDIUM,
                                         fg=Theme.ACCENT_SECONDARY)
        self.edges_count_label.pack(anchor="e")
    
    def _build_route_panel(self, parent):
        """Construir panel de selección de ruta"""
        card = ModernCard(parent, title="📍 CALCULAR RUTA")
        card.pack(fill="x", pady=(0, 15))
        
        content = tk.Frame(card, bg=Theme.BG_CARD)
        content.pack(fill="x", padx=15, pady=(0, 15))
        
        # Ciudad de origen
        tk.Label(content, text="Ciudad de origen:",
                font=Theme.FONT_SMALL, bg=Theme.BG_CARD,
                fg=Theme.TEXT_SECONDARY).pack(anchor="w", pady=(0, 5))
        
        self.origin_combo = ttk.Combobox(content, values=self.cities,
                                        font=Theme.FONT_BODY, width=30)
        self.origin_combo.pack(fill="x", pady=(0, 15))
        self.origin_combo.set(self.cities[0] if self.cities else "")
        self.origin_combo.bind('<<ComboboxSelected>>', self._on_selection_change)
        
        # Botón intercambiar
        swap_frame = tk.Frame(content, bg=Theme.BG_CARD)
        swap_frame.pack(fill="x", pady=5)
        
        ModernButton(swap_frame, text="↕️ Intercambiar", 
                    command=self._swap_cities,
                    bg=Theme.BG_LIGHT, width=150, height=30).pack()
        
        # Ciudad de destino
        tk.Label(content, text="Ciudad de destino:",
                font=Theme.FONT_SMALL, bg=Theme.BG_CARD,
                fg=Theme.TEXT_SECONDARY).pack(anchor="w", pady=(15, 5))
        
        self.dest_combo = ttk.Combobox(content, values=self.cities,
                                      font=Theme.FONT_BODY, width=30)
        self.dest_combo.pack(fill="x", pady=(0, 15))
        if len(self.cities) > 1:
            self.dest_combo.set(self.cities[1])
        self.dest_combo.bind('<<ComboboxSelected>>', self._on_selection_change)
        
        # Botón calcular ruta
        ModernButton(content, text="🚀 CALCULAR RUTA ÓPTIMA",
                    command=self._calculate_route,
                    bg=Theme.ACCENT_PRIMARY, 
                    width=280, height=50).pack(pady=10)
    
    def _build_config_panel(self, parent):
        """Construir panel de configuración"""
        card = ModernCard(parent, title="⚙️ CONFIGURACIÓN")
        card.pack(fill="x", pady=(0, 15))
        
        content = tk.Frame(card, bg=Theme.BG_CARD)
        content.pack(fill="x", padx=15, pady=(0, 15))
        
        # Selección de métrica
        tk.Label(content, text="Optimizar por:",
                font=Theme.FONT_SMALL, bg=Theme.BG_CARD,
                fg=Theme.TEXT_SECONDARY).pack(anchor="w", pady=(0, 5))
        
        ttk.Radiobutton(content, text="📏 Distancia (km)",
                       variable=self.use_distance, value=True,
                       style='Dark.TRadiobutton',
                       command=self._on_metric_change).pack(anchor="w", pady=2)
        
        ttk.Radiobutton(content, text="⏱️ Tiempo (minutos)",
                       variable=self.use_distance, value=False,
                       style='Dark.TRadiobutton',
                       command=self._on_metric_change).pack(anchor="w", pady=2)
        
        # Opciones adicionales
        tk.Frame(content, height=10, bg=Theme.BG_CARD).pack()
        
        ttk.Checkbutton(content, text="🔄 Calcular automáticamente",
                       variable=self.auto_calculate,
                       style='Dark.TCheckbutton').pack(anchor="w", pady=2)
        
        ttk.Checkbutton(content, text="📊 Mostrar gráfico",
                       variable=self.show_graph_var,
                       style='Dark.TCheckbutton').pack(anchor="w", pady=2)
    
    def _build_actions_panel(self, parent):
        """Construir panel de acciones"""
        card = ModernCard(parent, title="🎯 ACCIONES")
        card.pack(fill="x", pady=(0, 15))
        
        content = tk.Frame(card, bg=Theme.BG_CARD)
        content.pack(fill="x", padx=15, pady=(0, 15))
        
        buttons = [
            ("📊 Ver Estadísticas", self._show_statistics, Theme.BG_LIGHT),
            ("📋 Ver Historial", self._show_history_window, Theme.BG_LIGHT),
            ("🔄 Recargar Datos", self._reload_data, Theme.BG_LIGHT),
            ("❓ Ayuda", self._show_help, Theme.BG_LIGHT),
        ]
        
        for text, command, color in buttons:
            ModernButton(content, text=text, command=command,
                        bg=color, width=280, height=35).pack(pady=3)
    
    def _build_results_panel(self, parent):
        """Construir panel de resultados con pestañas"""
        notebook = ttk.Notebook(parent, style='Dark.TNotebook')
        notebook.pack(fill="both", expand=True)
        
        # Pestaña de resultados
        results_frame = tk.Frame(notebook, bg=Theme.BG_CARD)
        notebook.add(results_frame, text="  📝 Resultados  ")
        
        self.result_text = scrolledtext.ScrolledText(
            results_frame,
            font=Theme.FONT_MONO,
            bg=Theme.BG_DARK,
            fg=Theme.TEXT_PRIMARY,
            insertbackground=Theme.ACCENT_PRIMARY,
            wrap="word",
            padx=15,
            pady=15
        )
        self.result_text.pack(fill="both", expand=True)
        self._show_welcome_message()
        
        # Pestaña de estadísticas
        stats_frame = tk.Frame(notebook, bg=Theme.BG_CARD)
        notebook.add(stats_frame, text="  📊 Estadísticas  ")
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            font=Theme.FONT_BODY,
            bg=Theme.BG_DARK,
            fg=Theme.TEXT_PRIMARY,
            wrap="word",
            padx=15,
            pady=15
        )
        self.stats_text.pack(fill="both", expand=True)
        
        # Pestaña de historial
        history_frame = tk.Frame(notebook, bg=Theme.BG_CARD)
        notebook.add(history_frame, text="  🕐 Historial  ")
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            font=Theme.FONT_MONO,
            bg=Theme.BG_DARK,
            fg=Theme.TEXT_PRIMARY,
            wrap="word",
            padx=15,
            pady=15
        )
        self.history_text.pack(fill="both", expand=True)
    
    def _build_status_bar(self):
        """Construir barra de estado inferior"""
        status_bar = tk.Frame(self.root, bg=Theme.BG_MEDIUM, height=30)
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)
        
        self.status_label = AnimatedLabel(status_bar,
                                         text="✅ Sistema listo. Seleccione origen y destino.",
                                         font=Theme.FONT_SMALL,
                                         bg=Theme.BG_MEDIUM,
                                         fg=Theme.TEXT_SECONDARY)
        self.status_label.pack(side="left", padx=15, pady=5)
        
        # Reloj
        self.time_label = tk.Label(status_bar,
                                  text="",
                                  font=Theme.FONT_SMALL,
                                  bg=Theme.BG_MEDIUM,
                                  fg=Theme.TEXT_MUTED)
        self.time_label.pack(side="right", padx=15, pady=5)
        self._update_time()
    
    def _update_time(self):
        """Actualizar reloj de la barra de estado"""
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"🕐 {now}")
        self.root.after(1000, self._update_time)
    
    def _show_welcome_message(self):
        """Mostrar mensaje de bienvenida"""
        welcome = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   🗺️  BIENVENIDO A GPS NAVIGATOR PRO                             ║
║                                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   Este sistema utiliza el algoritmo de Dijkstra para              ║
║   encontrar la ruta más corta entre ciudades españolas.           ║
║                                                                    ║
║   INSTRUCCIONES:                                                   ║
║   ─────────────────────────────────────────────────────────       ║
║   1. Seleccione la ciudad de origen                               ║
║   2. Seleccione la ciudad de destino                              ║
║   3. Pulse "CALCULAR RUTA ÓPTIMA"                                 ║
║                                                                    ║
║   CARACTERÍSTICAS:                                                 ║
║   ─────────────────────────────────────────────────────────       ║
║   • Optimización por distancia o tiempo                           ║
║   • Visualización gráfica de rutas                                ║
║   • Historial de búsquedas                                        ║
║   • Exportación a CSV                                             ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════╝
"""
        self.result_text.insert("1.0", welcome)
    
    def _swap_cities(self):
        """Intercambiar ciudades de origen y destino"""
        origen = self.origin_combo.get()
        destino = self.dest_combo.get()
        self.origin_combo.set(destino)
        self.dest_combo.set(origen)
        
        if self.auto_calculate.get():
            self._calculate_route()
    
    def _on_selection_change(self, event=None):
        """Evento al cambiar la selección de ciudades"""
        if self.auto_calculate.get():
            self._calculate_route()
    
    def _on_metric_change(self):
        """Evento al cambiar la métrica de optimización"""
        self._refresh_graph_data()
        metric = "DISTANCIA" if self.use_distance.get() else "TIEMPO"
        self.status_label.config(text=f"✅ Métrica cambiada a: {metric}")
        self.status_label.flash(Theme.ACCENT_SUCCESS, 300)
        
        if self.auto_calculate.get():
            self._calculate_route()
    
    def _compute_route_totals(self, ruta: List[str]) -> Tuple[float, float]:
        """Calcular distancia y tiempo totales de una ruta"""
        total_distance = 0.0
        total_time = 0.0
        
        for i in range(len(ruta) - 1):
            edge = self.edge_map.get((ruta[i], ruta[i + 1]))
            if edge:
                total_distance += edge[0]
                total_time += edge[1]
        
        return total_distance, total_time
    
    def _calculate_route(self):
        """Calcular y mostrar la ruta óptima"""
        origen = self.origin_combo.get()
        destino = self.dest_combo.get()
        
        # Validaciones
        if not origen or not destino:
            messagebox.showwarning("⚠️ Datos incompletos",
                                 "Por favor, seleccione origen y destino.")
            return
        
        if origen == destino:
            messagebox.showwarning("⚠️ Error",
                                 "El origen y destino deben ser diferentes.")
            return
        
        self.status_label.config(text=f"🔍 Calculando ruta: {origen} → {destino}...")
        self.root.update()
        
        try:
            result = self.router.find_shortest_path(origen, destino)
            
            if result is None:
                self._show_no_route_found(origen, destino)
                return
            
            cost, ruta = result
            total_distance, total_time_min = self._compute_route_totals(ruta)
            
            # Crear objeto resultado
            resultado = ResultadoRuta(
                origen=origen,
                destino=destino,
                ruta=ruta,
                distancia_total=total_distance,
                tiempo_total_min=total_time_min,
                tiempo_total_horas=total_time_min / 60,
                num_paradas=len(ruta) - 2,
                velocidad_media=total_distance / (total_time_min / 60) if total_time_min > 0 else 0
            )
            
            # Guardar en historial
            self.db.save_route_history(origen, destino, total_distance, 
                                       resultado.tiempo_total_horas, ruta)
            
            # Mostrar resultados
            self._display_results(resultado)
            self._update_statistics(resultado)
            self._load_history()
            
            # Mostrar gráfico si está activado
            if self.show_graph_var.get():
                self._show_route_graph(ruta)
            
            # Actualizar estado
            self.status_label.config(
                text=f"✅ Ruta encontrada: {len(ruta)} ciudades, "
                     f"{total_distance:.0f} km, {resultado.tiempo_total_horas:.1f}h"
            )
            self.status_label.flash(Theme.ACCENT_SUCCESS, 300)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al calcular la ruta:\n{str(e)}")
            self.status_label.config(text="❌ Error en el cálculo")
    
    def _show_no_route_found(self, origen: str, destino: str):
        """Mostrar mensaje cuando no se encuentra ruta"""
        self.result_text.delete("1.0", "end")
        message = f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   ❌ NO SE ENCONTRÓ RUTA DISPONIBLE                               ║
║                                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   Origen:  {origen:<50}║
║   Destino: {destino:<50}║
║                                                                    ║
║   No existe una conexión entre estas ciudades en la red.          ║
║                                                                    ║
║   Posibles soluciones:                                            ║
║   • Verifique que ambas ciudades estén en la red                  ║
║   • Recargue los datos del sistema                                ║
║   • Seleccione ciudades diferentes                                ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════╝
"""
        self.result_text.insert("1.0", message)
        self.status_label.config(text=f"❌ No existe ruta entre {origen} y {destino}")
    
    def _display_results(self, resultado: ResultadoRuta):
        """Mostrar resultados detallados de la ruta"""
        self.result_text.delete("1.0", "end")
        
        output = """
╔══════════════════════════════════════════════════════════════════╗
║                    🎯 RUTA ÓPTIMA ENCONTRADA                      ║
╚══════════════════════════════════════════════════════════════════╝

"""
        
        # Información principal
        output += f"""┌─────────────────────────────────────────────────────────────────┐
│ 📍 INFORMACIÓN DE LA RUTA                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  🚩 Origen:           {resultado.origen:<40}│
│  🏁 Destino:          {resultado.destino:<40}│
│                                                                   │
│  📏 Distancia total:  {resultado.distancia_total:>8.1f} km                              │
│  ⏱️  Tiempo total:     {resultado.tiempo_total_min:>8.1f} min ({resultado.tiempo_total_horas:.1f} horas)             │
│  🚗 Velocidad media:  {resultado.velocidad_media:>8.1f} km/h                            │
│  🔄 Paradas:          {resultado.num_paradas:>8} ciudades intermedias             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

"""
        
        # Detalle del recorrido
        output += """┌─────────────────────────────────────────────────────────────────┐
│ 🛣️  DETALLE DE LA RUTA                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
"""
        
        for i, ciudad in enumerate(resultado.ruta):
            if i == 0:
                icon = "🚩"
                label = "INICIO"
            elif i == len(resultado.ruta) - 1:
                icon = "🏁"
                label = "FINAL "
            else:
                icon = "📍"
                label = f"  {i:2d}  "
            
            output += f"│  {icon} {label}  →  {ciudad:<45}│\n"
            
            # Mostrar distancia y tiempo al siguiente tramo
            if i < len(resultado.ruta) - 1:
                edge = self.edge_map.get((ciudad, resultado.ruta[i + 1]))
                if edge:
                    output += f"│       ↓      ({edge[0]:.0f} km, {edge[1]:.0f} min)                              │\n"
        
        output += """│                                                                   │
└─────────────────────────────────────────────────────────────────┘

"""
        
        # Consejos de viaje
        output += """┌─────────────────────────────────────────────────────────────────┐
│ 💡 CONSEJOS PARA EL VIAJE                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  • Consulte el estado del tráfico antes de salir                 │
│  • Descanse cada 2 horas de conducción                           │
│  • Tenga en cuenta posibles peajes en autopistas                 │
│  • Lleve combustible suficiente para el trayecto                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
"""
        
        self.result_text.insert("1.0", output)
    
    def _update_statistics(self, resultado: ResultadoRuta):
        """Actualizar pestaña de estadísticas con el último resultado"""
        self.stats_text.delete("1.0", "end")
        
        output = f"""
📊 ESTADÍSTICAS DE LA RUTA ACTUAL
{'═' * 50}

📈 MÉTRICAS PRINCIPALES:
─────────────────────────────────────────────────
• Ciudades en la ruta:     {len(resultado.ruta)}
• Distancia total:         {resultado.distancia_total:.1f} km
• Tiempo estimado:         {resultado.tiempo_total_horas:.1f} horas
• Velocidad media:         {resultado.velocidad_media:.1f} km/h
• Distancia por tramo:     {resultado.distancia_total / max(len(resultado.ruta) - 1, 1):.1f} km

📊 ANÁLISIS DE LA RUTA:
─────────────────────────────────────────────────
"""
        
        # Clasificación del viaje
        if resultado.tiempo_total_horas < 1:
            output += "• ⚡ Viaje corto (menos de 1 hora)\n"
        elif resultado.tiempo_total_horas < 3:
            output += "• 🚗 Viaje medio (1-3 horas)\n"
        elif resultado.tiempo_total_horas < 6:
            output += "• 🛣️ Viaje largo (3-6 horas)\n"
        else:
            output += "• 🏔️ Viaje muy largo (más de 6 horas)\n"
        
        if len(resultado.ruta) == 2:
            output += "• 🎯 Conexión directa\n"
        elif len(resultado.ruta) <= 4:
            output += "• 📍 Pocas paradas intermedias\n"
        else:
            output += "• 🔄 Múltiples paradas intermedias\n"
        
        self.stats_text.insert("1.0", output)
    
    def _load_history(self):
        """Cargar historial de rutas en la pestaña correspondiente"""
        history = self.db.get_route_history(15)
        self.history_text.delete("1.0", "end")
        
        if not history:
            self.history_text.insert("1.0", "\n  🕐 No hay rutas en el historial\n")
            return
        
        output = """
🕐 HISTORIAL DE RUTAS RECIENTES
════════════════════════════════════════════════════════════════

"""
        
        for i, (origen, destino, fecha, distancia, tiempo, ruta) in enumerate(history, 1):
            output += f"""  {i:2d}. {fecha}
      📍 {origen} → {destino}
      📏 {distancia:.1f} km  |  ⏱️ {tiempo:.1f} h
      🛣️ {ruta[:60]}{'...' if len(ruta) > 60 else ''}

"""
        
        self.history_text.insert("1.0", output)
    
    def _show_route_graph(self, ruta: List[str]):
        """Mostrar visualización gráfica de la ruta"""
        try:
            graph_window = tk.Toplevel(self.root)
            graph_window.title("📊 Visualización de Ruta")
            graph_window.geometry("900x700")
            graph_window.configure(bg=Theme.BG_DARK)
            
            fig = Figure(figsize=(10, 8), facecolor=Theme.BG_DARK)
            ax = fig.add_subplot(111)
            ax.set_facecolor(Theme.BG_MEDIUM)
            
            # Crear grafo con NetworkX
            G = nx.Graph()
            for i in range(len(ruta) - 1):
                edge = self.edge_map.get((ruta[i], ruta[i + 1]))
                if edge:
                    G.add_edge(ruta[i], ruta[i + 1], weight=edge[0])
            
            pos = nx.spring_layout(G, seed=42, k=2)
            
            # Dibujar grafo
            nx.draw_networkx_nodes(G, pos, ax=ax, node_size=2000,
                                  node_color=Theme.ACCENT_SECONDARY, alpha=0.9)
            nx.draw_networkx_edges(G, pos, ax=ax, width=3,
                                  edge_color=Theme.ACCENT_PRIMARY, alpha=0.8)
            nx.draw_networkx_labels(G, pos, ax=ax, font_size=9,
                                   font_color='white', font_weight='bold')
            
            # Etiquetas de peso
            edge_labels = nx.get_edge_attributes(G, 'weight')
            edge_labels = {k: f"{v:.0f} km" for k, v in edge_labels.items()}
            nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax,
                                        font_size=8, font_color=Theme.ACCENT_WARNING)
            
            ax.set_title(f'Ruta: {ruta[0]} → {ruta[-1]}',
                        color='white', fontsize=14, fontweight='bold', pad=20)
            ax.axis('off')
            
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
            ModernButton(graph_window, text="Cerrar",
                        command=graph_window.destroy,
                        bg=Theme.ACCENT_DANGER, width=150).pack(pady=10)
            
        except Exception as e:
            messagebox.showwarning("⚠️ Advertencia",
                                 f"No se pudo generar el gráfico:\n{str(e)}")
    
    def _show_statistics(self):
        """Mostrar ventana de estadísticas del sistema"""
        stats = self.db.get_stats()
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Estadísticas del Sistema")
        stats_window.geometry("600x500")
        stats_window.configure(bg=Theme.BG_DARK)
        
        text = scrolledtext.ScrolledText(stats_window, font=Theme.FONT_BODY,
                                        bg=Theme.BG_DARK, fg=Theme.TEXT_PRIMARY,
                                        padx=20, pady=20)
        text.pack(fill="both", expand=True, padx=10, pady=10)
        
        output = f"""
📊 ESTADÍSTICAS DEL SISTEMA GPS
{'═' * 50}

🌍 DATOS GEOGRÁFICOS:
─────────────────────────────────────────────────
• Ciudades en la red:      {stats['total_cities']}
• Conexiones totales:      {stats['total_edges']}
• Densidad de la red:      {stats['total_edges'] / max(stats['total_cities'], 1):.2f} conexiones/ciudad

📈 HISTORIAL DE USO:
─────────────────────────────────────────────────
• Rutas calculadas:        {stats['total_routes']}
• Distancia promedio:      {stats['avg_distance']:.1f} km
• Tiempo promedio:         {stats['avg_time']:.1f} horas

⚙️ CONFIGURACIÓN ACTUAL:
─────────────────────────────────────────────────
• Métrica principal:       {'Distancia (km)' if self.use_distance.get() else 'Tiempo (min)'}
• Cálculo automático:      {'Activado' if self.auto_calculate.get() else 'Desactivado'}
• Mostrar gráficos:        {'Activado' if self.show_graph_var.get() else 'Desactivado'}

🔧 INFORMACIÓN TÉCNICA:
─────────────────────────────────────────────────
• Algoritmo:               Dijkstra (cola de prioridad)
• Base de datos:           SQLite 3
• Interfaz:                Tkinter con tema oscuro
"""
        
        text.insert("1.0", output)
        text.config(state="disabled")
        
        ModernButton(stats_window, text="Cerrar",
                    command=stats_window.destroy,
                    bg=Theme.ACCENT_PRIMARY).pack(pady=10)
    
    def _show_history_window(self):
        """Mostrar ventana completa de historial"""
        history_window = tk.Toplevel(self.root)
        history_window.title("🕐 Historial Completo")
        history_window.geometry("900x600")
        history_window.configure(bg=Theme.BG_DARK)
        
        # Obtener todo el historial
        with self.db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historico_rutas ORDER BY fecha_hora DESC")
            history = cursor.fetchall()
        
        # Frame para la tabla
        tree_frame = tk.Frame(history_window, bg=Theme.BG_DARK)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ("ID", "Origen", "Destino", "Fecha", "Distancia", "Tiempo")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                           yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100 if col != "Fecha" else 150)
        
        for row in history:
            tree.insert("", "end", values=(
                row[0], row[1], row[2], row[3],
                f"{row[4]:.1f} km", f"{row[5]:.1f} h"
            ))
        
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        # Botones de acción
        button_frame = tk.Frame(history_window, bg=Theme.BG_DARK)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ModernButton(button_frame, text="📥 Exportar CSV",
                    command=lambda: self._export_history(history),
                    bg=Theme.ACCENT_SUCCESS, width=150).pack(side="left", padx=5)
        
        ModernButton(button_frame, text="🗑️ Limpiar",
                    command=self._clear_history,
                    bg=Theme.ACCENT_DANGER, width=150).pack(side="left", padx=5)
        
        ModernButton(button_frame, text="Cerrar",
                    command=history_window.destroy,
                    bg=Theme.BG_LIGHT, width=150).pack(side="right", padx=5)
    
    def _export_history(self, history):
        """Exportar historial a archivo CSV"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Origen", "Destino", "Fecha", 
                                   "Distancia (km)", "Tiempo (h)", "Ruta"])
                    for row in history:
                        writer.writerow(row)
                
                messagebox.showinfo("✅ Éxito", f"Historial exportado a:\n{file_path}")
            except Exception as e:
                messagebox.showerror("❌ Error", f"No se pudo exportar:\n{str(e)}")
    
    def _clear_history(self):
        """Limpiar todo el historial"""
        if messagebox.askyesno("⚠️ Confirmar",
                              "¿Desea borrar todo el historial?"):
            self.db.clear_history()
            self._load_history()
            messagebox.showinfo("✅ Completado", "Historial borrado correctamente.")
    
    def _reload_data(self):
        """Recargar datos de ejemplo"""
        if messagebox.askyesno("🔄 Confirmar",
                              "¿Desea recargar todos los datos?\nEsto sobrescribirá la red actual."):
            self.db.create_sample_data()
            self.cities = self.db.get_all_cities()
            self._refresh_graph_data()
            
            # Actualizar combos
            self.origin_combo['values'] = self.cities
            self.dest_combo['values'] = self.cities
            
            # Actualizar contadores
            self.cities_count_label.config(text=f"🏙️ {len(self.cities)} ciudades")
            self.edges_count_label.config(text=f"🛣️ {self.edge_count} conexiones")
            
            self.status_label.config(text="✅ Datos recargados correctamente")
            self.status_label.flash(Theme.ACCENT_SUCCESS, 300)
            
            messagebox.showinfo("✅ Completado",
                              f"Datos recargados:\n• {len(self.cities)} ciudades\n"
                              f"• {self.edge_count} conexiones")
    
    def _show_help(self):
        """Mostrar ventana de ayuda"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Ayuda")
        help_window.geometry("700x550")
        help_window.configure(bg=Theme.BG_DARK)
        
        text = scrolledtext.ScrolledText(help_window, font=Theme.FONT_BODY,
                                        bg=Theme.BG_DARK, fg=Theme.TEXT_PRIMARY,
                                        padx=20, pady=20)
        text.pack(fill="both", expand=True, padx=10, pady=10)
        
        help_text = """
🗺️ GPS NAVIGATOR PRO - GUÍA DE USO
════════════════════════════════════════════════════════════════

📌 CÓMO USAR EL SISTEMA:
─────────────────────────────────────────────────────────────
1. Seleccione una ciudad de origen en el desplegable superior
2. Seleccione una ciudad de destino en el desplegable inferior
3. Pulse el botón "CALCULAR RUTA ÓPTIMA"
4. Los resultados aparecerán en el panel derecho

⚙️ OPCIONES DE CONFIGURACIÓN:
─────────────────────────────────────────────────────────────
• Distancia: Optimiza la ruta por kilómetros recorridos
• Tiempo: Optimiza la ruta por minutos de viaje
• Cálculo automático: Recalcula al cambiar la selección
• Mostrar gráfico: Visualiza la ruta en un diagrama

🔧 CARACTERÍSTICAS TÉCNICAS:
─────────────────────────────────────────────────────────────
• Algoritmo de Dijkstra con cola de prioridad (heapq)
• Base de datos SQLite para persistencia de datos
• Red de 35+ ciudades españolas principales
• 100+ conexiones de carretera bidireccionales

💡 CONSEJOS DE USO:
─────────────────────────────────────────────────────────────
• Use el botón ↕️ para intercambiar origen y destino
• Consulte el historial para ver rutas anteriores
• Exporte el historial a CSV para análisis externo
• Recargue los datos si encuentra inconsistencias

📞 INFORMACIÓN ADICIONAL:
─────────────────────────────────────────────────────────────
• Verifique que la base de datos esté accesible
• Recargue los datos si hay problemas de conexión
• El sistema crea datos automáticamente si no existen
"""
        
        text.insert("1.0", help_text)
        text.config(state="disabled")
        
        ModernButton(help_window, text="Cerrar",
                    command=help_window.destroy,
                    bg=Theme.ACCENT_PRIMARY).pack(pady=10)
    
    def run(self):
        """Iniciar la aplicación"""
        self.root.mainloop()


# ═══════════════════════════════════════════════════════════════════════════
# 🚀 PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════════
def main():
    """Función principal de inicio"""
    print("=" * 70)
    print("🗺️  GPS NAVIGATOR PRO - SISTEMA DE NAVEGACIÓN AVANZADO")
    print("=" * 70)
    print("\n📊 Características del sistema:")
    print("   • Algoritmo de Dijkstra optimizado con cola de prioridad")
    print("   • Interfaz gráfica moderna con tema oscuro")
    print("   • Base de datos SQLite persistente")
    print("   • 35+ ciudades españolas principales")
    print("   • Visualización gráfica de rutas con NetworkX")
    print("\n⚡ Iniciando aplicación...")
    
    try:
        app = GPSApp()
        app.run()
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        print("   Verifique la instalación de Python y las dependencias.")
        input("\nPresione Enter para salir...")


if __name__ == "__main__":
    main()
