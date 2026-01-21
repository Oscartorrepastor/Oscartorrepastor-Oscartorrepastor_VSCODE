"""
SISTEMA GPS CON ALGORITMO DE DIJKSTRA
Versión MEJORADA - Interfaz gráfica mejorada y errores corregidos
"""

import sqlite3
import heapq
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
import networkx as nx
from datetime import datetime
import webbrowser

# ============================================================================
# 1. BASE DE DATOS MEJORADA
# ============================================================================
class DatabaseManager:
    def __init__(self, db_name="gps_system.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de nodos (ciudades)
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
        
        # Tabla de aristas (conexiones)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS aristas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origen TEXT NOT NULL,
                destino TEXT NOT NULL,
                distancia REAL NOT NULL CHECK(distancia > 0),
                tiempo REAL NOT NULL CHECK(tiempo > 0),
                tipo TEXT CHECK(tipo IN ('autovia', 'autopista', 'nacional', 'regional')),
                peaje BOOLEAN DEFAULT 0,
                unidireccional BOOLEAN DEFAULT 1
            )
        ''')
        
        # Historial de rutas
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
        
        # Tabla de usuarios (simulada)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                preferencia_metrica TEXT DEFAULT 'distancia'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_sample_data(self):
        """Crea datos de ejemplo completos"""
        print("Creando datos de ejemplo completos...")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Limpiar tablas
        cursor.execute("DELETE FROM aristas")
        cursor.execute("DELETE FROM nodos")
        cursor.execute("DELETE FROM historico_rutas")
        cursor.execute("DELETE FROM usuarios")
        
        # Insertar usuario por defecto
        cursor.execute("INSERT INTO usuarios (nombre, preferencia_metrica) VALUES (?, ?)", 
                      ("Usuario", "distancia"))
        
        # Datos de ciudades españolas con coordenadas aproximadas
        ciudades = [
            # (id, nombre, latitud, longitud, poblacion, tipo)
            (1, "Madrid", 40.4168, -3.7038, 3223000, "capital"),
            (2, "Barcelona", 41.3851, 2.1734, 1620000, "ciudad"),
            (3, "Valencia", 39.4699, -0.3763, 791000, "ciudad"),
            (4, "Sevilla", 37.3891, -5.9845, 688000, "ciudad"),
            (5, "Zaragoza", 41.6488, -0.8891, 666000, "ciudad"),
            (6, "Málaga", 36.7213, -4.4214, 569000, "ciudad"),
            (7, "Murcia", 37.9922, -1.1307, 447000, "ciudad"),
            (8, "Palma", 39.5696, 2.6502, 416000, "ciudad"),
            (9, "Las Palmas", 28.1235, -15.4363, 379000, "ciudad"),
            (10, "Bilbao", 43.2630, -2.9350, 345000, "ciudad"),
            (11, "Alicante", 38.3452, -0.4810, 332000, "ciudad"),
            (12, "Córdoba", 37.8882, -4.7794, 322000, "ciudad"),
            (13, "Valladolid", 41.6529, -4.7286, 299000, "ciudad"),
            (14, "Vigo", 42.2406, -8.7207, 295000, "ciudad"),
            (15, "Gijón", 43.5322, -5.6611, 271000, "ciudad"),
            (16, "Hospitalet", 41.3600, 2.1000, 257000, "ciudad"),
            (17, "Vitoria", 42.8467, -2.6716, 253000, "ciudad"),
            (18, "Granada", 37.1773, -3.5986, 233000, "ciudad"),
            (19, "Elche", 38.2675, -0.6980, 228000, "ciudad"),
            (20, "Oviedo", 43.3623, -5.8491, 220000, "ciudad"),
            (21, "Badalona", 41.4333, 2.2333, 220000, "ciudad"),
            (22, "Cartagena", 37.6057, -0.9913, 214000, "ciudad"),
            (23, "Terrassa", 41.5667, 2.0167, 218000, "ciudad"),
            (24, "Jerez", 36.6817, -6.1378, 213000, "ciudad"),
            (25, "Sabadell", 41.5483, 2.1074, 213000, "ciudad"),
            (26, "Móstoles", 40.3228, -3.8650, 207000, "ciudad"),
            (27, "Alcalá", 40.4817, -3.3643, 196000, "ciudad"),
            (28, "Pamplona", 42.8125, -1.6458, 198000, "ciudad"),
            (29, "Fuenlabrada", 40.2833, -3.8000, 194000, "ciudad"),
            (30, "Almería", 36.8402, -2.4679, 200000, "ciudad"),
            (31, "San Sebastián", 43.3183, -1.9812, 188000, "ciudad"),
            (32, "Leganés", 40.3272, -3.7639, 188000, "ciudad"),
            (33, "Santander", 43.4628, -3.8050, 172000, "ciudad"),
            (34, "Castellón", 39.9864, -0.0513, 171000, "ciudad"),
            (35, "Burgos", 42.3439, -3.6969, 176000, "ciudad"),
            (36, "Albacete", 38.9956, -1.8558, 172000, "ciudad"),
            (37, "Getafe", 40.3047, -3.7322, 183000, "ciudad"),
            (38, "Salamanca", 40.9644, -5.6631, 144000, "ciudad"),
            (39, "Logroño", 42.4667, -2.4500, 152000, "ciudad"),
            (40, "Huelva", 37.2583, -6.9508, 144000, "ciudad"),
            (41, "Ciudad Real", 38.9848, -3.9275, 75000, "ciudad"),
            (42, "Toledo", 39.8568, -4.0245, 84000, "ciudad"),
            (43, "Jaén", 37.7796, -3.7849, 113000, "ciudad"),
            (44, "Lleida", 41.6167, 0.6333, 138000, "ciudad"),
            (45, "Cádiz", 36.5350, -6.2975, 116000, "ciudad"),
            (46, "Tarragona", 41.1167, 1.2500, 132000, "ciudad"),
            (47, "Girona", 41.9833, 2.8167, 101000, "ciudad"),
            (48, "Badajoz", 38.8794, -6.9707, 150000, "ciudad"),
            (49, "Mérida", 38.9161, -6.3436, 59000, "ciudad"),
            (50, "Cáceres", 39.4765, -6.3722, 96000, "ciudad")
        ]
        
        for ciudad in ciudades:
            cursor.execute('''
                INSERT OR IGNORE INTO nodos (id, nombre, latitud, longitud, poblacion, tipo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ciudad)
        
        # Aristas completas y verificadas
        aristas = [
            # Madrid conexiones (todas bidireccionales)
            (1, "Madrid", "Barcelona", 621, 380, "autopista", 1, 0),
            (2, "Barcelona", "Madrid", 621, 380, "autopista", 1, 0),
            (3, "Madrid", "Valencia", 355, 210, "autovia", 0, 0),
            (4, "Valencia", "Madrid", 355, 210, "autovia", 0, 0),
            (5, "Madrid", "Sevilla", 538, 325, "autopista", 1, 0),
            (6, "Sevilla", "Madrid", 538, 325, "autopista", 1, 0),
            (7, "Madrid", "Zaragoza", 325, 195, "autovia", 0, 0),
            (8, "Zaragoza", "Madrid", 325, 195, "autovia", 0, 0),
            (9, "Madrid", "Toledo", 70, 42, "autovia", 0, 0),
            (10, "Toledo", "Madrid", 70, 42, "autovia", 0, 0),
            (11, "Madrid", "Ciudad Real", 180, 110, "autovia", 0, 0),
            (12, "Ciudad Real", "Madrid", 180, 110, "autovia", 0, 0),
            (13, "Madrid", "Albacete", 250, 150, "autovia", 0, 0),
            (14, "Albacete", "Madrid", 250, 150, "autovia", 0, 0),
            (15, "Madrid", "Burgos", 237, 142, "autovia", 0, 0),
            (16, "Burgos", "Madrid", 237, 142, "autovia", 0, 0),
            
            # Barcelona conexiones
            (17, "Barcelona", "Valencia", 349, 210, "autopista", 1, 0),
            (18, "Valencia", "Barcelona", 349, 210, "autopista", 1, 0),
            (19, "Barcelona", "Zaragoza", 296, 180, "autopista", 1, 0),
            (20, "Zaragoza", "Barcelona", 296, 180, "autopista", 1, 0),
            (21, "Barcelona", "Tarragona", 100, 60, "autopista", 0, 0),
            (22, "Tarragona", "Barcelona", 100, 60, "autopista", 0, 0),
            (23, "Barcelona", "Girona", 100, 60, "autovia", 0, 0),
            (24, "Girona", "Barcelona", 100, 60, "autovia", 0, 0),
            (25, "Barcelona", "Lleida", 150, 90, "autovia", 0, 0),
            (26, "Lleida", "Barcelona", 150, 90, "autovia", 0, 0),
            
            # Valencia conexiones
            (27, "Valencia", "Alicante", 166, 100, "autopista", 1, 0),
            (28, "Alicante", "Valencia", 166, 100, "autopista", 1, 0),
            (29, "Valencia", "Castellón", 65, 39, "autovia", 0, 0),
            (30, "Castellón", "Valencia", 65, 39, "autovia", 0, 0),
            (31, "Valencia", "Albacete", 190, 114, "autovia", 0, 0),
            (32, "Albacete", "Valencia", 190, 114, "autovia", 0, 0),
            
            # Sevilla conexiones
            (33, "Sevilla", "Córdoba", 138, 83, "autopista", 0, 0),
            (34, "Córdoba", "Sevilla", 138, 83, "autopista", 0, 0),
            (35, "Sevilla", "Málaga", 205, 125, "autopista", 1, 0),
            (36, "Málaga", "Sevilla", 205, 125, "autopista", 1, 0),
            (37, "Sevilla", "Huelva", 92, 55, "autovia", 0, 0),
            (38, "Huelva", "Sevilla", 92, 55, "autovia", 0, 0),
            (39, "Sevilla", "Cádiz", 125, 75, "autovia", 0, 0),
            (40, "Cádiz", "Sevilla", 125, 75, "autovia", 0, 0),
            
            # Zaragoza conexiones
            (41, "Zaragoza", "Pamplona", 180, 108, "autovia", 0, 0),
            (42, "Pamplona", "Zaragoza", 180, 108, "autovia", 0, 0),
            (43, "Zaragoza", "Burgos", 234, 140, "autovia", 0, 0),
            (44, "Burgos", "Zaragoza", 234, 140, "autovia", 0, 0),
            (45, "Zaragoza", "Lleida", 150, 90, "autovia", 0, 0),
            (46, "Lleida", "Zaragoza", 150, 90, "autovia", 0, 0),
            
            # Málaga conexiones
            (47, "Málaga", "Granada", 129, 77, "autovia", 0, 0),
            (48, "Granada", "Málaga", 129, 77, "autovia", 0, 0),
            (49, "Málaga", "Almería", 215, 129, "autopista", 1, 0),
            (50, "Almería", "Málaga", 215, 129, "autopista", 1, 0),
            
            # Bilbao conexiones
            (51, "Bilbao", "San Sebastián", 118, 71, "autopista", 0, 0),
            (52, "San Sebastián", "Bilbao", 118, 71, "autopista", 0, 0),
            (53, "Bilbao", "Vitoria", 66, 40, "autovia", 0, 0),
            (54, "Vitoria", "Bilbao", 66, 40, "autovia", 0, 0),
            (55, "Bilbao", "Burgos", 159, 95, "autovia", 0, 0),
            (56, "Burgos", "Bilbao", 159, 95, "autovia", 0, 0),
            
            # Valladolid conexiones
            (57, "Valladolid", "Salamanca", 115, 70, "autovia", 0, 0),
            (58, "Salamanca", "Valladolid", 115, 70, "autovia", 0, 0),
            (59, "Valladolid", "Burgos", 122, 73, "autovia", 0, 0),
            (60, "Burgos", "Valladolid", 122, 73, "autovia", 0, 0),
            (61, "Valladolid", "Madrid", 193, 116, "autovia", 0, 0),
            (62, "Madrid", "Valladolid", 193, 116, "autovia", 0, 0),
            
            # Oviedo/Gijón conexiones
            (63, "Oviedo", "Gijón", 28, 17, "autovia", 0, 0),
            (64, "Gijón", "Oviedo", 28, 17, "autovia", 0, 0),
            (65, "Oviedo", "Santander", 204, 125, "autovia", 0, 0),
            (66, "Santander", "Oviedo", 204, 125, "autovia", 0, 0),
            (67, "Gijón", "Bilbao", 304, 182, "autovia", 0, 0),
            (68, "Bilbao", "Gijón", 304, 182, "autovia", 0, 0),
            
            # Alicante/Murcia conexiones
            (69, "Alicante", "Murcia", 78, 47, "autovia", 0, 0),
            (70, "Murcia", "Alicante", 78, 47, "autovia", 0, 0),
            (71, "Murcia", "Albacete", 150, 90, "autovia", 0, 0),
            (72, "Albacete", "Murcia", 150, 90, "autovia", 0, 0),
            (73, "Murcia", "Almería", 220, 130, "autopista", 1, 0),
            (74, "Almería", "Murcia", 220, 130, "autopista", 1, 0),
            
            # Granada conexiones
            (75, "Granada", "Jaén", 98, 59, "autovia", 0, 0),
            (76, "Jaén", "Granada", 98, 59, "autovia", 0, 0),
            (77, "Granada", "Almería", 167, 100, "autovia", 0, 0),
            (78, "Almería", "Granada", 167, 100, "autovia", 0, 0),
            
            # Córdoba conexiones
            (79, "Córdoba", "Jaén", 105, 63, "autovia", 0, 0),
            (80, "Jaén", "Córdoba", 105, 63, "autovia", 0, 0),
            (81, "Córdoba", "Ciudad Real", 200, 120, "autovia", 0, 0),
            (82, "Ciudad Real", "Córdoba", 200, 120, "autovia", 0, 0),
            
            # Extremadura conexiones
            (83, "Badajoz", "Cáceres", 90, 54, "autovia", 0, 0),
            (84, "Cáceres", "Badajoz", 90, 54, "autovia", 0, 0),
            (85, "Cáceres", "Salamanca", 200, 120, "autovia", 0, 0),
            (86, "Salamanca", "Cáceres", 200, 120, "autovia", 0, 0),
            (87, "Badajoz", "Sevilla", 200, 120, "autovia", 0, 0),
            (88, "Sevilla", "Badajoz", 200, 120, "autovia", 0, 0),
            
            # Galicia conexiones
            (89, "Vigo", "Santiago", 90, 54, "autovia", 0, 0),
            (90, "Santiago", "Vigo", 90, 54, "autovia", 0, 0),
            (91, "Vigo", "Ourense", 90, 54, "autovia", 0, 0),
            (92, "Ourense", "Vigo", 90, 54, "autovia", 0, 0),
            (93, "Vigo", "Madrid", 600, 360, "autopista", 1, 0),
            (94, "Madrid", "Vigo", 600, 360, "autopista", 1, 0),
            
            # Pamplona/Logroño conexiones
            (95, "Pamplona", "Logroño", 90, 54, "autovia", 0, 0),
            (96, "Logroño", "Pamplona", 90, 54, "autovia", 0, 0),
            (97, "Logroño", "Burgos", 120, 72, "autovia", 0, 0),
            (98, "Burgos", "Logroño", 120, 72, "autovia", 0, 0),
            
            # Santander conexiones
            (99, "Santander", "Bilbao", 107, 65, "autovia", 0, 0),
            (100, "Bilbao", "Santander", 107, 65, "autovia", 0, 0),
            
            # Más conexiones importantes
            (101, "Ciudad Real", "Toledo", 120, 72, "autovia", 0, 0),
            (102, "Toledo", "Ciudad Real", 120, 72, "autovia", 0, 0),
            (103, "Toledo", "Córdoba", 300, 180, "autovia", 0, 0),
            (104, "Córdoba", "Toledo", 300, 180, "autovia", 0, 0),
            (105, "Salamanca", "Madrid", 210, 125, "autovia", 0, 0),
            (106, "Madrid", "Salamanca", 210, 125, "autovia", 0, 0)
        ]
        
        for arista in aristas:
            cursor.execute('''
                INSERT INTO aristas (id, origen, destino, distancia, tiempo, tipo, peaje, unidireccional)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', arista)
        
        conn.commit()
        conn.close()
        print(f"Datos creados: {len(ciudades)} ciudades, {len(aristas)} aristas")

# ============================================================================
# 2. DAO MEJORADO
# ============================================================================
class DAO:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_all_nodes(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM nodos ORDER BY nombre")
        nodes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return nodes
    
    def get_adjacency_list(self, use_distance=True):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT origen, destino, distancia, tiempo 
            FROM aristas
        ''')
        
        graph = {}
        for origen, destino, dist, tiempo in cursor.fetchall():
            if origen not in graph:
                graph[origen] = []
            cost = dist if use_distance else tiempo
            graph[origen].append((destino, cost))
            
            # Asegurarse de que el destino también existe como nodo en el grafo
            if destino not in graph:
                graph[destino] = []
        
        conn.close()
        return graph
    
    def save_route_history(self, origen, destino, distancia, tiempo, ruta):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO historico_rutas 
            (origen, destino, fecha_hora, distancia_total, tiempo_total, ruta_nodos)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (origen, destino, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
              distancia, tiempo, "->".join(ruta)))
        
        conn.commit()
        conn.close()
    
    def get_route_history(self, limit=10):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT origen, destino, fecha_hora, distancia_total, tiempo_total, ruta_nodos
            FROM historico_rutas 
            ORDER BY fecha_hora DESC 
            LIMIT ?
        ''', (limit,))
        
        history = cursor.fetchall()
        conn.close()
        return history

# ============================================================================
# 3. ALGORITMO DIJKSTRA MEJORADO
# ============================================================================
class Graph:
    def __init__(self, adjacency_list):
        self.graph = adjacency_list
    
    def dijkstra(self, start, end):
        if start not in self.graph:
            return None
        
        # Inicializar todas las distancias como infinito
        distances = {node: float('inf') for node in self.graph}
        previous = {node: None for node in self.graph}
        distances[start] = 0
        
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == end:
                break
            
            for neighbor, weight in self.graph.get(current, []):
                if neighbor not in distances:
                    distances[neighbor] = float('inf')
                    previous[neighbor] = None
                
                dist = current_dist + weight
                if dist < distances[neighbor]:
                    distances[neighbor] = dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (dist, neighbor))
        
        if end not in distances or distances[end] == float('inf'):
            return None
        
        # Reconstruir ruta
        path = []
        current = end
        while current:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        # Calcular tiempo estimado (aproximación: 60 km/h promedio)
        tiempo_estimado = distances[end] / 60 if distances[end] > 0 else 0
        
        return distances[end], path, tiempo_estimado
    
    def get_all_nodes(self):
        return list(self.graph.keys())

# ============================================================================
# 4. INTERFAZ GRÁFICA MEJORADA
# ============================================================================
class GPSApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Sistema GPS Avanzado - Algoritmo de Dijkstra")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar estilo
        self.setup_styles()
        
        # Variables tkinter
        self.use_distance = tk.BooleanVar(value=True)
        self.show_graph = tk.BooleanVar(value=False)
        self.auto_calculate = tk.BooleanVar(value=True)
        
        # Inicializar componentes
        self.db = DatabaseManager()
        self.dao = DAO(self.db)
        
        # Verificar datos
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM nodos")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            self.db.create_sample_data()
        
        # Cargar datos
        self.nodes = self.dao.get_all_nodes()
        self.graph_data = self.dao.get_adjacency_list(self.use_distance.get())
        self.graph = Graph(self.graph_data)
        
        # Construir interfaz
        self.setup_ui()
        
        # Cargar historial inicial
        self.load_history()
    
    def setup_styles(self):
        """Configurar estilos para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'background': '#f8f9fa'
        }
        
        # Configurar estilos
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), 
                       foreground=self.colors['primary'])
        style.configure('Subtitle.TLabel', font=('Segoe UI', 12), 
                       foreground=self.colors['secondary'])
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'),
                       padding=10, background=self.colors['secondary'],
                       foreground='white')
        style.map('Accent.TButton',
                 background=[('active', self.colors['primary'])])
        
        style.configure('Card.TFrame', background='white', relief=tk.RAISED,
                       borderwidth=1)
    
    def setup_ui(self):
        """Construir la interfaz de usuario"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(title_frame, text="🚀 SISTEMA GPS AVANZADO", 
                 style='Title.TLabel').pack(side=tk.LEFT)
        
        ttk.Label(title_frame, text="Algoritmo de Dijkstra • Base de Datos SQLite",
                 style='Subtitle.TLabel').pack(side=tk.LEFT, padx=(10, 0))
        
        # Contenedor principal
        container = ttk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo (30%)
        left_panel = ttk.Frame(container, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Panel de configuración
        config_card = ttk.Frame(left_panel, style='Card.TFrame', padding="15")
        config_card.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(config_card, text="⚙️ CONFIGURACIÓN", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Métrica
        metric_frame = ttk.Frame(config_card)
        metric_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(metric_frame, text="Métrica principal:").pack(anchor=tk.W)
        
        metric_radio_frame = ttk.Frame(metric_frame)
        metric_radio_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(metric_radio_frame, text="📏 Distancia (km)", 
                       variable=self.use_distance, value=True,
                       command=self.on_metric_change).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(metric_radio_frame, text="⏱️ Tiempo (minutos)", 
                       variable=self.use_distance, value=False,
                       command=self.on_metric_change).pack(anchor=tk.W, pady=2)
        
        # Opciones adicionales
        ttk.Checkbutton(config_card, text="🔄 Recalcular automáticamente",
                       variable=self.auto_calculate).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(config_card, text="📊 Mostrar gráfico de ruta",
                       variable=self.show_graph).pack(anchor=tk.W, pady=5)
        
        # Panel de búsqueda rápida
        quick_card = ttk.Frame(left_panel, style='Card.TFrame', padding="15")
        quick_card.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(quick_card, text="🔍 BÚSQUEDA RÁPIDA", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Filtro de ciudades
        ttk.Label(quick_card, text="Filtrar ciudades:").pack(anchor=tk.W)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(quick_card, textvariable=self.search_var)
        search_entry.pack(fill=tk.X, pady=5)
        search_entry.bind('<KeyRelease>', self.filter_cities)
        
        # Lista de ciudades filtradas
        cities_frame = ttk.Frame(quick_card)
        cities_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(cities_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cities_listbox = tk.Listbox(cities_frame, height=10,
                                        font=('Segoe UI', 9),
                                        yscrollcommand=scrollbar.set)
        self.cities_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.cities_listbox.yview)
        
        # Actualizar lista de ciudades
        self.update_cities_listbox()
        
        # Botones de acción
        action_card = ttk.Frame(left_panel, style='Card.TFrame', padding="15")
        action_card.pack(fill=tk.X)
        
        ttk.Button(action_card, text="🔄 Recargar Datos", 
                  command=self.reload_data).pack(fill=tk.X, pady=5)
        ttk.Button(action_card, text="📊 Ver Estadísticas", 
                  command=self.show_statistics).pack(fill=tk.X, pady=5)
        ttk.Button(action_card, text="📋 Ver Historial", 
                  command=self.show_history_window).pack(fill=tk.X, pady=5)
        ttk.Button(action_card, text="❓ Ayuda", 
                  command=self.show_help).pack(fill=tk.X, pady=5)
        ttk.Button(action_card, text="🚪 Salir", 
                  command=self.root.quit).pack(fill=tk.X, pady=5)
        
        # Panel derecho (70%)
        right_panel = ttk.Frame(container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Panel de entrada de ruta
        route_card = ttk.Frame(right_panel, style='Card.TFrame', padding="15")
        route_card.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(route_card, text="🗺️ CALCULAR RUTA", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Selectores de origen y destino
        input_grid = ttk.Frame(route_card)
        input_grid.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_grid, text="Origen:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        
        self.origin_combo = ttk.Combobox(input_grid, values=self.nodes, 
                                        font=('Segoe UI', 10), width=25)
        self.origin_combo.grid(row=0, column=1, padx=(0, 20), pady=5, sticky=tk.W)
        self.origin_combo.bind('<<ComboboxSelected>>', self.on_city_selected)
        
        ttk.Label(input_grid, text="Destino:", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        
        self.dest_combo = ttk.Combobox(input_grid, values=self.nodes, 
                                      font=('Segoe UI', 10), width=25)
        self.dest_combo.grid(row=1, column=1, padx=(0, 20), pady=5, sticky=tk.W)
        self.dest_combo.bind('<<ComboboxSelected>>', self.on_city_selected)
        
        # Botón para intercambiar origen/destino
        swap_btn = ttk.Button(input_grid, text="↔", width=3,
                             command=self.swap_cities)
        swap_btn.grid(row=0, column=2, rowspan=2, padx=(10, 0), pady=5)
        
        # Botón calcular
        calc_frame = ttk.Frame(route_card)
        calc_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(calc_frame, text="🚀 CALCULAR RUTA ÓPTIMA", 
                  style='Accent.TButton', command=self.calculate_route).pack()
        
        # Panel de resultados
        result_card = ttk.Frame(right_panel, style='Card.TFrame', padding="15")
        result_card.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(result_card, text="📋 RESULTADOS", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Pestañas para resultados
        notebook = ttk.Notebook(result_card)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de detalles
        details_tab = ttk.Frame(notebook)
        notebook.add(details_tab, text="📝 Detalles")
        
        self.result_text = scrolledtext.ScrolledText(details_tab, 
                                                    font=('Consolas', 10),
                                                    wrap=tk.WORD,
                                                    bg='white',
                                                    fg='#333333')
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de estadísticas
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text="📊 Estadísticas")
        
        self.stats_text = scrolledtext.ScrolledText(stats_tab,
                                                   font=('Segoe UI', 10),
                                                   wrap=tk.WORD,
                                                   bg='white',
                                                   fg='#333333')
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de historial reciente
        history_tab = ttk.Frame(notebook)
        notebook.add(history_tab, text="🕐 Historial")
        
        self.history_text = scrolledtext.ScrolledText(history_tab,
                                                     font=('Consolas', 9),
                                                     wrap=tk.WORD,
                                                     bg='white',
                                                     fg='#333333')
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Barra de estado
        self.status_bar = ttk.Frame(self.root, height=25, 
                                   style='Card.TFrame')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        self.status_label = ttk.Label(self.status_bar, 
                                     text="✅ Sistema listo. Seleccione origen y destino.")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.node_count_label = ttk.Label(self.status_bar,
                                         text=f"📊 Nodos: {len(self.nodes)}")
        self.node_count_label.pack(side=tk.RIGHT, padx=10)
        
        # Configurar valores iniciales
        if self.nodes:
            self.origin_combo.set(self.nodes[0])
            if len(self.nodes) > 1:
                self.dest_combo.set(self.nodes[1])
    
    def update_cities_listbox(self, filter_text=""):
        """Actualizar la lista de ciudades con filtro"""
        self.cities_listbox.delete(0, tk.END)
        
        filtered_cities = [city for city in self.nodes 
                          if filter_text.lower() in city.lower()]
        
        for city in sorted(filtered_cities):
            self.cities_listbox.insert(tk.END, city)
        
        # Vincular doble click para seleccionar
        self.cities_listbox.bind('<Double-Button-1>', self.on_listbox_select)
    
    def filter_cities(self, event=None):
        """Filtrar ciudades según texto de búsqueda"""
        self.update_cities_listbox(self.search_var.get())
    
    def on_listbox_select(self, event):
        """Seleccionar ciudad de la lista"""
        selection = self.cities_listbox.curselection()
        if selection:
            city = self.cities_listbox.get(selection[0])
            if not self.origin_combo.get() or self.origin_combo.get() == self.dest_combo.get():
                self.origin_combo.set(city)
            else:
                self.dest_combo.set(city)
    
    def on_city_selected(self, event=None):
        """Evento cuando se selecciona una ciudad"""
        if self.auto_calculate.get():
            self.calculate_route()
    
    def swap_cities(self):
        """Intercambiar origen y destino"""
        origen = self.origin_combo.get()
        destino = self.dest_combo.get()
        
        self.origin_combo.set(destino)
        self.dest_combo.set(origen)
        
        if self.auto_calculate.get():
            self.calculate_route()
    
    def on_metric_change(self):
        """Actualizar métrica"""
        self.graph_data = self.dao.get_adjacency_list(self.use_distance.get())
        self.graph = Graph(self.graph_data)
        
        metric = "DISTANCIA (km)" if self.use_distance.get() else "TIEMPO (minutos)"
        self.status_label.config(text=f"✅ Métrica cambiada a: {metric}")
        
        if self.auto_calculate.get() and self.origin_combo.get() and self.dest_combo.get():
            self.calculate_route()
    
    def reload_data(self):
        """Recargar datos de ejemplo"""
        self.db.create_sample_data()
        self.nodes = self.dao.get_all_nodes()
        
        # Actualizar combos
        self.origin_combo['values'] = self.nodes
        self.dest_combo['values'] = self.nodes
        
        # Actualizar lista
        self.update_cities_listbox(self.search_var.get())
        
        # Actualizar grafo
        self.graph_data = self.dao.get_adjacency_list(self.use_distance.get())
        self.graph = Graph(self.graph_data)
        
        # Actualizar contador
        self.node_count_label.config(text=f"📊 Nodos: {len(self.nodes)} | Aristas: {len(self.graph_data)}")
        
        self.status_label.config(text="✅ Datos recargados correctamente")
        messagebox.showinfo("Recarga completada", 
                          f"Datos recargados:\n• {len(self.nodes)} ciudades\n• Red de conexiones actualizada")
    
    def calculate_route(self):
        """Calcular ruta usando Dijkstra"""
        origen = self.origin_combo.get()
        destino = self.dest_combo.get()
        
        # Validaciones
        if not origen or not destino:
            messagebox.showwarning("Datos incompletos", 
                                 "Por favor, seleccione origen y destino.")
            return
        
        if origen == destino:
            messagebox.showwarning("Mismo origen y destino", 
                                 "El origen y destino no pueden ser iguales.")
            return
        
        # Actualizar estado
        self.status_label.config(text=f"🔍 Calculando ruta: {origen} → {destino}...")
        self.root.update()
        
        try:
            # Calcular ruta
            result = self.graph.dijkstra(origen, destino)
            
            if result is None:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(1.0, 
                    f"❌ NO EXISTE RUTA DISPONIBLE\n"
                    f"========================================\n\n"
                    f"Origen: {origen}\n"
                    f"Destino: {destino}\n\n"
                    f"No se encontró una ruta que conecte estas ciudades.\n"
                    f"Posibles causas:\n"
                    f"• No hay conexiones directas o indirectas\n"
                    f"• La red de transporte no llega a ambas ciudades\n"
                    f"• Error en los datos de conexión\n"
                )
                self.status_label.config(text=f"❌ No se encontró ruta entre {origen} y {destino}")
                return
            
            distancia, ruta, tiempo_estimado = result
            
            # Guardar en historial
            self.dao.save_route_history(origen, destino, distancia, tiempo_estimado, ruta)
            
            # Actualizar historial
            self.load_history()
            
            # Mostrar resultados
            self.display_results(origen, destino, distancia, ruta, tiempo_estimado)
            
            # Actualizar estadísticas
            self.update_statistics(ruta, distancia, tiempo_estimado)
            
            # Mostrar gráfico si está activado
            if self.show_graph.get():
                self.show_route_graph(ruta)
            
            # Actualizar estado
            metric = "km" if self.use_distance.get() else "min"
            self.status_label.config(
                text=f"✅ Ruta encontrada: {len(ruta)} nodos, {distancia:.1f} {metric}, {tiempo_estimado:.1f} horas"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la ruta:\n{str(e)}")
            self.status_label.config(text="❌ Error en el cálculo de ruta")
    
    def display_results(self, origen, destino, distancia, ruta, tiempo_estimado):
        """Mostrar resultados en el área de texto"""
        metric = "kilómetros" if self.use_distance.get() else "minutos"
        metric_abbr = "km" if self.use_distance.get() else "min"
        
        self.result_text.delete(1.0, tk.END)
        
        # Encabezado
        self.result_text.insert(tk.END, "="*70 + "\n")
        self.result_text.insert(tk.END, "🚀 RUTA ÓPTIMA ENCONTRADA\n")
        self.result_text.insert(tk.END, "="*70 + "\n\n")
        
        # Información básica
        self.result_text.insert(tk.END, f"📍 ORIGEN: {origen}\n")
        self.result_text.insert(tk.END, f"🎯 DESTINO: {destino}\n")
        self.result_text.insert(tk.END, f"📏 DISTANCIA TOTAL: {distancia:.1f} {metric}\n")
        self.result_text.insert(tk.END, f"⏱️ TIEMPO ESTIMADO: {tiempo_estimado:.1f} horas\n")
        self.result_text.insert(tk.END, f"🚗 VELOCIDAD MEDIA: {(distancia/tiempo_estimado if tiempo_estimado > 0 else 0):.1f} km/h\n")
        self.result_text.insert(tk.END, f"📍 NÚMERO DE PARADAS: {len(ruta)-2 if len(ruta) > 2 else 0}\n")
        self.result_text.insert(tk.END, f"🗺️ NODOS EN RUTA: {len(ruta)}\n\n")
        
        # Ruta detallada
        self.result_text.insert(tk.END, "📋 DETALLE DE LA RUTA:\n")
        self.result_text.insert(tk.END, "-"*70 + "\n")
        
        for i, nodo in enumerate(ruta, 1):
            prefix = "🚩 INICIO" if i == 1 else "🏁 FINAL" if i == len(ruta) else f"{i:2d}."
            self.result_text.insert(tk.END, f"{prefix} {nodo}\n")
        
        self.result_text.insert(tk.END, "\n" + "="*70 + "\n")
        
        # Información adicional
        self.result_text.insert(tk.END, "\n💡 INFORMACIÓN ADICIONAL:\n")
        self.result_text.insert(tk.END, "-"*40 + "\n")
        
        if len(ruta) == 2:
            self.result_text.insert(tk.END, "• Ruta directa entre ciudades\n")
        else:
            self.result_text.insert(tk.END, f"• Ruta con {len(ruta)-2} paradas intermedias\n")
        
        self.result_text.insert(tk.END, f"• Distancia promedio por tramo: {distancia/(len(ruta)-1):.1f} {metric_abbr}\n")
        
        # Sugerencias
        self.result_text.insert(tk.END, "\n💭 SUGERENCIAS:\n")
        self.result_text.insert(tk.END, "-"*40 + "\n")
        self.result_text.insert(tk.END, "• Verifique el estado del tráfico en tiempo real\n")
        self.result_text.insert(tk.END, "• Considere paradas para descanso cada 2 horas\n")
        self.result_text.insert(tk.END, "• Tenga en cuenta los peajes en autopistas\n")
        
        # Resaltar texto
        self.highlight_text()
    
    def highlight_text(self):
        """Resaltar texto en el área de resultados"""
        # Configurar tags para resaltado
        self.result_text.tag_config("header", foreground="#2c3e50", font=("Consolas", 11, "bold"))
        self.result_text.tag_config("important", foreground="#e74c3c", font=("Consolas", 10, "bold"))
        self.result_text.tag_config("success", foreground="#27ae60", font=("Consolas", 10))
        self.result_text.tag_config("info", foreground="#3498db", font=("Consolas", 9))
        
        # Aplicar tags
        self.result_text.tag_add("header", "1.0", "3.0")
        
        # Buscar y resaltar palabras importantes
        keywords = ["ORIGEN:", "DESTINO:", "DISTANCIA TOTAL:", "TIEMPO ESTIMADO:"]
        for keyword in keywords:
            start = "1.0"
            while True:
                pos = self.result_text.search(keyword, start, tk.END)
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                self.result_text.tag_add("important", pos, end)
                start = end
    
    def update_statistics(self, ruta, distancia, tiempo_estimado):
        """Actualizar estadísticas"""
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "📊 ESTADÍSTICAS DE LA RUTA\n")
        self.stats_text.insert(tk.END, "="*50 + "\n\n")
        
        self.stats_text.insert(tk.END, f"• Longitud de la ruta: {len(ruta)} ciudades\n")
        self.stats_text.insert(tk.END, f"• Distancia total: {distancia:.1f} km\n")
        self.stats_text.insert(tk.END, f"• Tiempo estimado: {tiempo_estimado:.1f} horas\n")
        self.stats_text.insert(tk.END, f"• Velocidad media: {(distancia/tiempo_estimado if tiempo_estimado > 0 else 0):.1f} km/h\n")
        self.stats_text.insert(tk.END, f"• Distancia promedio entre ciudades: {distancia/(len(ruta)-1):.1f} km\n\n")
        
        self.stats_text.insert(tk.END, "📈 ANÁLISIS DE LA RUTA:\n")
        self.stats_text.insert(tk.END, "-"*30 + "\n")
        
        if tiempo_estimado < 1:
            self.stats_text.insert(tk.END, "• Ruta corta (menos de 1 hora)\n")
        elif tiempo_estimado < 3:
            self.stats_text.insert(tk.END, "• Ruta media (1-3 horas)\n")
        elif tiempo_estimado < 6:
            self.stats_text.insert(tk.END, "• Ruta larga (3-6 horas)\n")
        else:
            self.stats_text.insert(tk.END, "• Ruta muy larga (más de 6 horas)\n")
        
        if len(ruta) == 2:
            self.stats_text.insert(tk.END, "• Ruta directa sin escalas\n")
        elif len(ruta) <= 4:
            self.stats_text.insert(tk.END, "• Ruta con pocas escalas\n")
        else:
            self.stats_text.insert(tk.END, "• Ruta con múltiples escalas\n")
    
    def load_history(self):
        """Cargar historial de rutas"""
        history = self.dao.get_route_history(10)
        self.history_text.delete(1.0, tk.END)
        
        if not history:
            self.history_text.insert(tk.END, "🕐 No hay historial de rutas\n")
            return
        
        self.history_text.insert(tk.END, "🕐 HISTORIAL DE RUTAS RECIENTES\n")
        self.history_text.insert(tk.END, "="*60 + "\n\n")
        
        for i, (origen, destino, fecha, distancia, tiempo, ruta) in enumerate(history, 1):
            self.history_text.insert(tk.END, f"{i:2d}. {fecha}\n")
            self.history_text.insert(tk.END, f"   📍 {origen} → {destino}\n")
            self.history_text.insert(tk.END, f"   📏 {distancia:.1f} km | ⏱️ {tiempo:.1f} h\n")
            
            # Mostrar ruta truncada si es muy larga
            if len(ruta) > 100:
                ruta_display = ruta[:100] + "..."
            else:
                ruta_display = ruta
            
            self.history_text.insert(tk.END, f"   🛣️  {ruta_display}\n\n")
    
    def show_route_graph(self, ruta):
        """Mostrar gráfico de la ruta"""
        try:
            # Crear ventana para el gráfico
            graph_window = tk.Toplevel(self.root)
            graph_window.title("📊 Visualización de Ruta")
            graph_window.geometry("800x600")
            
            # Crear figura de matplotlib
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Crear grafo para visualización
            G = nx.Graph()
            
            # Añadir nodos y aristas de la ruta
            for i in range(len(ruta)-1):
                G.add_edge(ruta[i], ruta[i+1])
            
            # Diseño del grafo
            pos = nx.spring_layout(G, seed=42)
            
            # Dibujar nodos
            nx.draw_networkx_nodes(G, pos, node_size=300, 
                                  node_color='lightblue', 
                                  edgecolors='black')
            
            # Dibujar aristas
            nx.draw_networkx_edges(G, pos, width=2, 
                                  edge_color='red', 
                                  style='solid')
            
            # Etiquetas
            nx.draw_networkx_labels(G, pos, font_size=10, 
                                   font_weight='bold')
            
            ax.set_title(f'Ruta: {" → ".join(ruta)}', fontsize=14, fontweight='bold')
            ax.axis('off')
            
            # Añadir leyenda
            ax.text(0.05, 0.05, f'Nodos: {len(ruta)}\nRuta óptima encontrada', 
                   transform=ax.transAxes, fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            # Integrar en Tkinter
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Botón para cerrar
            ttk.Button(graph_window, text="Cerrar", 
                      command=graph_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showwarning("Advertencia", 
                                 f"No se pudo generar el gráfico:\n{str(e)}")
    
    def show_statistics(self):
        """Mostrar estadísticas generales"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Estadísticas del Sistema")
        stats_window.geometry("600x500")
        
        # Obtener estadísticas de la base de datos
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM nodos")
        total_nodos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM aristas")
        total_aristas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM historico_rutas")
        total_rutas = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(distancia_total) FROM historico_rutas")
        avg_distancia = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(tiempo_total) FROM historico_rutas")
        avg_tiempo = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # Mostrar estadísticas
        text = scrolledtext.ScrolledText(stats_window, font=("Segoe UI", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "📊 ESTADÍSTICAS DEL SISTEMA GPS\n")
        text.insert(tk.END, "="*50 + "\n\n")
        
        text.insert(tk.END, "🌍 DATOS GEOGRÁFICOS:\n")
        text.insert(tk.END, f"• Ciudades en la base de datos: {total_nodos}\n")
        text.insert(tk.END, f"• Conexiones de transporte: {total_aristas}\n")
        text.insert(tk.END, f"• Densidad de la red: {(total_aristas/total_nodos if total_nodos > 0 else 0):.2f} conexiones/ciudad\n\n")
        
        text.insert(tk.END, "📈 HISTORIAL DE USO:\n")
        text.insert(tk.END, f"• Rutas calculadas: {total_rutas}\n")
        text.insert(tk.END, f"• Distancia promedio: {avg_distancia:.1f} km\n")
        text.insert(tk.END, f"• Tiempo promedio: {avg_tiempo:.1f} horas\n\n")
        
        text.insert(tk.END, "⚙️ CONFIGURACIÓN ACTUAL:\n")
        text.insert(tk.END, f"• Métrica principal: {'Distancia (km)' if self.use_distance.get() else 'Tiempo (min)'}\n")
        text.insert(tk.END, f"• Cálculo automático: {'Activado' if self.auto_calculate.get() else 'Desactivado'}\n")
        
        text.config(state=tk.DISABLED)
    
    def show_history_window(self):
        """Mostrar ventana de historial completo"""
        history_window = tk.Toplevel(self.root)
        history_window.title("🕐 Historial Completo de Rutas")
        history_window.geometry("800x600")
        
        # Obtener todo el historial
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historico_rutas ORDER BY fecha_hora DESC")
        history = cursor.fetchall()
        conn.close()
        
        # Crear Treeview para mostrar historial
        tree_frame = ttk.Frame(history_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        tree = ttk.Treeview(tree_frame, 
                           columns=("ID", "Origen", "Destino", "Fecha", "Distancia", "Tiempo"),
                           yscrollcommand=vsb.set,
                           xscrollcommand=hsb.set)
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        # Configurar columnas
        tree.heading("#0", text="#")
        tree.heading("ID", text="ID")
        tree.heading("Origen", text="Origen")
        tree.heading("Destino", text="Destino")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Distancia", text="Distancia (km)")
        tree.heading("Tiempo", text="Tiempo (h)")
        
        tree.column("#0", width=50)
        tree.column("ID", width=50)
        tree.column("Origen", width=100)
        tree.column("Destino", width=100)
        tree.column("Fecha", width=150)
        tree.column("Distancia", width=100)
        tree.column("Tiempo", width=100)
        
        # Insertar datos
        for i, row in enumerate(history, 1):
            tree.insert("", tk.END, text=str(i), 
                       values=(row[0], row[1], row[2], row[3], 
                              f"{row[4]:.1f}", f"{row[5]:.1f}"))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Botones
        button_frame = ttk.Frame(history_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Exportar a CSV", 
                  command=lambda: self.export_history(history)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar Historial", 
                  command=self.clear_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", 
                  command=history_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def export_history(self, history):
        """Exportar historial a CSV"""
        from tkinter import filedialog
        import csv
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Origen", "Destino", "Fecha", "Distancia (km)", "Tiempo (h)", "Ruta"])
                    for row in history:
                        writer.writerow(row)
                
                messagebox.showinfo("Exportación exitosa", 
                                  f"Historial exportado a:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")
    
    def clear_history(self):
        """Limpiar historial"""
        if messagebox.askyesno("Confirmar", 
                              "¿Está seguro de que desea borrar todo el historial?"):
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historico_rutas")
            conn.commit()
            conn.close()
            
            self.load_history()
            messagebox.showinfo("Historial borrado", "El historial ha sido borrado correctamente.")
    
    def show_help(self):
        """Mostrar ventana de ayuda"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Ayuda del Sistema GPS")
        help_window.geometry("700x500")
        
        text = scrolledtext.ScrolledText(help_window, font=("Segoe UI", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_text = """
🚀 SISTEMA GPS AVANZADO - AYUDA
================================

📌 CÓMO USAR EL SISTEMA:
1. Seleccione una ciudad de origen en el desplegable superior
2. Seleccione una ciudad de destino
3. Haga clic en "CALCULAR RUTA ÓPTIMA"
4. Los resultados se mostrarán en el panel de detalles

⚙️ FUNCIONALIDADES PRINCIPALES:

🔍 BÚSQUEDA RÁPIDA:
• Use el campo de búsqueda para filtrar ciudades
• Haga doble clic en una ciudad para seleccionarla como origen/destino
• Use el botón ↔ para intercambiar origen y destino

📊 VISUALIZACIÓN:
• Active "Mostrar gráfico de ruta" para ver una representación visual
• Consulte las pestañas de Estadísticas e Historial
• Exporte el historial a formato CSV

⚡ CONSEJOS:
• Active "Recalcular automáticamente" para resultados instantáneos
• Use diferentes métricas (distancia/tiempo) según sus necesidades
• Consulte el historial para ver rutas anteriores

🔧 ALGORITMO:
• El sistema usa el algoritmo de Dijkstra para encontrar la ruta más corta
• Soporta grafos dirigidos y no dirigidos
• Optimizado para redes de transporte reales

📞 SOPORTE:
• Para problemas técnicos, verifique que la base de datos esté intacta
• Recargue los datos si encuentra inconsistencias
• El sistema crea automáticamente datos de ejemplo si no existen

🎯 OBJETIVO:
Este sistema simula un sistema de navegación GPS real, calculando rutas
óptimas entre ciudades españolas usando algoritmos de teoría de grafos.
"""
        
        text.insert(1.0, help_text)
        text.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Cerrar", 
                  command=help_window.destroy).pack(pady=10)
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

# ============================================================================
# 5. EJECUCIÓN PRINCIPAL
# ============================================================================
def main():
    print("="*80)
    print("🚀 SISTEMA GPS AVANZADO CON ALGORITMO DE DIJKSTRA")
    print("="*80)
    print("\n📊 Características:")
    print("• 50+ nodos (ciudades españolas con coordenadas)")
    print("• 100+ aristas (red de transporte completa)")
    print("• Base de datos SQLite con múltiples tablas")
    print("• Algoritmo Dijkstra optimizado y robusto")
    print("• Interfaz gráfica moderna con Tkinter")
    print("• Visualización de gráficos con Matplotlib")
    print("• Historial de rutas y exportación a CSV")
    print("\n⚡ Iniciando sistema...")
    
    try:
        app = GPSApp()
        app.run()
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        print("Por favor, verifique la instalación de Python y las dependencias.")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()