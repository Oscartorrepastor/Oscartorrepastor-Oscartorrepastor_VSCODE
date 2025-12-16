class tarea{
    // atributos
    nombre
    fecha
    prioridad
    //constructores 1 solo 
    constructor(nombre,fecha,prioridad){
        this.nombre=nombre
        this.fecha=fecha
        this.prioridad=prioridad
    }
    //metodos

    /**
     * 
     */
    mostrarDatos() {
        console.log(`El nombre es ${this.nombre}`)
        console.log(`La fecha es ${this.fecha}`)
        console.log(`La prioridad es ${this.prioridad}`)
    }

        // getter setter

        getNombre(){
            return this.nombre
        }
        setNombre(nombre){
            this.nombre = nombre
        }
}

let tarea1 = new tarea("tarea1", new Date(), "Alta")
tarea1.setNombre("Tarea prioritaria")
tarea1.getNombre()
tarea1.mostrarDatos()