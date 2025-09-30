# 1 - Escribie un programa que calcule la suma de los numeros del 1 al 10

suma = 0
for i in range(1, 11):
    suma += i
print(f"La suma de los numeros del 1 al 10 es: {suma}")

# 2 - Crea un programa que calcule el factorial de un numero introducido por el usuario

factorial = 1
numero = int(input("Introduce un numero para calcular su factorial: "))
for i in range(1, numero + 1):
    factorial *= i
print(f"El factorial de {numero} es {factorial}")

# 3 - Diseña un programa que muestre los números primos entre 1 y 50

#import sympy 

print("Numeros primos entre 1 y 50:")
for num in range(2, 51):
    esPrimo = True
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            esPrimo = False
            break
    if esPrimo:
        print(num) 

# 4 - Realiza un programa que calcule la suma de los dígitos de un número entero ingresado por el usuario

numero = input("Introduce un numero entero: ")
sumaDigitos = 0
for digito in numero:
    sumaDigitos += int(digito)
print(f"La suma de los digitos de {numero} es {sumaDigitos}")

# 5 - Realiza un programa que sume los números pares del 1 al 100

sumaPares = 0
for i in range(2, 101, 2):
    sumaPares += i
print(f"La suma de los numeros pares del 1 al 100 es: {sumaPares}")

# 6 - Realiza un programa que calcule el area de un triangulo dado su base y altura

base = float(input("Introduce la base del triangulo: "))
altura = float(input("Introduce la altura del triangulo: "))
area = (base * altura) / 2
print(f"El area del triangulo es: {area}")

# 7 - Realiza un programa que muestre los nuemros del 1 al 100 pero que remplaze los multiplos de 3 por "Fizz", los multiplos de 5 por "Buzz" 
# y los multiplos de ambos por "FizzBuzz"

for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("Fizz Buzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

# 8 - Crea un programa que simule un juego de adivinanza donde el usuario debe adivinar un numero aleatorio generado por la computadora

import random
numero = random.randint(1, 11)
print("Adivina el numero entre 1 y 11")
while True:
    intento = int(input("Introduce un numero: "))
    if intento < numero:
        print("Numero muy bajo")
    elif intento > numero:
        print("Numero muy alto")
    else:
        print(f"El numero es correcto {numero}")
        break

# 10 - Realiza un programa que cuente cuántas vocales hay en una cadena de texto ingresada por el usuario

texto = input("Introduce una cadena de texto: ")
vocales = "aeiouAEIOU"
contador = 0
for char in texto:
    if char in vocales:
        contador += 1
print(f"El numero de vocales en la cadena es: {contador}")

# 12 - Escribe un programa que calcule el área de un círculo dado su radio

import math
radio = float(input("Introduce el radio del circulo: "))
area = math.pi * (radio ** 2)
print(f"El area del circulo es: {area}")


