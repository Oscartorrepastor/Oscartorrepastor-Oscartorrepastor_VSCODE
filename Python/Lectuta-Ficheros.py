import os

def procesar_archivo_palabras():
    # Crear carpeta si no existe (como en el PDF página 8)
    ruta_carpeta = "Ficheros"
    os.makedirs(ruta_carpeta, exist_ok=True)
    
    # === MÉTODO READ (página 3 del PDF) ===
    with open("Ficheros\palabras.txt", "r", encoding="utf-8") as archivo_entrada:
        contenido = archivo_entrada.read()  # read() para leer todo el contenido
    
    # Procesar palabras
    palabras = contenido.split()
    total_palabras = len(palabras)
    
    # Contar vocales
    total_vocales = 0
    for palabra in palabras:
        for caracter in palabra.lower():
            if caracter in 'aeiouáéíóú':
                total_vocales += 1
    
    # Contar frecuencia de palabras
    frecuencia_palabras = {}
    for palabra in palabras:
        palabra = palabra.lower()
        frecuencia_palabras[palabra] = frecuencia_palabras.get(palabra, 0) + 1
    
    # Encontrar palabras repetidas
    palabras_repetidas = {palabra: count for palabra, count in frecuencia_palabras.items() if count > 1}
    
    # Encontrar palabras más repetidas
    max_repeticiones = max(frecuencia_palabras.values()) if frecuencia_palabras else 0
    palabras_mas_repetidas = [palabra for palabra, count in frecuencia_palabras.items() if count == max_repeticiones]
    
    # === ESCRITURA EN salida.txt (usando write y writelines) ===
    ruta_salida1 = os.path.join(ruta_carpeta, "salida.txt")
    
    with open(ruta_salida1, "w", encoding="utf-8") as archivo_salida:
        # Usando write (página 4 del PDF)
        archivo_salida.write("=== ANÁLISIS DEL ARCHIVO palabras.txt ===\n")
        archivo_salida.write(f"Número total de palabras: {total_palabras}\n")
        archivo_salida.write(f"Número total de vocales: {total_vocales}\n")
        archivo_salida.write("\n--- PALABRAS REPETIDAS ---\n")
        
        if palabras_repetidas:
            # Preparar lista para writelines (página 5 del PDF)
            lineas_repetidas = []
            for palabra, count in sorted(palabras_repetidas.items(), key=lambda x: x[1], reverse=True):
                lineas_repetidas.append(f"'{palabra}': {count} veces\n")
            
            # Usando writelines
            archivo_salida.writelines(lineas_repetidas)
        else:
            archivo_salida.write("No hay palabras repetidas\n")
        
        archivo_salida.write("\n--- PALABRA/S MÁS REPETIDA/S ---\n")
        if palabras_mas_repetidas:
            for palabra in palabras_mas_repetidas:
                archivo_salida.write(f"'{palabra}': {max_repeticiones} veces\n")
        else:
            archivo_salida.write("No hay palabras repetidas\n")
    
    # === ESCRITURA EN salida2.txt (usando métodos diferentes) ===
    ruta_salida2 = os.path.join(ruta_carpeta, "salida2.txt")
    
    with open(ruta_salida2, "w", encoding="utf-8") as archivo_salida2:
        archivo_salida2.write("=== INFORMACIÓN SOBRE PALABRAS REPETIDAS ===\n\n")
        archivo_salida2.write("PALABRAS REPETIDAS (ordenadas alfabéticamente):\n")
        
        if palabras_repetidas:
            # Usando write para cada línea
            for palabra in sorted(palabras_repetidas.keys()):
                archivo_salida2.write(f"- {palabra}: {palabras_repetidas[palabra]} repeticiones\n")
        else:
            archivo_salida2.write("No hay palabras repetidas\n")
        
        archivo_salida2.write(f"\nRESUMEN:\n")
        archivo_salida2.write(f"Palabra(s) más repetida(s): {', '.join(palabras_mas_repetidas)}\n")
        archivo_salida2.write(f"Número de repeticiones: {max_repeticiones}\n")
        archivo_salida2.write(f"Total de palabras diferentes repetidas: {len(palabras_repetidas)}\n")
    
    # === MOSTRAR RESULTADOS POR PANTALLA (usando readlines) ===
    print("📊 RESULTADOS DEL ANÁLISIS:")
    print("=" * 50)
    
    # Leer el archivo recién creado con readlines (página 3 del PDF)
    with open(ruta_salida1, "r", encoding="utf-8") as f:
        lineas = f.readlines()
        for linea in lineas:
            print(linea, end='')  # end='' para evitar dobles saltos de línea
    
    print(f"\n✅ Archivos generados en la carpeta '{ruta_carpeta}':")
    print(f"   - salida.txt")
    print(f"   - salida2.txt")

# === VERSIÓN ALTERNATIVA USANDO READLINES DESDE EL PRINCIPIO ===
def version_con_readlines():
    """Versión que usa readlines() para leer el archivo original"""
    ruta_carpeta = "Ficheros"
    os.makedirs(ruta_carpeta, exist_ok=True)
    
    print("\n" + "="*60)
    print("VERSIÓN USANDO READLINES()")
    print("="*60)
    
    # === USANDO READLINES (página 3 del PDF) ===
    with open("palabras.txt", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()  # readlines() devuelve lista de líneas
    
    # Procesar palabras desde todas las líneas
    todas_palabras = []
    for linea in lineas:
        palabras_linea = linea.strip().split()
        todas_palabras.extend(palabras_linea)
    
    # Estadísticas
    total_palabras = len(todas_palabras)
    
    # Contar vocales
    total_vocales = 0
    for palabra in todas_palabras:
        for letra in palabra.lower():
            if letra in 'aeiouáéíóú':
                total_vocales += 1
    
    # Frecuencia
    frecuencia = {}
    for palabra in todas_palabras:
        palabra = palabra.lower()
        frecuencia[palabra] = frecuencia.get(palabra, 0) + 1
    
    # Escribir resultados usando seek y write (página 4 del PDF)
    ruta_resultado = os.path.join(ruta_carpeta, "resultado_readlines.txt")
    
    with open(ruta_resultado, "w+", encoding="utf-8") as f:  # w+ para lectura y escritura
        # Escribir contenido inicial
        f.write("ANÁLISIS CON READLINES\n")
        f.write("======================\n")
        f.write(f"Total de líneas en el archivo: {len(lineas)}\n")
        f.write(f"Total de palabras: {total_palabras}\n")
        f.write(f"Total de vocales: {total_vocales}\n\n")
        
        # Palabras únicas
        palabras_unicas = set(todas_palabras)
        f.write(f"Palabras diferentes encontradas: {len(palabras_unicas)}\n")
        
        # Usar seek para volver al principio y leer
        f.seek(0)  # seek(0, 0) - ir al principio (página 4)
        contenido = f.read()
        print(contenido)
        
        # Volver al final para añadir más
        f.seek(0, 2)  # seek(0, 2) - ir al final (página 4)
        f.write("\n--- FIN DEL ANÁLISIS ---\n")
    
    print(f"✅ Archivo adicional generado: 'resultado_readlines.txt'")

if __name__ == "__main__":
    print("🔍 INICIANDO ANÁLISIS DE palabras.txt")
    print("Métodos utilizados según el PDF:")
    print("- with open() (recomendado)")
    print("- read() y readlines()")
    print("- write() y writelines()") 
    print("- seek() para navegación en archivos")
    print("- Creación de directorios")
    print("- Diferentes modos de apertura\n")
    
    procesar_archivo_palabras()
    
    # Ejecutar versión alternativa
    version_con_readlines()