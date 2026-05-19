// MOTOR DE SINCRONIZACIÓN DE TELEMETRÍA DE RED // CORTEX v8.0
const WORKER_URL = 'https://workers.dev';

async function sincronizarEstadoSoberano() {
    try {
        const respuesta = await fetch(`${WORKER_URL}/api/v1/state`);
        if (!respuesta.ok) throw new Error(`HTTP_ERROR: ${respuesta.status}`);
        const datos = await respuesta.json();
        
        if (datos.operadorResiliencia) estado.resiliencia = datos.operadorResiliencia;
        if (datos.presupuestoLocal) estado.presupuesto = datos.presupuestoLocal;
        if (datos.ivaAplicado) estado.iva = datos.ivaAplicado;
        if (datos.currentChaos) {
            const chaosEl = document.getElementById('m-chaos');
            if (chaosEl) chaosEl.innerText = datos.currentChaos;
        }
        
        updateUI();
    } catch (error) {
        console.error('[SYNC_ERROR] Error de comunicación con el Worker:', error.message);
    }
}

async function inyectarVotoWorker(votoIndex) {
    try {
        console.log(`[UPLINK] Transmitiendo acción táctica: ${votoIndex}`);
        const respuesta = await fetch(`${WORKER_URL}/api/v1/simulation/vote`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ vote_index: votoIndex })
        });
        
        if (!respuesta.ok) throw new Error(`VOTE_ERROR: ${respuesta.status}`);
        await sincronizarEstadoSoberano();
    } catch (error) {
        console.error('[SYNC_ERROR] Fallo en la transmisión del comando:', error.message);
    }
}

window.triggerAccion = function(tipo) {
    if (tipo === 'iva') inyectarVotoWorker('iva');
    if (tipo === 'presupuesto') inyectarVotoWorker('presupuesto');
    if (tipo === 'golpe') inyectarVotoWorker('golpe');
};

setInterval(sincronizarEstadoSoberano, 4000);
document.addEventListener('DOMContentLoaded', sincronizarEstadoSoberano);
