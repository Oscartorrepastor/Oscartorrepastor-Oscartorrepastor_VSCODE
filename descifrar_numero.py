import requests

import re

# El ID misterioso
id_largo = "68637633726662436"

print("🔍 IDENTIFICANDO POSIBLE OPERADORA")
print("=" * 50)

# ============================================
# 1. EXTRAER POSIBLES NÚMEROS DEL ID
# ============================================
print("\n1. EXTRAYENDO NÚMEROS CANDIDATOS:")

# Longitudes típicas por país
candidatos = []

# Para España (9 dígitos móvil)
if len(id_largo) >= 9:
    es_numero = id_largo[:9]
    candidatos.append(("ES", es_numero))  # España
    print(f"  • ES (+34): {es_numero}")

# Para México (10 dígitos)
if len(id_largo) >= 10:
    mx_numero = id_largo[:10]
    candidatos.append(("MX", mx_numero))  # México
    print(f"  • MX (+52): {mx_numero}")

# Para Colombia (10 dígitos)
if len(id_largo) >= 10:
    co_numero = id_largo[:10]
    candidatos.append(("CO", co_numero))  # Colombia
    print(f"  • CO (+57): {co_numero}")

# ============================================
# 2. FUNCIÓN PARA IDENTIFICAR OPERADORA (ESPAÑA)
# ============================================
def operadora_espana(numero):
    """Identifica operadora en España por primeros dígitos"""
    
    # Diccionario de rangos (simplificado)
    rangos = {
        # Movistar
        '600': 'Movistar', '601': 'Movistar', '602': 'Movistar',
        '610': 'Movistar', '611': 'Movistar', '612': 'Movistar',
        '620': 'Movistar', '621': 'Movistar', '622': 'Movistar',
        '630': 'Movistar', '631': 'Movistar', '632': 'Movistar',
        '640': 'Movistar', '641': 'Movistar', '642': 'Movistar',
        '650': 'Movistar', '651': 'Movistar', '652': 'Movistar',
        '660': 'Movistar', '661': 'Movistar', '662': 'Movistar',
        '670': 'Movistar', '671': 'Movistar', '672': 'Movistar',
        '680': 'Movistar', '681': 'Movistar', '682': 'Movistar',
        '690': 'Movistar', '691': 'Movistar', '692': 'Movistar',
        
        # Vodafone
        '603': 'Vodafone', '604': 'Vodafone', '605': 'Vodafone',
        '613': 'Vodafone', '614': 'Vodafone', '615': 'Vodafone',
        '623': 'Vodafone', '624': 'Vodafone', '625': 'Vodafone',
        '633': 'Vodafone', '634': 'Vodafone', '635': 'Vodafone',
        '643': 'Vodafone', '644': 'Vodafone', '645': 'Vodafone',
        '653': 'Vodafone', '654': 'Vodafone', '655': 'Vodafone',
        '663': 'Vodafone', '664': 'Vodafone', '665': 'Vodafone',
        '673': 'Vodafone', '674': 'Vodafone', '675': 'Vodafone',
        '683': 'Vodafone', '684': 'Vodafone', '685': 'Vodafone',
        '693': 'Vodafone', '694': 'Vodafone', '695': 'Vodafone',
        
        # Orange
        '606': 'Orange', '607': 'Orange', '608': 'Orange',
        '616': 'Orange', '617': 'Orange', '618': 'Orange',
        '626': 'Orange', '627': 'Orange', '628': 'Orange',
        '636': 'Orange', '637': 'Orange', '638': 'Orange',
        '646': 'Orange', '647': 'Orange', '648': 'Orange',
        '656': 'Orange', '657': 'Orange', '658': 'Orange',
        '666': 'Orange', '667': 'Orange', '668': 'Orange',
        '676': 'Orange', '677': 'Orange', '678': 'Orange',
        '686': 'Orange', '687': 'Orange', '688': 'Orange',
        '696': 'Orange', '697': 'Orange', '698': 'Orange',
        
        # Yoigo
        '609': 'Yoigo', '619': 'Yoigo', '629': 'Yoigo',
        '639': 'Yoigo', '649': 'Yoigo', '659': 'Yoigo',
        '669': 'Yoigo', '679': 'Yoigo', '689': 'Yoigo',
        '699': 'Yoigo',
        
        # MásMóvil
        '607': 'MásMóvil', '608': 'MásMóvil',
        '617': 'MásMóvil', '618': 'MásMóvil',
        '627': 'MásMóvil', '628': 'MásMóvil',
        '637': 'MásMóvil', '638': 'MásMóvil',
        '647': 'MásMóvil', '648': 'MásMóvil',
        '657': 'MásMóvil', '658': 'MásMóvil',
        '667': 'MásMóvil', '668': 'MásMóvil',
        '677': 'MásMóvil', '678': 'MásMóvil',
        '687': 'MásMóvil', '688': 'MásMóvil',
        '697': 'MásMóvil', '698': 'MásMóvil',
    }
    
    # Tomar primeros 3 dígitos
    prefijo = numero[:3]
    return rangos.get(prefijo, "Desconocida")

