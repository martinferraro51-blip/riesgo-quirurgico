from flask import Flask, render_template, request, jsonify
import requests as http_requests
import os

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')


@app.route('/')
def index():
    return render_template('riesgo_quirurgico.html')


@app.route('/api/rq-analyze', methods=['POST'])
def api_rq_analyze():
    """Proxy a la API de Anthropic."""
    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'API key no configurada. Setear ANTHROPIC_API_KEY.'}), 500

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Sin datos'}), 400

    try:
        resp = http_requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01',
            },
            json={
                'model': data.get('model', 'claude-sonnet-4-20250514'),
                'max_tokens': data.get('max_tokens', 2500),
                'system': data.get('system', ''),
                'messages': data.get('messages', []),
            },
            timeout=60,
        )
        return jsonify(resp.json()), resp.status_code
    except http_requests.exceptions.Timeout:
        return jsonify({'error': 'Timeout al conectar con Anthropic'}), 504
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


if __name__ == '__main__':
    if not ANTHROPIC_API_KEY:
        print("=" * 60)
        print("  ATENCION: ANTHROPIC_API_KEY no configurada!")
        print("  Ejecutar: set ANTHROPIC_API_KEY=sk-ant-tu-key")
        print("=" * 60)
    else:
        print(f"API Key configurada: {ANTHROPIC_API_KEY[:12]}...")

    print("\n  Riesgo Quirurgico CV corriendo en http://0.0.0.0:5001")
    print("  Acceder desde otra PC: http://TU_IP:5001\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
