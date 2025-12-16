
let nombre = prompt("¿Cuál es tu nombre?");

let num1, num2;

while (true) {
    let input1 = prompt("Primer número:");
    num1 = parseFloat(input1);
    if (!isNaN(num1)) break;
    alert("¡Debe ser un número!");

    let input2 = prompt("Segundo número:");
    num2 = parseFloat(input2);
    if (!isNaN(num2)) break;
    alert("¡Debe ser un número!");
}

// Pedir operación
let op = prompt("Operación (+, -, *, /):");

// Calcular
let resultado;
if (op === '+') resultado = num1 + num2;
else if (op === '-') resultado = num1 - num2;
else if (op === '*') resultado = num1 * num2;
else if (op === '/') {
    if (num2 === 0) resultado = "No se divide entre 0";
    else resultado = num1 / num2;
} else {
    resultado = "Operación inválida";
}


alert("Resultado: " + resultado);