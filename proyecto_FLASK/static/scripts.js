
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("buscador");

    if(input){
        input.addEventListener("keyup", () => {
            let filtro = input.value.toLowerCase();
            let filas = document.querySelectorAll("#tabla tr");

            filas.forEach((fila, i) => {
                if(i === 0) return;
                let texto = fila.innerText.toLowerCase();
                fila.style.display = texto.includes(filtro) ? "" : "none";
            });
        });
    }
});
function modo(){
    document.body.classList.toggle("dark");
}