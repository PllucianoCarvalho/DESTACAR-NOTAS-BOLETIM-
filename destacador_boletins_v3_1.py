#!/usr/bin/env python3
"""Destacador de boletins v3.1: preserva versões anteriores e imprime resumo no boletim entregue à família."""
from pathlib import Path
import re
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox

LIMITE = 6.0
PRETO = (0, 0, 0)

def numero(txt):
    txt = txt.strip().replace(',', '.')
    if not re.fullmatch(r'\d{1,2}(?:\.\d+)?', txt):
        return None
    try: n = float(txt)
    except ValueError: return None
    return n if 0 <= n <= 10 else None

def classificar(p):
    if p > 95: return 'Avançado'
    if p > 80: return 'Adequado'
    if p > 60: return 'Básico'
    return 'Abaixo do básico'

def processar(entrada, saida, relatorio):
    doc = fitz.open(entrada)
    dados = []
    total_marcadas = 0
    try:
        for page in doc:
            words = page.get_text('words')
            # Identifica os limites verticais de cada boletim pela linha Disciplina.
            headers = sorted([w for w in words if w[4].strip().lower() == 'disciplina'], key=lambda w:w[1])
            nota_heads = sorted([w for w in words if w[4].strip().lower() == 'nota'], key=lambda w:(w[1],w[0]))
            # Destaca exclusivamente as células numéricas das colunas Nota.
            for nh in nota_heads:
                xc = (nh[0]+nh[2])/2
                y_start = nh[3] + 1
                same_table = [h for h in nota_heads if h[1] > nh[1]+1 and h[1] < nh[1]+230]
                y_end = min([h[1] for h in same_table] or [page.rect.height])
                for w in words:
                    x0,y0,x1,y1,txt = w[:5]
                    if not (y_start < y0 < y_end) or abs((x0+x1)/2-xc)>14: continue
                    n = numero(txt)
                    if n is None or n >= LIMITE: continue
                    a = page.add_rect_annot(fitz.Rect(x0-1.5,y0-1,x1+1.5,y1+1))
                    a.set_colors(stroke=PRETO)
                    a.set_border(width=1.2)
                    a.update()
                    total_marcadas += 1
            for i, head in enumerate(headers):
                top = head[1]
                bottom = headers[i+1][1] if i+1 < len(headers) else page.rect.height
                block = [w for w in words if top-60 <= w[1] < bottom]
                # Nome na mesma linha do campo Nome:
                name = 'Aluno não identificado'
                for j,w in enumerate(block):
                    if w[4].strip().lower().startswith('nome:'):
                        yname = w[1]
                        parts=[]
                        for z in block[j+1:]:
                            if abs(z[1]-yname)>2: break
                            if z[4].strip().lower() in ('rg:', 'nº', 'nº chamada:'): break
                            parts.append(z[4])
                        if parts: name=' '.join(parts).strip()
                        break
                # Coordenadas observadas no modelo de boletim anexado.
                row_top = head[3]+1
                result_y = min([w[1] for w in words if w[4].strip().lower()=='resultado' and row_top < w[1] < bottom] or [bottom-18])
                grades=[]; absences=[]
                for w in words:
                    x0,y0,x1,y1,txt=w[:5]; cx=(x0+x1)/2; cy=(y0+y1)/2
                    if not (row_top < cy < result_y): continue
                    n=numero(txt)
                    if n is None: continue
                    if any(abs(cx-x)<13 for x in (160,233,306)): grades.append(n)
                    if any(abs(cx-x)<13 for x in (196,270,343)) and float(n).is_integer(): absences.append(int(n))
                faltas=sum(absences)
                pct=(sum(grades)/(10*len(grades))*100) if grades else None
                classificacao=classificar(pct) if pct is not None else 'Sem notas numéricas'
                item={'nome':name,'faltas':faltas,'notas':grades,'percentual':pct,'classificacao':classificacao}
                dados.append(item)
                # Imprime o resumo no próprio boletim, na área inferior do bloco do aluno.
                # As coordenadas são limitadas à página e ao bloco para não invadir o boletim seguinte.
                largura = page.rect.width
                # Os dois indicadores ficam na MESMA linha, evitando invadir a linha
                # de assinatura do secretário/diretor. Mantém-se o resultado final intacto.
                x_faltas = max(24, largura - 310)
                x_aprov = max(24, largura - 600)
                y_resumo = min(result_y + 13, bottom - 34)
                if y_resumo > row_top:
                    page.insert_text((x_aprov, y_resumo),
                                     f'Aproveitamento: {pct:.1f}% - {classificacao}' if pct is not None else f'Classificação: {classificacao}',
                                     fontsize=7, fontname='helv', color=PRETO)
                    page.insert_text((x_faltas, y_resumo), f'Total de faltas: {faltas}',
                                     fontsize=7, fontname='helv', color=PRETO)
        doc.save(saida,garbage=4,deflate=True)
    finally: doc.close()
    # Relatório separado para a pedagoga, com uma ficha por aluno com notas baixas.
    rel=fitz.open(); page=rel.new_page(width=595,height=842); y=48
    def write(line='', size=10):
        nonlocal page,y
        if y>790:
            page=rel.new_page(width=595,height=842); y=48
        if line: page.insert_text((42,y),line[:105],fontsize=size,fontname='helv',color=PRETO)
        y += 17 if line else 10
    write('RELATÓRIO PEDAGÓGICO - ACOMPANHAMENTO DO RENDIMENTO',12)
    write(f'Arquivo: {Path(entrada).name}',9); write('Critério: nota numérica abaixo de 6,0 em qualquer trimestre.',9); write()
    baixos=[d for d in dados if any(n<LIMITE for n in d['notas'])]
    if not baixos: write('Nenhum aluno com nota abaixo de 6,0 foi identificado.')
    for d in baixos:
        write(f"Aluno(a): {d['nome']}")
        write(f"Soma de faltas: {d['faltas']} | Aproveitamento: {d['percentual']:.1f}% - {d['classificacao']}" if d['percentual'] is not None else f"Soma de faltas: {d['faltas']} | {d['classificacao']}",9)
        write('Notas abaixo de 6,0: verificar as células contornadas no boletim processado.',9)
        write(); write('Ciência do pai/mãe/responsável: __________________________________________',9)
        write('Assinatura: ___________________________________________________________',9)
        write('Data: ______/______/____________',9); write(); write('- '*45,8); write()
    rel.save(relatorio,garbage=4,deflate=True); rel.close()
    return total_marcadas,dados,len(baixos)

def main():
    root=tk.Tk(); root.withdraw(); root.attributes('-topmost',True)
    path=filedialog.askopenfilename(title='Escolha o PDF original dos boletins',filetypes=[('Arquivos PDF','*.pdf')],parent=root)
    if not path: root.destroy(); return
    src=Path(path); out=src.with_name(src.stem+'_processado_v3_1'+src.suffix); i=2
    while out.exists(): out=src.with_name(f'{src.stem}_processado_v3_{i}{src.suffix}'); i+=1
    report=src.with_name(out.stem+'_relatorio_pedagogico.pdf')
    try:
        marked,students,low=processar(src,out,report)
        messagebox.showinfo('Concluído',f'Notas contornadas: {marked}\nBoletins analisados: {len(students)}\nAlunos com notas baixas: {low}\n\nBoletins:\n{out}\n\nRelatório pedagógico:\n{report}',parent=root)
    except Exception as e: messagebox.showerror('Erro ao processar PDF',str(e),parent=root)
    finally: root.destroy()
if __name__=='__main__': main()
