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
      // Ruta para verificar el estado y base de datos
      if (url.pathname === "/api/v1/state") {
        const { results } = await env.paisenobras_db.prepare(
          "SELECT sqlite_version() as version;"
        ).all();
        
        return new Response(JSON.stringify({ status: "online", db: results }), {
          headers: { "Content-Type": "application/json", ...corsHeaders },
        });
      }

      // Respuesta por defecto para evitar el error 404
      return new Response(`
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <title>País en Obras - Cortex</title>
          <style>body { font-family: sans-serif; padding: 40px; background: #f4f4f9; }</style>
        </head>
        <body>
          <h1>Entorno Unificado de Cortex</h1>
          <p>La API está activa en: <a href="/api/v1/state">/api/v1/state</a></p>
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
