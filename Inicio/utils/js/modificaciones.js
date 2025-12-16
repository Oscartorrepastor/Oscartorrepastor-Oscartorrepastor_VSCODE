let botonAgregar = document.querySelector("#btnAgregar")
let botonLimpiar = document.querySelector("#btnLimpiar")
let botonVaciar = document.querySelector("#btnVaciar")

let nombreInput = document.querySelector("#nombreInput")
let apellidoInput = document.querySelector("#apellidoInput")
let inputfecha = document.querySelector("#inputfecha")
let inputedad = document.querySelector("#inputedad")

let listaAgregados = document.querySelector("#listaAgregados ul")

botonAgregar.addEventListener("click", (evet)=>{
   let nombre = nombreInput.value 
   let apellido = apellidoInput.value
   let fecha = inputfecha.value
   let edad = inputedad.value

   if(nombre === "" || apellido === "" || fecha === "" ){
    lanzarAlerta("Error","Por favor completa todos los campos","error")
    return
   }else{
    agregarLi(nombre, apellido, fecha)
   console.log(`Nombre ${nombre}, apellido ${apellido}, fecha ${fecha}, edad ${edad}`);
   }
})

botonVaciar.addEventListener("click", (event)=> {

    listaAgregados.innerHTML="";
})

botonLimpiar.addEventListener("click",(evet)=> {
    nombreInput.value = ""
    apellidoInput.value = ""
    inputfecha.value = ""
    inputedad.value = "disabled selected"
    
    listaAgregados.innerHTML = ""

    lanzarAlerta("Formulario limpiado", "Se han limpiado los campos del formulario", "success")
})

function lanzarAlerta(title, text, icon){
    Swal.fire({
  title: title,
  text: text,
  icon: icon
});
}



function agregarLi(nombre, apellido, fecha){
    let li = document.createElement("li")
    let btnEliminar = document.createElement("Button")

    btnEliminar.classList.add("btn", "btn-danger");
    btnEliminar.innerText = "Borrar";
    btnEliminar.addEventListener("click", (e) => {
        li.classList.remove("animate__fadeIn")
        li.classList.add("animate__bounceInRight")
        setTimeout(() =>{
            li.classList.remove("animate__fadeIn")
            li.classList.add("animate__bounceInRight")
            setTimeout(() => {
                li.remove();
            }, 600);
        }, 600)
        
    });

    li.classList.add("list-group-item", "animate__animated", "animate__fadeIn")
    li.textContent = `Nombre: ${nombre}, Apellido: ${apellido}, Fecha de Nacimiento: ${fecha}`
    li.appendChild(btnEliminar)
    

    listaAgregados.appendChild(li)
    

    lanzarAlerta("Agregado","Elemento agregado a la lista","success")
}

/*
añadir boton eliminar para ir borrando los elementos de uno en uno de la lista
hay que añadir el boton en el li creado y luego añadirle un event listener para que borre el li padre
lanzar una alerta de confirmacion antes de borrar el elemento
*/