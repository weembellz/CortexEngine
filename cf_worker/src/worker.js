export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // ─── RUTA API: /api/v1/state (Consulta segura compatible con D1) ───
      if (url.pathname === "/api/v1/state") {
        let state = {
          success: true,
          world_state: {
            world: { chaos: 0.55, h_index: 7.42 },
            economy: { deuda_publica_pct: 113.2, regimen_actual: "DEMOCRACIA_DEBIL", brent_usd: 84.52, oro_fed_tons: 8133.5 },
            life_os: { gastos_reales: {}, alquiler_total_real: 368.45, suministros_base: 15, operador_local: {}, empadronamiento: "PENDIENTE_PRESENCIAL", coordenadas: "41.648 N, 1.141 E" },
            terrario_sefa: { status: "MONITOREANDO", activos: { monero_base: 0.15, capital_extraido_eur: 0 } },
            news_feed: { titular: "WORKER REINICIADO", impacto: "SISTEMA OPERATIVO EN EDGE CANÓNICO" }
          }
        };

        // Si D1 está configurado, intentamos mapear datos dinámicos de forma segura
        if (env.paisenobras_db) {
          try {
            const { results } = await env.paisenobras_db.prepare(
              "SELECT sqlite_version() as v;" 
            ).all().catch(() => ({ results: [] })); // Evita que un fallo de permisos tire el worker
            if (results && results.length) {
              state.database_status = "connected";
            }
          } catch(e) {
            state.database_status = "restricted_access";
          }
        }

        return new Response(JSON.stringify(state), {
          headers: { "Content-Type": "application/json", ...corsHeaders },
        });
      }

      // ─── RUTA FRONTEND PRINCIPAL: Servir el Dashboard de control ───
      return new Response(`
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>País en Obras - Cortex Edge</title>
            <style>
                body { background: #0a0a0c; color: #00ff66; font-family: monospace; padding: 30px; }
                .container { max-width: 900px; margin: 0 auto; border: 1px solid #00ff66; padding: 20px; box-shadow: 0 0 15px rgba(0,255,102,0.2); }
                h1 { border-bottom: 1px solid #00ff66; padding-bottom: 10px; color: #fff; }
                a { color: #00ffff; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .panel { background: #11141a; padding: 15px; border-radius: 4px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>MÁQUINA DE GUERRA FINANCIERA - CORTEX</h1>
                <p>NÚCLEO CANÓNICO DE OPERACIONES DESPLEGADO EN EL EDGE DE CLOUDFLARE</p>
                <div class="panel">
                    <h3>Puntos de acceso disponibles:</h3>
                    <ul>
                        <li>API de Estado Crítico: <a href="/api/v1/state">/api/v1/state</a></li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
      `, {
        headers: { "Content-Type": "text/html; charset=utf-8", ...corsHeaders },
      });

    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { "Content-Type": "application/json", ...corsHeaders },
      });
    }
  }
};
