<div align="center">

# 🎯 TRIGGER - Detector de Cor Automático

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue? style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/github/repo-size/rafaelxo/TRIGGER?style=for-the-badge&color=orange" alt="Repo Size">
  <img src="https://img.shields.io/github/stars/rafaelxo/TRIGGER?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/github/last-commit/rafaelxo/TRIGGER?style=for-the-badge&color=red" alt="Last Commit">
</p>

**Bot de detecção automática de cor amarela com clique automático**

Desenvolvido em **Python** utilizando manipulação de tela em baixo nível com **ctypes**

</div>

---

## 📚 Sobre

**TRIGGER** é um bot de detecção de cor que monitora continuamente uma área ao redor do cursor do mouse e realiza cliques automáticos quando detecta pixels amarelos. O projeto utiliza programação em baixo nível com a API do Windows através de **ctypes**, garantindo alta performance e baixa latência.

### 🎯 Casos de Uso
- ⚡ Automação de tarefas baseadas em detecção visual
- 🎮 Auxílio em jogos que requerem reação rápida a estímulos visuais
- 🤖 Estudos de visão computacional e automação
- 🔬 Testes de performance de detecção em tempo real

---

## ✨ Funcionalidades

### 🔥 Principais Recursos

- ✅ **Detecção em Tempo Real**: Captura e análise de tela em até 100 FPS
- ✅ **Alta Performance**: Uso de ctypes e API do Windows para máxima velocidade
- ✅ **Configuração Flexível**: Parâmetros ajustáveis via linha de comando
- ✅ **Modo Teste**: Detecta sem clicar para calibração
- ✅ **Ativação por Tecla**: Liga/desliga com hotkey customizável
- ✅ **Área Customizável**: Define tamanho da região de detecção
- ✅ **Sensibilidade Ajustável**:  Controle fino da detecção de cor
- ✅ **Modo Verbose**: Log detalhado de cada detecção
- ✅ **Autoinstalação**: Instala dependências automaticamente

---

## 🛠️ Tecnologias e Bibliotecas

### 📦 Dependências

| Biblioteca | Versão | Uso |
|: -----------|:-------|:----|
| 🐍 **Python** | 3.8+ | Linguagem base |
| ⌨️ **keyboard** | Latest | Captura de teclas e hotkeys |
| 🖱️ **pyautogui** | Latest | Simulação de cliques |
| 🔧 **ctypes** | Built-in | Interface com API do Windows |

### 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│         Windows API (ctypes)            │
├─────────────────────────────────────────┤
│  • GetDC / ReleaseDC                   │
│  • CreateCompatibleDC / DeleteDC       │
│  • BitBlt (captura de tela)            │
│  • GetCursorPos (posição do mouse)     │
│  • SendInput (cliques)                 │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│      Processamento de Imagem            │
├─────────────────────────────────────────┤
│  • Captura de ROI (Region of Interest) │
│  • Análise pixel por pixel             │
│  • Detecção de cor amarela (RGB)       │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│         Sistema de Ação                 │
├─────────────────────────────────────────┤
│  • Verificação de estado (ativo/off)   │
│  • Execução de cliques triplos         │
│  • Controle de intervalo               │
└─────────────────────────────────────────┘
```

---

### ⚙️ Parâmetros Disponíveis

| Parâmetro | Padrão | Descrição |
|: ----------|:-------|:----------|
| `--area` | 100 | Tamanho da área de detecção (pixels) |
| `--sensibilidade` | 200 | Sensibilidade:  150=alta, 200=média, 230=baixa |
| `--intervalo` | 0.01 | Intervalo mínimo entre cliques (segundos) |
| `--fps` | 100 | Taxa de verificação por segundo |
| `--tecla` | caps lock | Tecla para ativar/desativar |
| `--teste` | - | Modo teste (só detecta, não clica) |
| `--verbose` | - | Mostra log de cada detecção |

---

## 🔬 Como Funciona

### 1️⃣ **Captura de Tela**
```python
def capture_roi_to_buffer(x, y, roi):
    # Captura área ao redor do cursor usando BitBlt
    # Retorna buffer de pixels em formato BGRA (32-bit)
