let boton = document.querySelector("#btn-primary")
let parrafo = document.querySelector("#contenido")
boton.addEventListener("click",() =>{

    let tarea1 = new tarea("Tarea1", new Date(), "Baja")
    tarea1.mostrarDatos()

})
