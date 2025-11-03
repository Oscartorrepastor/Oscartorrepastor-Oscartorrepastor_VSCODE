# Hacer Calcualdora cinetifica

import math
import sys

# Importar librerias colorama

from colorama import init, Fore
init(autoreset=True)

# Agregar contraseña a la calculadora

def solicitar_contrasena():
    contrasena_correcta = "1234"
    intentos = 3
    while intentos > 0:
        contrasena = input("🚀Ingrese la contrasena para acceder a la calculadora: ")
        if contrasena == contrasena_correcta:
            print(Fore.GREEN + "Acceso concedido.")
            return True
        else:
            intentos -= 1
            print(Fore.RED + f"😭😭 Contrasena incorrecta. Le quedan {intentos} intentos.😭😭")
    print(Fore.RED + "😭😭 Acceso denegado. Saliendo del programa.😭😭")
    return False

# Funciones basicas

def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        return "Error: Division por cero"
    return a / b

def valor_absoluto(a):
    return abs(a)

def tangente(a):
    return math.tan(math.radians(a))

def seno(a):
    return math.sin(math.radians(a))

def coseno(a):
    return math.cos(math.radians(a))

def logaritmo(a):
    if a <= 0:
        return "Error: Logaritmo de numero no positivo"
    return math.log10(a)

def logaritmo_neperiano(a):
    if a <= 0:
        return "Error: Logaritmo de numero no positivo"
    return math.log(a)

def euler_exponencial(a):
    return math.exp(a)

def raiz_cuadrada(a):
    if a < 0:
        return "Error: Raiz cuadrada de numero negativo"
    return math.sqrt(a)

# Menu de opciones

def menu():
    print("🚀🚀Calculadora Cientifica🚀🚀")
    print("1. ➕")
    print("2. ➖")
    print("3. ✖️")
    print("4. ➗")
    print("5. ➖🔄")
    print("6. 📐tan")
    print("7. 📝🔢✖️📐")
    print("8. 📐cos")
    print("9. 🔟log")
    print("10. ℯln")
    print("11. 𝑒ˣ")
    print("12. √")
    print("13. Salir")

# Ejecutar calculadora

def calculadora():
    if not solicitar_contrasena():
        sys.exit()

    while True:
        menu()
        opcion = input("Seleccione una opcion (1-13): ")

        if opcion == '1':
            a = float(input("Ingrese el primer numero: "))
            b = float(input("Ingrese el segundo numero: "))
            print(Fore.CYAN + f"Resultado: {sumar(a, b)}")

        elif opcion == '2':
            a = float(input("Ingrese el primer numero: "))
            b = float(input("Ingrese el segundo numero: "))
            print(Fore.CYAN + f"Resultado: {restar(a, b)}")

        elif opcion == '3':
            a = float(input("Ingrese el primer numero: "))
            b = float(input("Ingrese el segundo numero: "))
            print(Fore.CYAN + f"Resultado: {multiplicar(a, b)}")

        elif opcion == '4':
            a = float(input("Ingrese el primer numero: "))
            b = float(input("Ingrese el segundo numero: "))
            print(Fore.CYAN + f"Resultado: {dividir(a, b)}")

        elif opcion == '5':
            a = float(input("Ingrese un numero: "))
            print(Fore.CYAN + f"Resultado: {valor_absoluto(a)}")

        elif opcion == '6':
            a = float(input("Ingrese un angulo en grados: "))
            print(Fore.CYAN + f"Resultado: {tangente(a)}")

        elif opcion == '7':
            a = float(input("Ingrese un angulo en grados: "))
            print(Fore.CYAN + f"Resultado: {seno(a)}")

        elif opcion == '8':
            a = float(input("Ingrese un angulo en grados: "))
            print(Fore.CYAN + f"Resultado: {coseno(a)}")

        elif opcion == '9':
            a = float(input("Ingrese un numero positivo: "))
            print(Fore.CYAN + f"Resultado: {logaritmo(a)}")

        elif opcion == '10':
            a = float(input("Ingrese un numero positivo: "))
            print(Fore.CYAN + f"Resultado: {logaritmo_neperiano(a)}")

        elif opcion == '11':
            a = float(input("Ingrese un numero: "))
            print(Fore.CYAN + f"Resultado: {euler_exponencial(a)}")

        elif opcion == '12':
            a = float(input("Ingrese un numero no negativo: "))
            print(Fore.CYAN + f"Resultado: {raiz_cuadrada(a)}")
        elif opcion == '13':
            print(Fore.YELLOW + "Saliendo de la calculadora. ¡Hasta luego!")
            break
        else:
            print(Fore.RED + "Opcion no valida. Intente de nuevo.")

calculadora()

        