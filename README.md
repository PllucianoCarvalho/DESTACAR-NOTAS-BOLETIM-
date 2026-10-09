# Destacador de Boletins

Aplicativo em Python para processar PDFs de boletins escolares no Linux Mint/Ubuntu. O programa permite selecionar um PDF por uma janela gráfica, contorna em preto notas numéricas abaixo de 6,0, calcula total de faltas e aproveitamento e gera um relatório pedagógico separado.

> **Atenção:** o posicionamento e a leitura das colunas foram ajustados para um modelo específico de boletim. Sempre teste com uma cópia do PDF e confira os resultados antes de entregar documentos às famílias. Não publique boletins reais nem dados pessoais de estudantes neste repositório.

## Recursos

- Seleção do PDF por janela gráfica.
- Contorno preto nas notas numéricas abaixo de 6,0.
- Soma de faltas identificadas nas colunas trimestrais.
- Cálculo de aproveitamento a partir das notas numéricas lidas.
- Classificação de aproveitamento:
  - **Avançado:** acima de 95%.
  - **Adequado:** acima de 80% até 95%.
  - **Básico:** acima de 60% até 80%.
  - **Abaixo do básico:** 60% ou menos.
- Geração de um PDF processado e de um relatório pedagógico separado.
- Criação de nomes de saída novos para não sobrescrever o PDF original.

## Requisitos

- Linux Mint ou Ubuntu.
- Python 3 e `venv`.
- Tkinter para a janela de seleção de arquivos.
- Conexão com a internet durante a instalação para instalar o PyMuPDF.

## Instalação recomendada

Baixe os arquivos `destacador_boletins_v3_1.py` e `Instalar_Destacador_Boletins_v3_1.sh` para a mesma pasta, por exemplo **Downloads**.

Abra o Terminal e execute os comandos **nesta ordem**:

```bash
cd ~/Downloads
```

Confira se os arquivos estão presentes:

```bash
ls -l destacador_boletins_v3_1.py Instalar_Destacador_Boletins_v3_1.sh
```

Instale os componentes do sistema necessários:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
```

Dê permissão de execução ao instalador:

```bash
chmod +x Instalar_Destacador_Boletins_v3_1.sh
```

Execute o instalador:

```bash
./Instalar_Destacador_Boletins_v3_1.sh
```

O instalador cria uma instalação separada em:

```text
~/Aplicativos/DestacadorBoletins_v3_1
```

Também cria um atalho chamado **Destacador de boletins v3.1** no menu de aplicativos. A instalação usa um ambiente virtual próprio e não deve substituir as versões anteriores.

## Como usar

1. Abra o menu de aplicativos do Linux Mint.
2. Procure por **Destacador de boletins v3.1** e abra.
3. Na janela de seleção, escolha o PDF original do boletim.
4. Aguarde a mensagem de conclusão.
5. Confira os dois arquivos gerados na mesma pasta do PDF de origem:
   - `NOME_PROCESSADO_v3_1.pdf`: boletins com as notas destacadas e o resumo inserido.
   - `NOME_PROCESSADO_v3_1_relatorio_pedagogico.pdf`: relatório separado para acompanhamento pedagógico.

Se já existir um arquivo com o mesmo nome, o programa cria outro nome com um número para evitar sobrescrever a saída anterior. O PDF original não é alterado.

## Executar pelo Terminal

Depois de instalar:

```bash
~/Aplicativos/DestacadorBoletins_v3_1/venv/bin/python ~/Aplicativos/DestacadorBoletins_v3_1/destacador_boletins_v3_1.py
```

## Atualizar ou reinstalar

1. Baixe a nova versão do script e do instalador.
2. Coloque ambos na mesma pasta.
3. Execute novamente os comandos de instalação acima.

Faça backup dos PDFs e confira o resultado de teste após cada atualização. As versões anteriores devem ser mantidas em diretórios separados.

## Solução de problemas

### Erro: Tkinter não instalado

```bash
sudo apt update
sudo apt install python3-tk
```

### Erro: não encontrou o script Python

Confirme que os dois arquivos estão na mesma pasta e que os nomes estão corretos:

```bash
ls -l ~/Downloads/destacador_boletins_v3_1.py ~/Downloads/Instalar_Destacador_Boletins_v3_1.sh
```

### Erro ao criar o ambiente virtual

```bash
sudo apt install python3-venv
```

### O resumo aparece fora do lugar ou os cálculos não conferem

O script usa coordenadas e posições de colunas ajustadas ao modelo de boletim usado durante o desenvolvimento. Não utilize o PDF processado até conferir visualmente a posição de total de faltas, aproveitamento, classificação e os destaques. Informe o problema e, se necessário, adapte o código ao modelo de PDF.

## Arquivos do projeto

- `destacador_boletins_v3_1.py` — aplicativo principal.
- `Instalar_Destacador_Boletins_v3_1.sh` — instalador para Linux Mint/Ubuntu.
- `README.md` — documentação e comandos de instalação.

## Privacidade e uso responsável

Boletins contêm dados pessoais de crianças e adolescentes. Use somente em ambiente autorizado, mantenha os PDFs em local seguro e não envie documentos reais para repositórios públicos. Publique apenas código, documentação e exemplos fictícios ou anonimizados.

## Licença

A licença ainda não foi definida. Consulte o responsável pelo repositório antes de reutilizar ou redistribuir o projeto.
