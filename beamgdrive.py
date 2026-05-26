import keyboard
import time
import pyautogui
import requests
import os
import threading
from flask import Flask, jsonify, render_template_string

# ==========================================
# CONFIGURACOES PRINCIPAIS
# ==========================================
WEBHOOK_URL = 'COLE_AQUI_SEU_WEBHOOK_DO_DISCORD' 

HOTKEY_INICIAR_PARAR = 'ctrl+shift+1'
HOTKEY_PRINT = 'ctrl+shift+2'
HOTKEY_ENVIAR = 'ctrl+shift+3'
HOTKEY_RESET = 'ctrl+shift+4'

# ==========================================
# ESTADO DA APLICACAO (CACHE E CONTROLE)
# ==========================================
tempo_inicio = None
tempo_congelado = None
caminho_print_cache = 'print_temp.png'
rodando = False
print_tirado = False
status_envio = "ocioso" # Estados: ocioso, enviando, enviado, erro

app = Flask(__name__)

# ==========================================
# FUNCOES DE LOGICA E CRONOMETRO
# ==========================================

def formatar_tempo(segundos):
    """Formata o tempo em MM:SS.ms"""
    m, s = divmod(segundos, 60)
    ms = (segundos - int(segundos)) * 100
    return f"{int(m):02d}:{int(s):02d}.{int(ms):02d}"

def get_tempo_ao_vivo():
    """Retorna o tempo em tempo real para o dashboard."""
    if rodando:
        return formatar_tempo(time.time() - tempo_inicio)
    elif tempo_congelado:
        return tempo_congelado
    else:
        return "00:00.00"

def toggle_tempo():
    """Inicia ou para o cronometro."""
    global tempo_inicio, tempo_congelado, rodando
    if not rodando:
        tempo_inicio = time.time()
        rodando = True
        print("Cronometro INICIADO.")
    else:
        tempo_total = time.time() - tempo_inicio
        tempo_congelado = formatar_tempo(tempo_total)
        rodando = False
        print(f"Tempo PARADO: {tempo_congelado}")

def tirar_print():
    """Captura a tela e salva em cache, sinalizando a UI."""
    global print_tirado
    print_tela = pyautogui.screenshot()
    print_tela.save(caminho_print_cache)
    print_tirado = True
    print("Print capturado e salvo no cache.")

def processar_envio_discord():
    """Funcao assincrona para enviar dados ao Discord sem travar a UI."""
    global status_envio
    status_envio = "enviando"
    
    try:
        payload = {"content": f"🏁 **Nova Volta Registrada!**\n⏱️ **Tempo:** `{tempo_congelado}`"}
        with open(caminho_print_cache, 'rb') as f:
            arquivos = {'file': (caminho_print_cache, f, 'image/png')}
            resposta = requests.post(WEBHOOK_URL, data=payload, files=arquivos)
            
        if resposta.status_code in [200, 204]:
            print(f"Sucesso ao enviar. Tempo: {tempo_congelado}")
            status_envio = "enviado"
            # Mantem a mensagem de sucesso por 3 segundos na UI
            time.sleep(3)
            resetar_geral(silencioso=True)
        else:
            print(f"Falha na API do Discord: {resposta.status_code}")
            status_envio = "erro"
            time.sleep(3)
            status_envio = "ocioso"
    except Exception as e:
        print(f"Erro na rotina de envio: {e}")
        status_envio = "erro"
        time.sleep(3)
        status_envio = "ocioso"

def enviar_dados():
    """Inicia a thread de envio se os requisitos forem atendidos."""
    global tempo_congelado, print_tirado
    if not tempo_congelado or not print_tirado:
        print("Aviso: Tempo ou print ausentes no cache. Envio cancelado.")
        return
    if status_envio == "enviando":
        return # Evita multiplos envios simultaneos
    
    print("Iniciando envio para o Discord...")
    threading.Thread(target=processar_envio_discord).start()

def resetar_geral(silencioso=False):
    """Zera o cronometro, limpa o cache e reseta a UI."""
    global tempo_inicio, tempo_congelado, rodando, print_tirado, status_envio
    tempo_inicio = None
    tempo_congelado = None
    rodando = False
    print_tirado = False
    status_envio = "ocioso"
    
    if os.path.exists(caminho_print_cache):
        try:
            os.remove(caminho_print_cache)
        except OSError:
            pass
            
    if not silencioso:
        print("Sistema resetado com sucesso.")

