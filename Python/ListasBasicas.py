# Ejercicio 1 
lista = ["melocoton", "pera", "manzana", "platano", "uva"]  
print("Lista: ", lista)
print("Primer elemento: ", lista[0], ", Ultimo elemento: ", lista[-1])

#Ejercico 2
lista2 = []
lista2.append(1)
lista2.append(2)
lista2.append(3)

lista2.remove(2)
print( lista2)

#Ejercicio 3
lista3 =[1, 2, 3, 4, 5]

for i in range(len(lista3)):
    lista3[i] = lista3[i] * 2
print(lista3)

#Ejercicio 4
lista4 = ["manzana", "pera", "naranja"]
buscar = input("Ingrese una fruta a buscar: ")
if buscar in lista4:
    print("La fruta se encuentra en la lista")
else:
    print("La fruta no se encuentra en la lista")

#Ejercicio 5
lista5 = list(range(1, 11))
print("Los tra primeros numeros son: ", lista5[:3])
print("Los tres ultimos numeros son: ", lista5[-3:])
print("Los numeros del medio son: ", lista5[3:7])
