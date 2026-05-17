export default {
  async fetch(request, env, ctx) {
    const TAILSCALE_IP = "http://100.64.0.1:5001"; // IP del Cerebro en Pop!_OS
    const url = new URL(request.url);
    const targetUrl = TAILSCALE_IP + url.pathname + url.search;
    
    const newRequest = new Request(targetUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: "manual"
    });
    
    try {
      return await fetch(newRequest);
    } catch (e) {
      return new Response("Cortex Edge: Error de enlace con el Cerebro local via Tailscale.", { status: 502 });
    }
  }
};
