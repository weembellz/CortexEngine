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
        
        
    }, 4000);
}

function optimizarIVA() {
    
    estadoSistema.ivaAplicado = 10;
    estadoSistema.operadorResiliencia = Math.min(100, estadoSistema.operadorResiliencia + 5);
}

function ajustePresupuestario() {
    
    estadoSistema.presupuestoLocal -= 75000;
    estadoSistema.operadorResiliencia = Math.max(0, estadoSistema.operadorResiliencia - 10);
}

function iniciarInterfazTeclado() {
    readline.emitKeypressEvents(process.stdin);
    if (process.stdin.isTTY) process.stdin.setRawMode(true);

    process.stdin.on('keypress', (str, key) => {
        if ((key && key.ctrl && key.name === 'c') || str === '3') {
            
            process.exit();
        }
        if (str === '1') optimizarIVA();
        if (str === '2') ajustePresupuestario();
    });
}

console.clear();








iniciarMonitoreo();
iniciarInterfazTeclado();

