export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });

    if (path === "/api/v1/state" && request.method === "GET") {
      try {
        const { results } = await env.paisenobras_db.prepare("SELECT key, value FROM world_state").all();
        const worldState = {};
        for (const row of results) worldState[row.key] = JSON.parse(row.value);
        return Response.json({ success: true, world_state: worldState }, { headers: cors });
      } catch (err) {
        return Response.json({ success: false, error: err.message }, { status: 500, headers: cors });
      }
    }

    if (path === "/api/update-state" && request.method === "POST") {
      try {
        const { type, key, value } = await request.json();
        if (type === "world_state" && key && value) {
          const stmt = env.paisenobras_db.prepare("INSERT OR REPLACE INTO world_state (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)");
          await stmt.bind(key, JSON.stringify(value)).run();
          return Response.json({ success: true, message: `Actualizado ${key}` }, { headers: cors });
        }
        return Response.json({ success: false, error: "Payload inválido" }, { status: 400, headers: cors });
      } catch (err) {
        return Response.json({ success: false, error: err.message }, { status: 500, headers: cors });
      }
    }
    return new Response("Not Found", { status: 404, headers: cors });
  }
};
