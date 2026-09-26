# Formata Energia: filme de lançamento

Um vídeo de lançamento de 48 s em motion graphics (1920×1080, 60 fps) para a **Formata Energia**
(no-breaks, representante Engetron), no estilo dos vídeos de lançamento de SaaS que circulam no X/Twitter.

**Vídeo final:** [`formata-launch.mp4`](formata-launch.mp4)

## Roteiro (120 BPM, cortes no tempo da música)

| Tempo | Cena |
|---|---|
| 0–4 s | Abertura: a energia cai, a onda da rede vira uma linha reta e o alerta de falha pisca |
| 4–8 s | Revelação da marca: o logo Formata é desenhado traço a traço |
| 8–13 s | "Energia que não para.": a linha de no-breaks em um palco com reflexo |
| 13–18 s | 01 Área médica: ultrassom, ressonância, tomógrafo |
| 18–23 s | 02 No-breaks: carrossel 3D de Volt a Double Way Trifásico (0,7 a 825 kVA) |
| 23–30 s | 03 Double Way: simulação de queda de energia, com transferência de 0 ms, WBRC/IoT e software |
| 30–35 s | 04 Assistência técnica 7×24 |
| 35–39 s | Órbita "missões críticas": baterias, estabilizadores e segmentos atendidos |
| 39–43 s | 27 anos, 825 kVA, 7×24, representante exclusivo Engetron |
| 43–48 s | CTA: "Fale com um especialista", site e telefone |

As fotos de produto, os banners e o logo Engetron foram baixados de formataenergia.com.br.
O fundo branco das fotos de produto foi removido. O logo Formata foi redesenhado em vetor a partir
do original, para ficar nítido em 1080p e poder ser animado.

## Como gerar de novo

Requisitos: Node 18+, Python 3 com `numpy scipy pillow`, e `ffmpeg` (ou `pip install imageio-ffmpeg`
e `FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")`).

```bash
npm install                      # Playwright (Chromium headless)
python3 music.py                 # trilha sintetizada → music.wav
npm run render                   # renderiza os quadros e grava formata-launch.mp4
node render.mjs --preview 5,20   # PNGs de quadros específicos em previews/
```

Abra `index.html` no navegador para ver a animação ao vivo, ou use `index.html?t=12.5` para congelar um quadro.

- `index.html`: toda a animação. Cada quadro é uma função pura do tempo `t`, então a renderização é determinística.
- `render.mjs`: tira uma captura por quadro no Chromium headless e envia ao ffmpeg, em paralelo.
- `music.py`: trilha 100% sintetizada (bateria, baixo, pad, arpejo, whooshes, sons de queda de energia e alarme), sincronizada com as cenas e livre de direitos autorais.