# ============================================
# 3. FUNCIÓN PARA MÉXICO
# ============================================
def operadora_mexico(numero):
    """Identifica operadora en México"""
    
    # Los primeros 3 dígitos después de lada
    # Ejemplo: 55 1234 5678 (55 es CDMX)
    
    rangos = {
        '551': 'Telcel', '552': 'Telcel', '553': 'Telcel',
        '554': 'Movistar', '555': 'Movistar', 
        '556': 'AT&T', '557': 'AT&T',
        '558': 'Unefon', '559': 'Unefon',
        '561': 'Telcel', '562': 'Telcel',
        '563': 'Movistar', '564': 'Movistar',
        '565': 'AT&T', '566': 'AT&T',
        '568': 'Unefon', '569': 'Unefon',
        '644': 'Telcel', '645': 'Telcel',
        '646': 'Movistar', '647': 'AT&T',
        '656': 'Telcel', '664': 'Movistar',
        '662': 'Telcel', '663': 'Movistar',
        '668': 'Telcel', '669': 'Movistar',
        '686': 'Telcel', '687': 'Movistar',
        '744': 'Telcel', '745': 'Movistar',
        '771': 'Telcel', '772': 'Movistar',
        '999': 'Telcel', '998': 'Movistar',
    }
    
    if len(numero) >= 10:
        # Tomar dígitos 3-5 (dependiendo del formato)
        if numero.startswith('55'):  # CDMX
            prefijo = numero[2:5]
        else:
            prefijo = numero[:3]
        
        return rangos.get(prefijo, "Desconocida")
    
    return "Formato inválido"

# ============================================
# 4. FUNCIÓN PARA CONSULTAR API ONLINE
# ============================================
def consultar_operadora_online(pais, numero):
    """Intenta consultar operadora en APIs públicas"""
    
    apis = {
        'ES': f'https://api.adviceslip.com/advice',  # EJEMPLO - necesitarías API real
        'MX': f'https://api.adviceslip.com/advice',
        'CO': f'https://api.adviceslip.com/advice',
    }
    
    try:
        # NOTA: Necesitas una API real como:
        # - numverify.com (tiene API gratuita limitada)
        # - abstractapi.com/phone-validation-api
        # - verdad.com.mx/api-telefonos (México)
        
        print(f"    🔗 Buscar manualmente: 'operadora {numero} {pais}' en Google")
        return "Consulta manual necesaria"
        
    except:
        return "Error en consulta"

# ============================================
# 5. ANALIZAR CADA CANDIDATO
# ============================================
print("\n2. IDENTIFICANDO OPERADORAS:")

