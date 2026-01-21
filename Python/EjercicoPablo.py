def torres_hanoi(n, origen, destino, auxiliar):
    if n == 1:
        print(f"Mover disco 1 de {origen} a {destino}")
    else:
        torres_hanoi(n - 1, origen, auxiliar, destino)
        print(f"Mover disco {n} de {origen} a {destino}")
        torres_hanoi(n - 1, auxiliar, destino, origen)


# Programa principal
if __name__ == "__main__":
    n = int(input("Introduce el número de discos: "))
    
    print(f"\nSolución para {n} discos:\n")
    torres_hanoi(n, "Origen", "Destino", "Auxiliar")
    
    movimientos_minimos = 2**n - 1
    print(f"\nNúmero mínimo de movimientos: {movimientos_minimos}")