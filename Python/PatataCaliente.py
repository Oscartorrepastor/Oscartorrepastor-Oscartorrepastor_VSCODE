# Juego de la Patata Caliente

import time
import random



# El tiepo tiene que estar entre 8 y 15 segundos
tiempoLimite = random.randint (8, 15)
print(tiempoLimite)

# Nuemro ente 1 y 100 incluidos
numero = random.randint (1, 101)
print("El numero secreto es: ",numero)

# Se puede indicar por pantalla, si lo prefieres (no es obligatorio), el tiempo que hay para adivinar el número

tiempo = time.time()

# Si se termina el tiempo, se indica que has perdido, que se ha terminado el programa y el número que se tendría que haber encontrado.

# Si lo encuentras, felicitas al usuario.

print(f"Tienes {tiempoLimite} segundos para adivinar el numero entre 1 y 100")

while True:
    if time.time() - tiempo > tiempoLimite:
        print(f"Se acabo el tiempo\n")
        print(f"El numero era: {numero}")
        break

    intento = input("Que numero crees que es: ")

    if not intento.isdigit():
        print("Solo se permiten numeros enteros")
        continue

    intento = int(intento)

    if intento == numero:
        print("Has adivinado el número")
        break

    elif intento < numero:
        print("El numero es mayor")
    else:
        print("El numero es menor")
