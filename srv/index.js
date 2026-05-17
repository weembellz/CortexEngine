export default {
  async fetch(request, env, ctx) {
    const tunnelUrl = "https://exclusively-sep-requirements-cover.trycloudflare.com";
    const url = new URL(request.url);
    const target = new URL(url.pathname + url.search, tunnelUrl);
    return fetch(new Request(target, {
      method: request.method,
      headers: request.headers,
      body: request.body
    }));
  }
}