export default {
  async fetch(request, env, ctx) {
    const TAILSCALE_IP = "http://100.64.0.1:5001"; // IP del Cerebro Acer Spin 3
    const url = new URL(request.url);
    const targetUrl = TAILSCALE_IP + url.pathname + url.search;
    
    // Clonar peticion con la redireccion del proxy local
    const newRequest = new Request(targetUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body
    });
    
    try {
      return await fetch(newRequest);
    } catch (e) {
      return new Response("Error de conexion con el Nodo Cerebro via Tailscale: " + e.message, { status: 502 });
    }
  }
};
