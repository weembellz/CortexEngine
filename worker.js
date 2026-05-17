export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json"
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    try {
      if (url.pathname === "/api/v1/state" && request.method === "GET") {
        const state = await env.STATE_KV.get("master_state");
        if (!state) return new Response(JSON.stringify({ error: "No state" }), { status: 404, headers: cors });
        return new Response(state, { status: 200, headers: cors });
      }
      if (url.pathname === "/api/v1/state" && request.method === "POST") {
        const body = await request.text();
        JSON.parse(body); // validar
        await env.STATE_KV.put("master_state", body);
        return new Response(JSON.stringify({ success: true }), { status: 200, headers: cors });
      }
      if (url.pathname === "/api/v1/simulation/vote" && request.method === "POST") {
        const { vote_index } = await request.json();
        let raw = await env.STATE_KV.get("master_state");
        if (!raw) return new Response(JSON.stringify({ error: "No state" }), { status: 404 });
        let state = JSON.parse(raw);
        let debt = state.simulation.debt_to_gdp_ratio;
        if (vote_index === 0) debt = Math.max(0, debt - 10);
        else debt = Math.max(0, debt - 8);
        state.simulation.debt_to_gdp_ratio = debt;
        await env.STATE_KV.put("master_state", JSON.stringify(state));
        return new Response(JSON.stringify({ success: true }), { status: 200, headers: cors });
      }
      return new Response(JSON.stringify({ error: "Not found" }), { status: 404, headers: cors });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: cors });
    }
  }
};
