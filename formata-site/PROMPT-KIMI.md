Faça as correções abaixo no site da Formata Energia. Não mude o posicionamento, a estrutura geral nem os textos que não forem citados aqui. Ao final, liste o que foi alterado.

## 1. Críticos

1.1. **Subpáginas com 404 ao acessar direto.** Hoje /area-medica, /produtos, /solucoes/* etc. só abrem navegando a partir da home; ao atualizar a página ou abrir o link direto, o servidor devolve 404. Configure o fallback de SPA (toda rota → index.html) e, de preferência, pré-renderize cada rota do sitemap (SSG) para que título, descrição e conteúdo venham no HTML inicial de cada página.

1.2. **Imagem de compartilhamento e favicon.** Substitua /og-image.jpg pela nova imagem 1200×630 que vou enviar (fundo escuro, vermelho da marca) e /favicon.svg pelo novo favicon vermelho que vou enviar. Remova qualquer uso do verde (#34d399) que tenha sobrado do modelo.

1.3. **Logos de terceiros.** Deixe os logos de fabricantes (Siemens Healthineers, GE HealthCare, Philips, Samsung) e de clientes controláveis por uma lista em um único arquivo de configuração, para eu remover facilmente os que não tiverem autorização. Não adicione nenhum logo novo.

1.4. **Remova o selo/botão "Kimi"** e o aviso de conteúdo de IA do site publicado.

## 2. Conteúdo e números

2.1. Faixa de potência: troque "De 600VA a 6,6MVA" por "De 700 VA a 6,6 MVA" em todo o site. No card de trifásicos, escreva "10 kVA a 825 kVA por unidade · até 6,6 MVA em paralelo".

2.2. Troque "Revenda exclusiva Engetron" por "Representante Engetron" (vou confirmar o termo contratual depois; deixe fácil de trocar).

2.3. Troque "Resposta técnica com brevidade" por "Resposta técnica rápida" (hero e seção de contato).

2.4. Padronize a grafia: sempre "nobreak/nobreaks" (o diagrama usa "no-breaks") e sempre espaço entre número e unidade ("600 VA", "6,6 MVA", "10 kVA").

2.5. Imagens: nos textos alternativos, não diga "protegida pela Formata" em fotos que não são instalações reais da Formata; use descrições neutras ("Sala de ressonância magnética", "Corredor de data center"). No card "Sala de servidores para IA", use uma imagem de sala de servidores, não de um nobreak de rack. No card "Nobreak para servidores de IA", use uma imagem com fundo escuro como os outros cards (ou recorte o fundo branco).

## 3. Clientes e prova social

3.1. Separe a seção em duas faixas com rótulo: "Homologada pelos fabricantes" (fabricantes) e "Clientes que atendemos" (clientes).

3.2. Na faixa de clientes, aumente os logos para no mínimo 120 px de largura e 40 px de altura, sem tons de cinza/opacidade que dificultem a leitura, e coloque o nome da empresa no alt de cada logo (as cópias duplicadas do carrossel podem ficar com alt="" e aria-hidden="true").

## 4. Contato e conversão

4.1. Transforme os telefones em links clicáveis: tel:+551120983571 e o WhatsApp https://wa.me/5511996088144.

4.2. No mobile, adicione um botão flutuante de WhatsApp no canto inferior direito, com a mesma mensagem pré-preenchida do botão "Pedir orçamento".

4.3. No formulário, além de abrir o WhatsApp, envie também os dados por e-mail para comercial@formataenergia.com.br (por exemplo via Formspree, Web3Forms ou endpoint próprio), para o contato não se perder se a pessoa não enviar no WhatsApp. Mostre uma mensagem de confirmação.

4.4. Na seção "Quanto custa uma hora parada na sua operação?", adicione um botão "Calcular o custo da minha parada" apontando para /calculadora.

## 5. Rodapé e institucional

5.1. Adicione ao rodapé: razão social e CNPJ (deixe campos para eu preencher: [RAZÃO SOCIAL], [CNPJ]), endereço ([ENDEREÇO]), horário (segunda a sexta, 8h às 18h), links para Instagram e LinkedIn ([URLs]) e link "Política de privacidade".

5.2. Crie a página /politica-de-privacidade (LGPD): quais dados o formulário coleta, finalidade (responder à solicitação), compartilhamento com o WhatsApp, prazo de guarda, direitos do titular e contato comercial@formataenergia.com.br. Ligue essa página no aviso abaixo do formulário.

5.3. Crie a página /quem-somos (32 anos, desde 1994, atuação em área médica, data centers e indústria, representante Engetron, atendimento técnico em todo o Brasil) e inclua "Quem somos" no menu.

5.4. Use o mesmo logo em todos os lugares (cabeçalho, rodapé, favicon, imagem de compartilhamento).

## 6. Acessibilidade e visual

6.1. Contraste: os botões vermelhos com texto branco estão com 3,76:1. Troque o vermelho de fundo dos botões para #DC2626 (hover #B91C1C), mantendo #EF4444 só em textos grandes e detalhes. Na seção branca "Da entrada da rede à carga crítica", escureça as legendas cinza e o texto de apoio para no mínimo #4B5563.

6.2. Grades: os 5 cards da área médica e os 3 cards de Data Centers & IA deixam um card sozinho. Use 3 colunas no desktop (ou ajuste para não sobrar card órfão).

6.3. Nos cards de "Soluções de energia crítica", deixe no máximo 1 botão principal + 1 link de texto por card.

6.4. No cabeçalho do hero, o texto pequeno "ESPECIALISTAS EM CONTINUIDADE DE ENERGIA PARA EMPRESAS" quebra em duas linhas; encurte para "ESPECIALISTAS EM ENERGIA CRÍTICA".

## 7. Desempenho

7.1. Converta as fotos (hero, cards médicos e de data center) para WebP no tamanho em que aparecem (no máximo 2× a largura exibida) e use srcset. Exemplos: ultrassom.jpg tem 323 KB e aparece com 258 px; datacenter.jpg tem 282 KB.

7.2. Reduza os logos PNG de 800 px para o tamanho exibido (no máximo 2×) e converta para WebP ou SVG.

7.3. Garanta loading="lazy" em tudo abaixo da dobra e width/height em todas as imagens para evitar pulos de layout.