# ==========================================
# SERVIDOR WEB (INTERFACE TELA DIVIDIDA)
# ==========================================

@app.route('/')
def painel():
    """Renderiza a interface do usuario (Tablet)."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard BeamNG</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                background-color: #121212; color: white; font-family: 'Segoe UI', sans-serif; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; 
                height: 100vh; margin: 0; padding: 10px; box-sizing: border-box; text-align: center;
            }
            #status-box { 
                font-size: clamp(1.2rem, 4vw, 2.5rem); font-weight: bold; margin-bottom: 15px; 
                padding: 10px 20px; border-radius: 10px; text-transform: uppercase; 
                transition: background-color 0.3s; width: 100%; max-width: 350px; box-sizing: border-box;
            }
            #tempo-box { 
                font-size: clamp(3rem, 15vw, 8rem); font-family: monospace; 
                font-weight: bold; letter-spacing: 1px; line-height: 1; margin-bottom: 10px;
            }
            .notificacao {
                font-size: clamp(1rem, 3vw, 1.5rem); font-weight: bold; margin-top: 10px;
                padding: 8px 15px; border-radius: 8px; display: none; width: 100%; max-width: 300px;
            }
            #notificacao-print { background-color: #17a2b8; color: white; }
            #notificacao-envio { background-color: #444; color: white; }
            
            .idle { background-color: #444; }
            .running { background-color: #28a745; }
            .stopped { background-color: #dc3545; }
        </style>
    </head>
    <body>
        <div id="status-box" class="idle">AGUARDANDO...</div>
        <div id="tempo-box">00:00.00</div>
        
        <div id="notificacao-print">📸 PRINT SALVO!</div>
        <div id="notificacao-envio"></div>
        
        <script>
            function atualizarPainel() {
                fetch('/status')
                    .then(response => response.json())
                    .then(data => {
                        // Atualiza Cronometro e Status Base
                        document.getElementById('tempo-box').innerText = data.tempo;
                        const statusBox = document.getElementById('status-box');
                        
                        if (data.rodando) {
                            statusBox.innerText = "🟢 RODANDO";
                            statusBox.className = "running";
                        } else if (data.tempo !== "00:00.00") {
                            statusBox.innerText = "🛑 PARADO";
                            statusBox.className = "stopped";
                        } else {
                            statusBox.innerText = "🟡 ESPERANDO";
                            statusBox.className = "idle";
                        }

                        // Atualiza Status do Print
                        const printBox = document.getElementById('notificacao-print');
                        printBox.style.display = data.print_tirado ? "block" : "none";

                        // Atualiza Status de Envio ao Discord
                        const envioBox = document.getElementById('notificacao-envio');
                        if (data.status_envio === "enviando") {
                            envioBox.innerText = "⏳ ENVIANDO...";
                            envioBox.style.backgroundColor = "#ffc107";
                            envioBox.style.color = "black";
                            envioBox.style.display = "block";
                        } else if (data.status_envio === "enviado") {
                            envioBox.innerText = "✅ ENVIADO!";
                            envioBox.style.backgroundColor = "#28a745";
                            envioBox.style.color = "white";
                            envioBox.style.display = "block";
                        } else if (data.status_envio === "erro") {
                            envioBox.innerText = "❌ ERRO AO ENVIAR";
                            envioBox.style.backgroundColor = "#dc3545";
                            envioBox.style.color = "white";
                            envioBox.style.display = "block";
                        } else {
                            envioBox.style.display = "none";
                        }
                    });
            }
            // Atualiza o DOM a cada 100ms
            setInterval(atualizarPainel, 100);
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/status')
def status():
    """Endpoint consumido pelo frontend para atualizar a UI."""
    return jsonify({
        "rodando": rodando,
        "tempo": get_tempo_ao_vivo(),
        "print_tirado": print_tirado,
        "status_envio": status_envio
    })

# ==========================================
# INICIALIZACAO
# ==========================================
if __name__ == '__main__':
    print("Iniciando escuta do teclado (Stream Deck)...")
    keyboard.add_hotkey(HOTKEY_INICIAR_PARAR, toggle_tempo)
    keyboard.add_hotkey(HOTKEY_PRINT, tirar_print)
    keyboard.add_hotkey(HOTKEY_ENVIAR, enviar_dados)
    keyboard.add_hotkey(HOTKEY_RESET, resetar_geral)
    
    print("Servidor Web iniciado. Acesse o IP da sua maquina na porta 5000.")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
