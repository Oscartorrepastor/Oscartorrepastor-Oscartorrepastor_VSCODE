import tkinter as tk
from tkinter import ttk, messagebox
import time
import math

class HanoiSolver:
    """Clase que maneja la lógica de las Torres de Hanói"""
    def __init__(self):
        self.movimientos = []
        self.estado_actual = 0
        self.solucion = []
        
    def resolver(self, n, origen='A', destino='C', auxiliar='B'):
        """Genera la solución óptima para n discos"""
        self.movimientos = []
        self.solucion = []
        self.estado_actual = 0
        self._hanoi_recursivo(n, origen, destino, auxiliar)
        return self.movimientos
    
    def _hanoi_recursivo(self, n, origen, destino, auxiliar):
        """Algoritmo recursivo de Hanói"""
        if n == 1:
            self.movimientos.append((1, origen, destino))
            return
        self._hanoi_recursivo(n-1, origen, auxiliar, destino)
        self.movimientos.append((n, origen, destino))
        self._hanoi_recursivo(n-1, auxiliar, destino, origen)
    
    def siguiente_movimiento(self):
        """Retorna el siguiente movimiento"""
        if self.estado_actual < len(self.movimientos):
            movimiento = self.movimientos[self.estado_actual]
            self.estado_actual += 1
            return movimiento
        return None
    
    def anterior_movimiento(self):
        """Retorna el movimiento anterior"""
        if self.estado_actual > 0:
            self.estado_actual -= 1
            return self.movimientos[self.estado_actual - 1] if self.estado_actual > 0 else None
        return None
    
    def reiniciar(self):
        """Reinicia el estado"""
        self.estado_actual = 0
    
    def get_movimientos_totales(self):
        """Retorna el total de movimientos"""
        return len(self.movimientos)
    
    def get_movimientos_realizados(self):
        """Retorna los movimientos realizados"""
        return self.estado_actual

class HanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanói - Solucionador")
        self.root.geometry("900x650")
        
        # Variables
        self.num_discos = 3
        self.animando = False
        self.velocidad = 500  # ms
        self.colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                       '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
        
        # Inicializar solver
        self.solver = HanoiSolver()
        
        # Estado de las torres: {'A': [discos], 'B': [], 'C': []}
        self.torres = {'A': [], 'B': [], 'C': []}
        self.movimientos = []
        
        # Configurar interfaz
        self.setup_ui()
        
        # Inicializar estado
        self.inicializar_torres()
        self.dibujar_torres()
    
    def setup_ui(self):
        """Configura toda la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos de grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Controles
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_frame.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_controles(control_frame)
        
        # Panel derecho - Visualización
        vis_frame = ttk.LabelFrame(main_frame, text="Visualización", padding="10")
        vis_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_visualizacion(vis_frame)
        
        # Panel inferior - Información
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_info(info_frame)
    
    def setup_controles(self, parent):
        """Configura los controles de la interfaz"""
        # Número de discos
        ttk.Label(parent, text="Número de discos:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.discos_var = tk.IntVar(value=3)
        discos_spinbox = ttk.Spinbox(parent, from_=1, to=10, textvariable=self.discos_var, 
                                     width=10, command=self.cambiar_discos)
        discos_spinbox.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Velocidad
        ttk.Label(parent, text="Velocidad (ms):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.velocidad_var = tk.IntVar(value=500)
        velocidad_scale = ttk.Scale(parent, from_=100, to=1000, variable=self.velocidad_var,
                                   orient=tk.HORIZONTAL, length=150)
        velocidad_scale.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.velocidad_label = ttk.Label(parent, text="500 ms")
        self.velocidad_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 15))
        
        velocidad_scale.configure(command=self.actualizar_velocidad)
        
        # Botones
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=5, column=0, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Resolver", command=self.resolver,
                  width=15).pack(pady=5)
        ttk.Button(btn_frame, text="Paso a Paso", command=self.paso_a_paso,
                  width=15).pack(pady=5)
        ttk.Button(btn_frame, text="Siguiente", command=self.siguiente,
                  width=15).pack(pady=5)
        ttk.Button(btn_frame, text="Anterior", command=self.anterior,
                  width=15).pack(pady=5)
        ttk.Button(btn_frame, text="Reiniciar", command=self.reiniciar,
                  width=15).pack(pady=5)
        
        # Información matemática
        info_btn = ttk.Button(parent, text="Ver Fórmula", command=self.mostrar_formula)
        info_btn.grid(row=6, column=0, pady=(20, 5))
    
    def setup_visualizacion(self, parent):
        """Configura el área de visualización"""
        # Canvas para dibujar
        self.canvas = tk.Canvas(parent, width=600, height=400, bg='white', 
                               highlightthickness=1, highlightbackground="gray")
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_info(self, parent):
        """Configura el panel de información"""
        # Text widget para mostrar información
        self.info_text = tk.Text(parent, height=6, width=80, wrap=tk.WORD,
                                font=('Consolas', 10), bg='#f0f0f0')
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Actualizar información inicial
        self.actualizar_info()
    
    def inicializar_torres(self):
        """Inicializa el estado de las torres"""
        self.torres = {'A': [], 'B': [], 'C': []}
        for i in range(self.num_discos, 0, -1):
            self.torres['A'].append(i)
    
    def dibujar_torres(self):
        """Dibuja las torres y discos en el canvas"""
        self.canvas.delete("all")
        
        # Dimensiones
        canvas_width = 600
        canvas_height = 400
        base_y = 350
        altura_torre = 200
        
        # Posiciones de las torres
        posiciones = {
            'A': (150, base_y),
            'B': (300, base_y),
            'C': (450, base_y)
        }
        
        # Dibujar base
        self.canvas.create_rectangle(50, base_y, 550, base_y + 20, 
                                    fill='#8B4513', outline='black', width=2)
        
        # Dibujar torres
        for torre, (x, y) in posiciones.items():
            # Poste
            self.canvas.create_rectangle(x-5, y-altura_torre, x+5, y, 
                                        fill='#A0522D', outline='black', width=2)
            
            # Etiqueta
            self.canvas.create_text(x, y+30, text=f"Torre {torre}", 
                                   font=('Arial', 12, 'bold'))
        
        # Dibujar discos
        for torre, discos in self.torres.items():
            x = posiciones[torre][0]
            y_base = posiciones[torre][1]
            
            for i, disco in enumerate(discos):
                # Tamaño proporcional al número de disco
                ancho = 20 + disco * 20
                altura = 20
                y = y_base - (i * altura) - altura
                
                # Color basado en el número de disco
                color_idx = (disco - 1) % len(self.colores)
                color = self.colores[color_idx]
                
                # Dibujar disco
                self.canvas.create_rectangle(x - ancho//2, y,
                                           x + ancho//2, y + altura,
                                           fill=color, outline='black', width=2)
                
                # Número del disco
                self.canvas.create_text(x, y + altura//2, 
                                       text=str(disco),
                                       font=('Arial', 10, 'bold'))
    
    def cambiar_discos(self):
        """Cambia el número de discos"""
        self.num_discos = self.discos_var.get()
        self.reiniciar()
    
    def actualizar_velocidad(self, *args):
        """Actualiza la velocidad de animación"""
        self.velocidad = self.velocidad_var.get()
        self.velocidad_label.config(text=f"{self.velocidad} ms")
    
    def resolver(self):
        """Resuelve automáticamente el problema"""
        if self.animando:
            return
        
        # Generar solución
        self.movimientos = self.solver.resolver(self.num_discos)
        self.animando = True
        self.animar_solucion(0)
    
    def animar_solucion(self, indice):
        """Anima la solución completa"""
        if not self.animando or indice >= len(self.movimientos):
            self.animando = False
            return
        
        # Realizar movimiento
        disco, origen, destino = self.movimientos[indice]
        self.realizar_movimiento(disco, origen, destino)
        
        # Actualizar información
        self.actualizar_info()
        
        # Programar siguiente movimiento
        self.root.after(self.velocidad, lambda: self.animar_solucion(indice + 1))
    
    def paso_a_paso(self):
        """Realiza un solo paso"""
        if not self.movimientos:
            self.movimientos = self.solver.resolver(self.num_discos)
        
        movimiento = self.solver.siguiente_movimiento()
        if movimiento:
            disco, origen, destino = movimiento
            self.realizar_movimiento(disco, origen, destino)
            self.actualizar_info()
    
    def siguiente(self):
        """Siguiente movimiento"""
        self.paso_a_paso()
    
    def anterior(self):
        """Movimiento anterior"""
        movimiento = self.solver.anterior_movimiento()
        if movimiento:
            # Para deshacer, invertimos origen y destino
            disco, destino, origen = movimiento
            self.realizar_movimiento(disco, origen, destino)
            
            # Ajustar estado del solver
            self.solver.estado_actual -= 1
            self.actualizar_info()
    
    def realizar_movimiento(self, disco, origen, destino):
        """Realiza un movimiento entre torres"""
        # Validar que el disco existe en la torre de origen
        if disco in self.torres[origen]:
            # Remover de origen
            self.torres[origen].remove(disco)
            # Añadir a destino
            self.torres[destino].append(disco)
            # Redibujar
            self.dibujar_torres()
            
            # Destacar el movimiento
            self.destacar_movimiento(disco, origen, destino)
        else:
            print(f"Error: Disco {disco} no encontrado en torre {origen}")
    
    def destacar_movimiento(self, disco, origen, destino):
        """Destaca visualmente un movimiento"""
        # Posiciones de las torres
        posiciones = {
            'A': 150,
            'B': 300,
            'C': 450
        }
        
        x1 = posiciones[origen]
        x2 = posiciones[destino]
        y = 100  # Altura fija para la línea de movimiento
        
        # Dibujar línea de movimiento
        self.canvas.create_line(x1, y, x2, y, 
                               fill='red', width=2, arrow=tk.BOTH,
                               tags=('movimiento',))
        
        # Eliminar después de 500ms
        self.root.after(500, lambda: self.canvas.delete('movimiento'))
    
    def reiniciar(self):
        """Reinicia el estado del juego"""
        self.animando = False
        self.inicializar_torres()
        self.movimientos = []
        self.solver.reiniciar()
        self.dibujar_torres()
        self.actualizar_info()
    
    def actualizar_info(self):
        """Actualiza el panel de información"""
        total_movimientos = (1 << self.num_discos) - 1  # 2^n - 1
        mov_realizados = self.solver.get_movimientos_realizados()
        
        info = f"""
