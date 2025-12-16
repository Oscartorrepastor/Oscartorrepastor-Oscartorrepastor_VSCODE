// funcipnes nominales o de flecha

// nominales --> function(parametros){}
function realizarCalculo(op1, op2) {
    console.log(`la suma de los dos parametros es ${op1 + op2}`)
}

realizarCalculo(3, 8)

function caluloRetorno(op1, op2) {
    return op1 + op2
}

function caluloRetorno(op1, op2 = 7) {
    return op1 + op2
}

function operacionFantasma(op1) {
    console.log(`El numero de atgumentos es de ${arguments.length}`);
    
}

operacionFantasma(1, 2, 3, 4)