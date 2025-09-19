# Ejercicio 1 
# Diferencias entre paradigma imperativo y declarativo

# Imperativo: Indica paso a paso como de debe realizar una tarea

# Declarativo: Describe el resultado que se quieres tener sin decir como hacerlo

# Ejercicio 2 
# Paradigma Imperativo

# Para hacer un sandwich: 1º - Ir a la cocicna 2º - abrir el armario 
# 3º - sacar el pan 4º - abrir la nevera 
# 5º - sacar el jamon y el queso 6º - hacer el sandwich 
# 7º - comer el sandwich

# Ejercicio 3 
# Paradigma Orientado a Objetos

# Permite que el codigo sea reutilizado, organizado y sencillo de mantener 

# Ejercicio 4 
# Tipado Dinamico

# Una variable no necesita ser declarada como un yipo expecifico al momnto de 
# crearla, puede contener diferentes tipos de valores a lo largo de su vida.

# Ejercicio 5 
# Implementa los siguientes ejercicios en Python

# 5.1 - Suma de números

num1 = int(input("Introduce el primer número: "))
num2 = int(input("Introduce el segundo número: "))
suma = num1 + num2
print ("La suma es:", suma)

# 5.2 - Calculadora de area de un cuadrado

lado = int(input("Introduce el lado del cuadrado: "))
lado * lado
print("El área del cuadrado es:", lado * lado)

# 5.3 - Conversion de temperatura

celsius = int(input("Introduce la temperatura en grados Celsius: "))
fahrenheit = (celsius * 9/5) + 32
print("La temperatura en grados Fahrenheit es:", fahrenheit)

# 5.4 - Calculadora de IMC
peso = int(input("Introduce tu peso en kg: "))
altura = int(input("Introduce tu altura en metros: "))
#imc = peso / (altura ** 2)
print(f"Tu índice de masa corporal es:", {peso / (altura ** 2)})

# 5.5 - Concatenación de cadenas: 

cadena1 = input("Introduce la primera cadena: ")
cadena2 = input("Introduce la segunda cadena: ")
cadenaConcatenada = cadena1 + " " + cadena2
print("La cadena concatenada es:", cadenaConcatenada)

# 5. 6 Determinar el tipo de dato:


# 5.7 Calcular el promedio de tres números:

num1 = int(input("Introduce el primer número: "))
num2 = int(input("Introduce el segundo número: "))
num3 = int(input("Introduce el tercer número: "))
promedio = (num1 + num2 + num3) / 3
print("El promedio es:", promedio)

# 5.8 Área de un triángulo:

base = int(input("Introduce la base del triángulo: "))
altura = int(input("Introduce la altura del triángulo: "))
area = (base * altura) / 2
print("El área del triángulo es:", area)

# 5.9 Edad en el futuro:

edadActual = int(input("Introduce tu edad actual: "))
añosFuturo = int(input("Introduce el número de años en el futuro: "))
edadFutura = edadActual + añosFuturo
print("Tu edad en", añosFuturo, "años será:", edadFutura)

# 5.10 Área de un rectángulo:

largo = int(input("Introduce el largo del rectángulo: "))
ancho = int(input("Introduce el ancho del rectángulo: "))
area = largo * ancho
print("El área del rectángulo es:", area)

# 5.11 Días a segundos:

dias = int(input("Introduce el número de días: "))
segundos = dias * 24 * 60 * 60
print(dias, "días son", segundos, "segundos")

# 5.12 Raíz cuadrada:

num = int(input("Introduce un número: "))
raiz_cuadrada = num ** 0.5
print("La raíz cuadrada de", num, "es:", raiz_cuadrada)

# 5.13 Conversión de moneda:

euros = float(input("Introduce la cantidad en euros: "))
tasa_cambio = 1.1  # Ejemplo de tasa de cambio
dolares = euros * tasa_cambio
print(euros, "euros son", dolares, "dólares")
