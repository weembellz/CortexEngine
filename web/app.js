/**
 * CORTEX OS - HUD Core Operations
 * Gestiona la conexion por WebSockets y peticiones REST hacia la API v1.
 */

const CONFIG = {
    wsUrl: `ws://${window.location.hostname}:5005/api/v1/ws`,
    apiUrl: `${window.location.protocol}//${window.location.hostname}:5005/api/v1`
};

let socket = null;
let map = null;
let markersLayer = null;

function initHUD() {
    console.log("[INIT] Inicializando paneles del Mando Central...");
    initMap();
    connectWebSocket();
    setupEventListeners();
}

function initMap() {
    if (typeof L !== 'undefined') {
        map = L.map('map-container').setView([40.4167, -3.7037], 6);
        L.tileLayer('https://{s}://{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors &copy; <a href="https://carto.com">CARTO</a>'
        }).addTo(map);
        markersLayer = L.layerGroup().addTo(map);
    } else {
        console.warn("[WARN] Leaflet.js no detectado. El panel del mapa operará en modo degradado.");
    }
}

function connectWebSocket() {
    console.log(`[WS] Estableciendo enlace con el Edge local: ${CONFIG.wsUrl}`);
    socket = new WebSocket(CONFIG.wsUrl);

    socket.onopen = () => {
        console.log("[WS] Conexión reactiva Pub/Sub establecida.");
        const indicator = document.getElementById("status-indicator");
        if (indicator) indicator.className = "status-online";
    };

    socket.onmessage = (event) => {
        try {
            const state = JSON.parse(event.data);
            renderState(state);
        } catch (err) {
            console.error("[WS] Error al procesar payload de datos:", err);
        }
    };

    socket.onclose = () => {
        console.warn("[WS] Enlace cerrado. Reintentando conexión en 5 segundos...");
        const indicator = document.getElementById("status-indicator");
        if (indicator) indicator.className = "status-offline";
        setTimeout(connectWebSocket, 5000);
    };

    socket.onerror = (error) => {
        console.error("[WS] Fallo crítico en socket:", error);
    };
}

function renderState(state) {
    if (!state) return;

    if (state.simulation) {
        const hIndex = document.getElementById("metric-hindex");
        const inflation = document.getElementById("metric-inflation");
        const corruption = document.getElementById("metric-corruption");
        const defcon = document.getElementById("metric-defcon");

        if (hIndex) hIndex.innerText = Number(state.simulation.h_index).toFixed(2);
        if (inflation) inflation.innerText = Number(state.simulation.inflation_rate).toFixed(1) + "%";
        if (corruption) corruption.innerText = state.simulation.corruption_index + "%";
        if (defcon) defcon.innerText = state.simulation.defcon_level;
    }
    
    if (state.infrastructure) {
        const sefaTemp = document.getElementById("sefa-temp");
        const sefaHum = document.getElementById("sefa-hum");

        if (sefaTemp) sefaTemp.innerText = Number(state.infrastructure.terrarium_temperature_celsius).toFixed(1) + "°C";
        if (sefaHum) sefaHum.innerText = Number(state.infrastructure.terrarium_humidity_percentage).toFixed(1) + "%";
        
        const muscleStatus = state.infrastructure.node_muscle_status;
        const powerBtn = document.getElementById("btn-power");
        if (powerBtn) {
            powerBtn.innerText = muscleStatus === "ONLINE" ? "APAGAR MÚSCULO" : "ENCENDER MÚSCULO";
            powerBtn.className = muscleStatus === "ONLINE" ? "btn-danger" : "btn-success";
        }
    }
    
    if (state.system) {
        const timestamp = document.getElementById("system-timestamp");
        if (timestamp) timestamp.innerText = state.system.timestamp;
    }
}

function setupEventListeners() {
    const powerBtn = document.getElementById("btn-power");
    if (powerBtn) {
        powerBtn.addEventListener("click", async () => {
            const currentAction = powerBtn.innerText.includes("ENCENDER") ? "on" : "off";
            powerBtn.disabled = true;
            try {
                const res = await fetch(`${CONFIG.apiUrl}/nodes/muscle/power`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: currentAction })
                });
                const data = await res.json();
                console.log("[SYSTEM] Respuesta de hardware:", data);
            } catch (err) {
                console.error("[SYSTEM] Fallo en la llamada de energía:", err);
            } finally {
                powerBtn.disabled = false;
            }
        });
    }

    const radarBtn = document.getElementById("btn-radar-search");
    if (radarBtn) {
        radarBtn.addEventListener("click", async () => {
            const latInput = document.getElementById("input-lat");
            const lonInput = document.getElementById("input-lon");
            const lat = latInput ? parseFloat(latInput.value) || 40.4167 : 40.4167;
            const lon = lonInput ? parseFloat(lonInput.value) || -3.7037 : -3.7037;
            
            try {
                const res = await fetch(`${CONFIG.apiUrl}/radar/locations?lat=${lat}&lon=${lon}&radius=5000`);
                const payload = await res.json();
                if (payload.success && markersLayer) {
                    markersLayer.clearLayers();
                    payload.data.forEach(loc => {
                        L.marker([loc.latitude, loc.longitude])
                         .bindPopup(`<b>${loc.name}</b><br>Categoría: ${loc.category}`)
                         .addTo(markersLayer);
                    });
                }
            } catch (err) {
                console.error("[RADAR] Fallo en búsqueda espacial:", err);
            }
        });
    }
}

window.onload = initHUD;