for pais, numero in candidatos:
    print(f"\n  📞 {pais} - Número: {numero}")
    
    if pais == "ES":
        operadora = operadora_espana(numero)
        print(f"    🏢 Operadora probable: {operadora}")
        
        # Tu número empieza con 686...
        if numero.startswith('686'):
            print(f"    📍 Prefijo 686: Orange o MásMóvil en España")
            print(f"    🔍 Detalle: Los números 686xxx xxx son móviles")
            
    elif pais == "MX":
        operadora = operadora_mexico(numero)
        print(f"    🏢 Operadora probable: {operadora}")
        
    elif pais == "CO":
        # Análisis simple para Colombia
        if numero.startswith('300') or numero.startswith('301') or numero.startswith('310'):
            print(f"    🏢 Operadora probable: Claro Colombia (móvil)")
        elif numero.startswith('315') or numero.startswith('316'):
            print(f"    🏢 Operadora probable: Movistar Colombia")
        elif numero.startswith('320') or numero.startswith('321'):
            print(f"    🏢 Operadora probable: Tigo Colombia")
        else:
            print(f"    🏢 Operadora: Consultar manualmente")
    
    # Intentar consulta online
    print(f"    🌐 Consulta online: ", end="")
    resultado_online = consultar_operadora_online(pais, numero)
    print(resultado_online)

# ============================================
# 6. ANÁLISIS ESPECÍFICO DE TU ID
# ============================================
print("\n" + "=" * 50)
print("3. ANÁLISIS DETALLADO DE TU ID:")
print("=" * 50)

print(f"ID completo: {id_largo}")
print(f"Longitud: {len(id_largo)} dígitos")

# Buscar patrones en el ID completo
print("\n🔎 PATRONES DENTRO DEL ID:")

# ¿Contiene prefijos conocidos?
prefijos_conocidos = ['686', '637', '633', '726', '662', '436']
for prefijo in prefijos_conocidos:
    if prefijo in id_largo:
        pos = id_largo.find(prefijo)
        print(f"  • Prefijo '{prefijo}' en posición {pos}")

# Dividir en posibles números
print("\n🧩 POSIBLES DIVISIONES:")
divisiones = [
    ("68-637-633", "Posible número + operadora"),
    ("686-376-337", "Formato típico español"),
    ("68637-63372-66624-36", "Como ID técnico"),
    ("686376337-26662436", "Número + timestamp/ID"),
]

for division, comentario in divisiones:
    print(f"  • {division} → {comentario}")

# ============================================
# 7. RECOMENDACIONES PRÁCTICAS
# ============================================
print("\n" + "=" * 50)
print("🎯 ¿CÓMO SABER LA OPERADORA REAL?")
print("=" * 50)

print("""
1. **PRUEBA DIRECTA** (más efectivo):
   - Llama al número candidato desde otro teléfono
   - En la pantalla suele aparecer la operadora
   - O contesta y pregunta educadamente

2. **BUSCAR EN REDES**:
   - WhatsApp: Añade como contacto → ver info
   - Truecaller: Muestra operadora a veces
   - Google: "686376337 operadora"

3. **APLICACIONES ESPECÍFICAS**:
   - Para España: '¿Quién me llama?' (App Store/Play Store)
   - Para México: 'Truecaller' o 'Whoscall'
   - Web: numeracion.es (España), portabilidad.mx (México)

4. **CON OPERADORA**:
   - Si tienes denuncia policial, ELLOS SÍ PUEDEN
   - Con tu ID completo y hora exacta de llamada
   - Te dirán operadora Y número real (con orden judicial)
""")

# ============================================
# 8. GENERAR REPORTE
# ============================================
print("\n💾 Generando reporte de análisis...")

reporte = f"""
REPORTE DE ANÁLISIS DE ID: {id_largo}
Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

MEJORES CANDIDATOS:
1. España (+34): {id_largo[:9]}
   • Prefijo: 686 → Orange/MásMóvil probable
   • Formato: +34 686 376 337

2. México (+52): {id_largo[:10]}
   • Prefijo: 686 → Posible Telcel/Movistar norte
   • Formato: +52 686 376 3372

3. Colombia (+57): {id_largo[:10]}
   • Prefijo: 686 → No típico en Colombia

RECOMENDACIONES:
- Prueba llamar a: +34 686 376 337
- Busca en Truecaller ese número
- Si es acoso: Guarda ID completo y denuncia
"""

with open('analisis_operadora.txt', 'w', encoding='utf-8') as f:
    f.write(reporte)

print("✅ Reporte guardado en 'analisis_operadora.txt'")
print("\n⚠️ Recuerda: La única forma segura de saber la operadora")
print("   es que tu compañía telefónica te lo diga (con denuncia).")