const fs = require('fs');
const readline = require('readline');

// Estado inicial en Tàrrega
const estadoSistema = {
    operadorResiliencia: 85,
    presupuestoLocal: 500000,
    ivaAplicado: 21,
    ultimaActualizacion: ""
};

const LOG_FILE = './log_simulacion.json';

function guardarLog() {
    try {
        let historial = [];
        if (fs.existsSync(LOG_FILE)) {
            const contenido = fs.readFileSync(LOG_FILE, 'utf8');
            historial = contenido ? JSON.parse(contenido) : [];
        }
        historial.push({ ...estadoSistema });
        fs.writeFileSync(LOG_FILE, JSON.stringify(historial, null, 2));
    } catch (error) {
        // Silencioso en terminal para no romper el flujo visual
    }
}

function iniciarMonitoreo() {
    setInterval(() => {
        estadoSistema.ultimaActualizacion = new Date().toLocaleTimeString();
        guardarLog();
        console.log(`\n[MONITOR - ${estadoSistema.ultimaActualizacion}] Estado actual:`, estadoSistema);
        process.stdout.write("Acción (1: IVA, 2: Presupuesto, 3: Salir): ");
    }, 4000);
}

function optimizarIVA() {
    console.log("\n\n[EJECUTANDO] Optimización de IVA...");
    estadoSistema.ivaAplicado = 10;
    estadoSistema.operadorResiliencia = Math.min(100, estadoSistema.operadorResiliencia + 5);
}

function ajustePresupuestario() {
    console.log("\n\n[EJECUTANDO] Ajuste presupuestario...");
    estadoSistema.presupuestoLocal -= 75000;
    estadoSistema.operadorResiliencia = Math.max(0, estadoSistema.operadorResiliencia - 10);
}

function iniciarInterfazTeclado() {
    readline.emitKeypressEvents(process.stdin);
    if (process.stdin.isTTY) process.stdin.setRawMode(true);

    process.stdin.on('keypress', (str, key) => {
        if ((key && key.ctrl && key.name === 'c') || str === '3') {
            console.log("\n\nCerrando Industrial Gateway v4.5...");
            process.exit();
        }
        if (str === '1') optimizarIVA();
        if (str === '2') ajustePresupuestario();
    });
}

console.clear();
console.log("=================================================");
console.log(" Iniciando Industrial Gateway v4.5 en Tàrrega   ");
console.log("=================================================");
console.log("Controles interactivos inmediatos:");
console.log(" [1] Optimizar IVA");
console.log(" [2] Ajuste Presupuestario");
console.log(" [3] o Ctrl+C para Salir\n");

iniciarMonitoreo();
iniciarInterfazTeclado();
process.stdout.write("Acción (1: IVA, 2: Presupuesto, 3: Salir): ");
