// OSCILOSCOPIO GEOPOLÍTICO ASÍNCRONO DE UN PÍXEL // CORE v7.2
function inicializarPlotterAtemporal() {
    const canvas = document.getElementById('canvas-orbital');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    // Forzar renderizado pixelado nativo sin interpolación
    canvas.style.imageRendering = 'pixelated';
    ctx.imageSmoothingEnabled = false;

    let arrayPuntos = Array(100).fill(0);
    
    function redimensionar() {
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = 120;
    }
    window.addEventListener('resize', redimensionar);
    redimensionar();

    function bucleRender() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Rejilla de Fondo Táctica
        ctx.strokeStyle = '#111111';
        ctx.lineWidth = 1;
        const pasoGrilla = 20;
        for (let x = 0; x < canvas.width; x += pasoGrilla) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += pasoGrilla) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }

        // Simulación de coeficientes de ruido técnico
        const coefCaos = parseFloat(document.getElementById('m-chaos')?.innerText) || 0.55;
        const hIndex = parseFloat(document.getElementById('m-hindex')?.innerText) || 7.42;
        
        let nuevoPunto = (canvas.height / 2) + (Math.sin(Date.now() * 0.005) * hIndex * 2) + ((Math.random() - 0.5) * canvas.height * coefCaos);
        arrayPuntos.push(nuevoPunto);
        if (arrayPuntos.length > canvas.width) arrayPuntos.shift();

        // Línea de Fósforo en Oro Mate (#D4AF37) de 1 píxel
        ctx.strokeStyle = '#D4AF37';
        ctx.lineWidth = 1;
        ctx.beginPath();
        for (let i = 0; i < arrayPuntos.length; i++) {
            if (i === 0) ctx.moveTo(i, arrayPuntos[i]);
            else ctx.lineTo(i, arrayPuntos[i]);
        }
        ctx.stroke();

        if (coefCaos > 0.75 && Math.random() > 0.85) {
            ctx.fillStyle = 'rgba(220, 38, 38, 0.15)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        requestAnimationFrame(bucleRender);
    }
    requestAnimationFrame(bucleRender);
}

// Inyección limpia en la ventana global
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializarPlotterAtemporal);
} else {
    inicializarPlotterAtemporal();
}
