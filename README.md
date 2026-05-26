# BeamNG.drive-Discord-Timer

Aplicação local desenvolvida em **Python + Flask** para registrar tempos de voltas urbanas no **BeamNG.drive**, capturar screenshots automaticamente em segundo plano e enviar os resultados diretamente para um canal privado do Discord via Webhook.

Projetado para setups com:
- 🎮 Elgato Stream Deck
- 📱 Tablet secundário
- 🏁 Drift / Time Attack / Roleplay

---

# ✨ Recursos

## ⏱️ Cronômetro em Segundo Plano

Controle total via atalhos globais de teclado — não é necessário focar a janela da aplicação.

Ideal para:
- Stream Deck
- Macros
- Teclados numéricos
- Botões USB dedicados

---

## 📸 Sistema de Cache Inteligente

O tempo da volta e a captura da imagem funcionam separadamente.

Isso permite:
- finalizar a volta primeiro;
- escolher o melhor momento para tirar o print;
- enviar tudo apenas quando quiser.

Perfeito para:
- drift shots;
- replay;
- ângulos cinematográficos;
- HUD limpo.

---

## 🌐 Dashboard Web Responsivo

Interface local otimizada para:
- tablets;
- segunda tela;
- divisão de tela;
- uso rápido durante gameplay.

Acesse pelo navegador sem instalar nada no dispositivo.

---

## 🔔 Feedback em Tempo Real

Notificações visuais informam:
- tempo registrado;
- captura do print;
- status do envio;
- erros de conexão/webhook.

---

# 🛠️ Tecnologias Utilizadas

- Python
- Flask
- Keyboard
- PyAutoGUI
- Pillow
- Requests

---

# 📦 Instalação

## 1️⃣ Instale o Python

Baixe em:

https://www.python.org/downloads/

Durante a instalação marque:

```bash
✅ Add Python to PATH
```

---

## 2️⃣ Instale as Dependências

Abra o CMD ou PowerShell e execute:

```bash
pip install flask keyboard pyautogui requests Pillow pyscreeze
```

---

# ⚙️ Configuração

## 1️⃣ Criando o Webhook do Discord

No Discord:

1. Abra o canal desejado
2. Vá em:
   `Configurações do Canal → Integrações → Webhooks`
3. Clique em:
   `Novo Webhook`
4. Copie a URL gerada

---

## 2️⃣ Configure no Projeto

No arquivo:

```python
beamgdrive.py
```

Substitua:

```python
WEBHOOK_URL = "COLE_SEU_WEBHOOK_AQUI"
```

---

# ▶️ Como Executar

No terminal:

```bash
python beamgdrive.py
```

A aplicação iniciará localmente.

---

# 📱 Acessando pelo Tablet

Descubra o IP local do computador:

```bash
ipconfig
```

Procure por algo como:

```bash
IPv4: 192.168.0.15
```

Depois, no navegador do tablet:

```bash
http://192.168.0.15:5000
```

---

# 🎮 Controles Padrão

| Função | Atalho |
|---|---|
| ▶️ Iniciar / Parar Tempo | `Ctrl + Shift + 1` |
| 📸 Tirar Print | `Ctrl + Shift + 2` |
| 📤 Enviar para Discord | `Ctrl + Shift + 3` |
| 🔄 Resetar Tudo | `Ctrl + Shift + 4` |

Os atalhos podem ser alterados diretamente no código-fonte.

---

# 🖥️ Fluxo Recomendado

## Exemplo de uso:

1. Inicie a corrida
2. Pare o cronômetro ao finalizar
3. Posicione a câmera do jogo
4. Tire o print
5. Envie para o Discord

---

# 📂 Estrutura Esperada

```bash
project/
│
├── beamgdrive.py
├── screenshots/
├── static/
└── templates/
```

---

# ⚠️ Observações

- Execute como administrador caso os atalhos globais não funcionem.
- O jogo pode precisar estar em:
  - modo janela;
  - janela sem borda.
- O tablet e o PC precisam estar na mesma rede local.

---

# 🚀 Ideias Futuras

- Ranking de voltas
- Histórico de tempos
- Integração com OBS
- Overlay em tempo real
- Upload automático de replay
- Estatísticas por carro/mapa
- Sistema multiplayer/local leaderboard

---

# 📸 Objetivo do Projeto

Criar uma experiência rápida e fluida para registrar sessões urbanas, drift runs e time attacks no BeamNG.drive sem precisar sair do jogo constantemente.

Feito para setups imersivos e uso casual entre amigos/comunidades.