```

### 2️⃣ **Detecção de Cor**
```python
def contains_yellow(buf, width, height, r_min, g_min, b_max):
    # Analisa cada pixel no formato BGR
    # Detecta amarelo:  R >= r_min AND G >= g_min AND B <= b_max
    if r >= r_min and g >= g_min and b <= b_max: 
        return True
```

### 3️⃣ **Sistema de Clique**
```python
# Quando detecta amarelo e está ativo: 
for i in range(3):
    click_left()      # Executa clique
    time.sleep(0.05)  # Pequeno delay entre cliques
```

### 🎨 Detecção de Cor Amarela

A detecção utiliza o espaço de cor RGB: 
- **R (Red)**: ≥ sensibilidade (padrão: 200)
- **G (Green)**: ≥ sensibilidade (padrão: 200)
- **B (Blue)**: ≤ limite baixo (padrão: 5)

Isso garante que apenas tons amarelos/dourados sejam detectados.

---

## 📊 Performance

### ⚡ Benchmarks

| Configuração | FPS Teórico | FPS Real | Latência |
|:-------------|: ------------|:---------|:---------|
| Padrão (100 FPS) | 100 | ~95-100 | ~10ms |
| Alta (120 FPS) | 120 | ~110-120 | ~8ms |
| Máxima (200 FPS) | 200 | ~150-180 | ~5-7ms |

### 💡 Dicas de Otimização

- 🔹 **Reduzir área**: Menor ROI = mais rápido
- 🔹 **Ajustar FPS**: Balance entre performance e uso de CPU
- 🔹 **Modo teste**: Calibrar sensibilidade antes de usar
- 🔹 **Privilégios Admin**: Necessário para máxima performance

---

## 🔐 Segurança e Avisos

### ⚠️ Avisos Importantes

- 🛑 **Uso Responsável**: Este projeto é apenas para fins educacionais
- 🛑 **Jogos Online**: O uso em jogos online pode violar termos de serviço
- 🛑 **Privilégios Admin**: O script requer execução como administrador
- 🛑 **Failsafe**: PyAutoGUI failsafe está desabilitado para performance

### 📜 Disclaimer

Este projeto foi desenvolvido exclusivamente para fins de **aprendizado** e **estudo de automação**. O autor não se responsabiliza pelo uso inadequado ou por violações de termos de serviço de terceiros.

---

## 🎓 Conceitos Abordados

### Programação Baixo Nível
- ✅ Uso de ctypes para chamadas diretas à API do Windows
- ✅ Manipulação de estruturas C em Python
- ✅ Gerenciamento manual de contextos de dispositivo (DC)
- ✅ Buffers de memória e manipulação de pixels

### Visão Computacional
- ✅ Captura de região de interesse (ROI)
- ✅ Análise de pixels em tempo real
- ✅ Detecção de cor no espaço RGB
- ✅ Otimização de loops de processamento

### Automação
- ✅ Simulação de entrada do usuário
- ✅ Hotkeys globais
- ✅ Threading e sincronização
- ✅ Controle de taxa de execução (FPS)

---

## 👤 Autor

**Rafael**  
[![GitHub](https://img.shields.io/badge/GitHub-rafaelxo-181717?style=for-the-badge&logo=github)](https://github.com/rafaelxo)

---

## 📄 Licença

Este projeto é destinado exclusivamente a **fins educacionais** e de estudo.   
**Uso por sua conta e risco.  O autor não se responsabiliza por qualquer uso inadequado.**

---

## ⭐ Agradecimentos

Se este projeto foi útil para seus estudos, considere dar uma ⭐ no repositório!

---

<div align="center">

**Desenvolvido para fins educacionais - Use com responsabilidade ⚠️**

</div>