TORRES DE HANÓI - INFORMACIÓN

Discos: {self.num_discos}
Movimientos mínimos necesarios: {total_movimientos:,}
Movimientos realizados: {mov_realizados:,}
Movimientos restantes: {total_movimientos - mov_realizados:,}

FÓRMULA: 2^{self.num_discos} - 1 = {total_movimientos:,}

ESTADO: {'Animando...' if self.animando else 'Listo'}

TORRES ACTUALES:
A: {self.torres['A']}
B: {self.torres['B']}
C: {self.torres['C']}
"""
        
        # Limpiar y mostrar nueva información
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
        self.info_text.configure(state='disabled')
    
    def mostrar_formula(self):
        """Muestra información sobre la fórmula matemática"""
        formula_info = """
FÓRMULA DE LAS TORRES DE HANÓI

El número mínimo de movimientos para resolver
el problema con n discos es:

M(n) = 2ⁿ - 1

Donde:
• n = número de discos
• M(n) = movimientos mínimos

EJEMPLOS:
• 1 disco: 2¹ - 1 = 1 movimiento
• 3 discos: 2³ - 1 = 7 movimientos
• 8 discos: 2⁸ - 1 = 255 movimientos

CURIOSIDAD:
Si tuvieras 64 discos y movieras uno por segundo,
tardarías aproximadamente 585 mil millones de años
en resolver el puzzle.
"""
        
        messagebox.showinfo("Fórmula Matemática", formula_info)

def main():
    """Función principal"""
    root = tk.Tk()
    app = HanoiGUI(root)
    
    # Centrar ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Iniciar
    root.mainloop()

if __name__ == "__main__":
    main()