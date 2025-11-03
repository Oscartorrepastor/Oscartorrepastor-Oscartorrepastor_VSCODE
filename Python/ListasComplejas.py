# Ejercicio 1: Tabla de multiplicar 

tabla = int(input("Dime la tabla de multiplicar que quieres saber: "))
for i in range(1, 11):
    print(f"{tabla} x {i} = {tabla * i}")
print("\n")

# Ejercicio 2: Semi-Tirangulo de asteriscos

filas = int(input("Cuantas filas de asteriscos quieres: "))
for i in range(1, filas + 1):
    print('*' * i)
print("\n")

# Ejercicio 3: Patron de numeros

filas = int(input("De cuanto es el patron de numeros: "))
for i in range(1, filas + 1):
    for j in range(1, filas + 1):
        print(j, end=' ')
    print()
print("\n")

# Ejercicio 4a: Matriz de ceros 

filas = int(input("De cuanto quieres que sea la matriz: "))
for i in range(filas):
    for j in range(filas):
        print(0, end=' ')
    print()
print("\n")

# Ejercicio 4b: Modificar

filas = int(input("De cuanto quieres que sea la matriz aleatorial: "))
import random as match
for i in range(filas):
    for j in range(filas):
        numero = match.randint(1, 10)
        if numero % 2 == 0:
            numero += 1        
        print(numero, end=' ')
    print()
print("\n")

# Ejercicio 4c: Rellena matriz

n = int(input("Introduce el tamaño de la matriz (n): "))
matriz = []
for i in range(n):
        fila = []
        for j in range(n):
            num = int(input(f"Introduce el número para la posición [{i}][{j}]: "))
            fila.append(num)
        matriz.append(fila)
for fila in matriz:
        print(fila)
print("\n")

# Ejercicio 5: Suma de matrices

n = int(input("De cuanto quieres que sea la matriz: "))
matriz1 = []
matriz2 = []
suma_matrices = []
print("Rellena la primera matriz:")
for i in range(n):
    fila = []
    for j in range(n):
        num = int(input(f"Introduce el número para la posición [{i}][{j}]: "))
        fila.append(num)
    matriz1.append(fila)
print("Rellena la segunda matriz:")
for i in range(n):
    fila = []
    for j in range(n):
        num = int(input(f"Introduce el número para la posición [{i}][{j}]: "))
        fila.append(num)
    matriz2.append(fila)
for i in range(n):
    fila_suma = []
    for j in range(n):
        suma = matriz1[i][j] + matriz2[i][j]
        fila_suma.append(suma)
    suma_matrices.append(fila_suma)
for fila in suma_matrices:
    print(fila)
print("\n")

# Ejercicio 6: Calculo de la suma de fila y columna en una matriz

n = int(input("De cuanto quieres que sea la matriz: "))
matriz = []
print("Rellena la matriz:")
for i in range(n):
    fila = []
    for j in range(n):
        num = int(input(f"Introduce el número para la posición [{i}][{j}]: "))
        fila.append(num)
    matriz.append(fila)
suma_filas = []
suma_columnas = [0] * n
for i in range(n):
    suma_fila = sum(matriz[i])
    suma_filas.append(suma_fila)
    for j in range(n):
        suma_columnas[j] += matriz[i][j]
for i in range(n):
    print(f"Suma de la fila {i}: {suma_filas[i]}")
for j in range(n):
    print(f"Suma de la columna {j}: {suma_columnas[j]}")
print("\n")

# Ejercicio 7: Dibujo de rombo

filas = int(input("Cuantas filas quieres que tenga el rombo (debe ser impar): "))
if filas % 2 == 0:
    print("El número debe ser impar.")
else:
    mitad = filas // 2
    for i in range(mitad + 1):
        print(' ' * (mitad - i) + '*' * (2 * i + 1))
    for i in range(mitad - 1, -1, -1):
        print(' ' * (mitad - i) + '*' * (2 * i + 1))
print("\n")

# Ejercicio 8: Dada la suiguiente matriz realiza la suma de sus diagonales
matriz = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25]
]
suma_diagonal_principal = 0
suma_diagonal_secundaria = 0
n = len(matriz)
for i in range(n):
    suma_diagonal_principal += matriz[i][i]
    suma_diagonal_secundaria += matriz[i][n - 1 - i]
print(f"Suma de la diagonal principal: {suma_diagonal_principal}")
print(f"Suma de la diagonal secundaria: {suma_diagonal_secundaria}")
print("\n")

# Ejercicio 9: Igual que el anterior pero por teclado

n = int(input("De cuanto quieres que sea la matriz: "))
matriz = []
print("Rellena la matriz:")
for i in range(n):
    fila = []
    for j in range(n):
        num = int(input(f"Introduce el número para la posición [{i}][{j}]: "))
        fila.append(num)
    matriz.append(fila)
suma_diagonal_principal = 0
suma_diagonal_secundaria = 0
for i in range(n):
    suma_diagonal_principal += matriz[i][i]
    suma_diagonal_secundaria += matriz[i][n - 1 - i]
print(f"Suma de la diagonal principal: {suma_diagonal_principal}")
print(f"Suma de la diagonal secundaria: {suma_diagonal_secundaria}")
print("\n")
