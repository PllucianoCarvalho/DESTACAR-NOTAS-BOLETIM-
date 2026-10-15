# Destacador de Boletins

**Versão atual: 3.2.1**

Aplicativo em Python para Linux Mint/Ubuntu que processa PDFs de boletins escolares, contorna em preto notas numéricas abaixo de 6,0, calcula totais de faltas e aproveitamento, desenha estrelas de proficiência e gera um relatório pedagógico separado.

> **Atenção:** a leitura das notas e faltas usa coordenadas ajustadas a um modelo específico de boletim. Antes de usar os arquivos gerados oficialmente, teste com uma cópia anonimizada e confira visualmente todos os resultados, inclusive quando há dois boletins na mesma folha. Não publique PDFs reais nem dados pessoais de estudantes neste repositório.

## Recursos da versão 3.2.1

- Seleção do PDF pela janela de arquivos.
- Contorno preto em células numéricas da coluna Nota com valor abaixo de 6,0.
- Soma das faltas lidas nas colunas trimestrais.
- Cálculo de aproveitamento a partir das notas numéricas reconhecidas.
- Classificação do aproveitamento:
  - **Avançado:** acima de 95%.
  - **Adequado:** acima de 80% até 95%.
  - **Básico:** acima de 60% até 80%.
  - **Abaixo do básico:** 60% ou menos.
- Desenho de estrelas conforme a faixa de aproveitamento.
- Resumo de faltas e aproveitamento no boletim.
- PDF processado e relatório pedagógico separados.
- Nomes de saída novos para não substituir o PDF original.
- Instalador próprio que mantém a versão 3.1 em diretório separado.

## Requisitos

- Linux Mint ou Ubuntu.
- Python 3, `python3-venv` e Tkinter.
- Internet durante a instalação para instalar o PyMuPDF.

Instale os componentes do sistema antes de executar o instalador:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
```

## Instalação da versão atual

Baixe **estes dois arquivos da versão 3.2.1** para a mesma pasta, por exemplo `~/Downloads`:

- [destacador_boletins_v3_2_1.py](https://github.com/PllucianoCarvalho/DESTACAR-NOTAS-BOLETIM-/blob/main/destacador_boletins_v3_2_1.py)
- [Instalar_Destacador_Boletins_v3_2_1.sh](https://github.com/PllucianoCarvalho/DESTACAR-NOTAS-BOLETIM-/blob/main/Instalar_Destacador_Boletins_v3_2_1.sh)

Abra o Terminal e execute, na ordem:

```bash
cd ~/Downloads
ls -l destacador_boletins_v3_2_1.py Instalar_Destacador_Boletins_v3_2_1.sh
chmod +x Instalar_Destacador_Boletins_v3_2_1.sh
./Instalar_Destacador_Boletins_v3_2_1.sh
```

O instalador procura o script Python na **mesma pasta em que ele próprio está**, cria um ambiente virtual separado e instala o PyMuPDF na versão definida pelo instalador. Portanto, os dois arquivos precisam permanecer juntos durante a instalação.

A instalação fica em:

```text
~/Aplicativos/DestacadorBoletins_v3_2_1
```

Também é criado o atalho **Destacador de Boletins v3.2.1** no menu de aplicativos. O instalador não altera os arquivos da versão 3.1.

## Como usar

1. Abra o menu de aplicativos do Linux Mint.
2. Procure por **Destacador de Boletins v3.2.1** e abra.
3. Selecione o PDF original dos boletins.
4. Aguarde a mensagem de conclusão.
5. Confira os dois arquivos criados **na mesma pasta do PDF de origem**:
   - `NOME_DO_ARQUIVO_processado_v3_2_1.pdf`: boletins com destaques e resumo.
   - `NOME_DO_ARQUIVO_processado_v3_2_1_relatorio_pedagogico.pdf`: relatório separado para acompanhamento pedagógico.

O programa escolhe outro nome com um número final caso uma saída com o mesmo nome já exista. O PDF original não é alterado.

## Executar pelo Terminal

```bash
~/Aplicativos/DestacadorBoletins_v3_2_1/venv/bin/python ~/Aplicativos/DestacadorBoletins_v3_2_1/destacador_boletins_v3_2_1.py
```

## Atualizar ou reinstalar

1. Baixe novamente os dois arquivos da versão desejada.
2. Mantenha o script e o instalador na mesma pasta.
3. Execute novamente os comandos de instalação acima.

Reexecutar o instalador da 3.2.1 atualiza os arquivos dessa versão. As versões antigas ficam em diretórios separados. Guarde os PDFs originais e confira o resultado de um arquivo de teste após atualizar.

## Solução de problemas

### Tkinter não instalado

```bash
sudo apt update
sudo apt install python3-tk
```

### Erro ao criar o ambiente virtual

```bash
sudo apt install python3-venv
```

Depois, execute o instalador novamente.

### O instalador não encontra o script Python

Confira se os dois arquivos estão na mesma pasta e se os nomes correspondem à versão 3.2.1:

```bash
ls -l destacador_boletins_v3_2_1.py Instalar_Destacador_Boletins_v3_2_1.sh
```

### Resumo fora do lugar, faltas/notas incorretas ou estrelas ausentes

O aplicativo usa posições fixas de colunas e palavras do modelo de boletim para identificar notas, faltas e limites de cada boletim. O formato do PDF ou mudanças no formulário podem exigir ajuste do código. Não entregue o PDF processado até conferir as duas folhas, as notas contornadas, as estrelas, a soma de faltas, o aproveitamento e o relatório.

## Arquivos principais

- `destacador_boletins_v3_2_1.py` — aplicativo atual.
- `Instalar_Destacador_Boletins_v3_2_1.sh` — instalador atual.
- `destacador_boletins_v3_1.py` e `Instalar_Destacador_Boletins_v3_1.sh` — versão anterior, preservada.
- `tests/test_destacador.py` — teste automatizado com PDF fictício.
- `.github/workflows/test.yml` — execução automatizada dos testes.

## Privacidade

Boletins contêm dados pessoais de crianças e adolescentes. Use somente em ambiente autorizado e mantenha os PDFs em local seguro. Não envie boletins reais para repositórios públicos. O repositório ignora arquivos PDF, ambientes virtuais e arquivos temporários para reduzir o risco de publicação acidental.

## Licença

A licença ainda não foi definida. Consulte o responsável pelo repositório antes de reutilizar ou redistribuir o projeto.
