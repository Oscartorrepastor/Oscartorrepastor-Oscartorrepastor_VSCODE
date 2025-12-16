const listas = ["Compras", "Tareas", "Proyectos", "Ideas", "Libros por leer"];
listas.push("Palabra nueva")
listas.unshift("Elemento 1", "Elemento 2")
listas[2] = "Elemnto mio"

listas.pop()
listas.shift()

listas = listas.filter((element)=>  {
    return element != "Tareas"
});

console.log(listas);