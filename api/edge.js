export const config = {
    runtime: 'edge',
    regions: ['iad1'],
};

export default async function handler(request) {
    const streamlitResponse = await fetch('http://localhost:8501', {
        method: request.method,
        headers: request.headers,
        body: request.body,
    });

    return new Response(streamlitResponse.body, {
        status: streamlitResponse.status,
        headers: streamlitResponse.headers,
    });
} 