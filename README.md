# PAÍS EN OBRAS · CORTEX ENGINE

**Gemelo digital hostil de España. Un sistema autónomo que convierte datos públicos (BOE, INE, REE, AEMET) en un videojuego de mundo abierto que se deforma en tiempo real con humor negro, estética documental y calidad cinematográfica. Es también una fábrica de dinero descentralizada que monetiza el caos de forma indirecta, anónima y automática.**

---

## 1. QUÉ ES ESTO

PAÍS EN OBRAS no es un simulador tradicional ni un noticiero pasivo. Es un **noticiero jugable** y un **gemelo digital hostil de España**.

Mientras España se mueve al ritmo del Boletín Oficial del Estado (BOE), del IPC (INE), de la demanda energética (REE) y de las alertas meteorológicas (AEMET), este sistema construye un mundo 3D deformable y genera activos económicos (vídeos 4K, donaciones XMR, datasets de crisis, diseños de tatuajes) sin intervención humana.

El videojuego está pensado para ser **jugado gratis por cualquier persona** desde cualquier dispositivo (móvil, tablet, PC) sin instalar nada. La **única pantalla** —el panel de control— es para el operador y también es el punto de entrada pública. Todo ocurre ahí: el juego, el chat con el enjambre IA, la generación de tatuajes, el scraping en vivo y la telemetría de los nodos.

---

## 2. EL VIDEOJUEGO (MECÁNICA CENTRAL)

### 2.1. Deformación del mundo según H‑INDEX
- **H‑INDEX < 1.5** → España próspera, calles limpias, tráfico fluido.
- **1.5 – 3.0** → Obras en las coordenadas exactas de las licitaciones (grúas, vallas).
- **3.0 – 5.0** → Pintadas, semáforos rotos, manifestaciones de NPCs, grafitis Agenda 2030.
- **5.0 – 7.5** → Saqueos, inflación virtual, apagones zonales (REE).
- **> 7.5** → Crisis total: inundaciones (AEMET), apagones masivos, toque de queda virtual.

---

## 3. ARQUITECTURA REAL (NODOS MESH)


| Nodo | Hardware / SO | Función |
| :--- | :--- | :--- |
| **CEREBRO** | Acer Spin 3 / Pop!_OS | Scrapers, FastAPI (5005), Enjambre IA, Orquestador. |
| **MÚSCULO** | Win11 / RTX 3060 12GB | Unreal Engine 5.4, Cesium, Pixel Streaming, WebUI Forge. |
| **MANDO** | Unified Web Browser | Pantalla única de control absoluto y juego público. |

---

## 4. ESTRUCTURA DE ARCHIVOS (FHS CANÓNICA)

```text
cortex/
├── bin/          # Scripts de arranque y automatización
├── core/         # Oráculo (generación de state.json)
├── data/         # Contrato maestro, SQLite y galería de activos
├── srv/          # Servidor FastAPI (API y lógica de juego)
├── web/          # Pantalla única (Three.js Engine)
└── var/log/      # Registros operativos
```

---

## 5. INTEGRACIÓN NODO MÚSCULO (RTX 3060)

### Telemetría (muscle.py)
Protocolo de enlace para inyectar potencia de renderizado en la interfaz de mando:
```python
# Endpoint de destino: http://<IP_CEREBRO>:5005/api/muscle/update
```

---

## 6. MONETIZACIÓN INDIRECTA (YIELD GENERATION)

- **Clips 4K:** Publicación automática de crisis en RRSS con QR de Monero.
- **Marketplace Assets:** Venta de diseños (Tattoos) generados por la RTX 3060 vinculados a eventos del BOE.
- **SaaS Alertas:** Feed filtrado por IA para detección temprana de licitaciones públicas.

---

## 7. COMANDOS DE OPERACIÓN

```bash
# Estado del servicio
sudo systemctl status cortex.service

# Logs en tiempo real
sudo journalctl -u cortex.service -f

# Inspección de datos de simulación
curl -s http://localhost:5005/api/game/state | jq
```

---
**Soberanía Tecnológica · Datos Públicos · Realidad Generada**
