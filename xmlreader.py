import os
import xml.etree.ElementTree as ET
import pandas as pd

diretorio = "/home/fabio/Projects/xmlreader"

planilha_clientes = pd.read_excel(
    "planilha_clientes.xlsx", dtype={'cnpj': str})

planilha_cidades = pd.read_excel("planilha_cidades.xlsx")

arquivos_xml = [arquivo for arquivo in os.listdir(
    diretorio) if arquivo.endswith('.xml')]

produtos_totais = {}
trocas = []
observacoes = []
fora_rota = []

for arquivo_xml in arquivos_xml:
    caminho_arquivo_xml = os.path.join(diretorio, arquivo_xml)

    tree = ET.parse(arquivo_xml)
    root = tree.getroot()

    cnpj_cliente = root.find(
        ".//{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}CNPJ").text

    for index, cnpj in enumerate(planilha_clientes['cnpj']):
        if cnpj_cliente == cnpj:
            observacoes.append(
                [planilha_clientes['nome'][index], planilha_clientes['observação'][index]])

    cidades = root.find(
        ".//{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}enderDest/{http://www.portalfiscal.inf.br/nfe}/cMun").text
    
    for cidade in cidades:
        if cidade in planilha_cidades['suzano']:
            

    produtos = root.findall(".//{http://www.portalfiscal.inf.br/nfe}det")

    for produto in produtos:
        codigo_produto = produto.find(
            '{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}cProd'
        ).text
        nome_produto = produto.find(
            '{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}xProd'
        ).text
        quantidade_produto = produto.find(
            '{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}qCom'
        ).text

        if codigo_produto in produtos_totais:
            produtos_totais[codigo_produto]["quantidade"] += float(
                quantidade_produto)
        else:
            produtos_totais[codigo_produto] = {
                'nome': nome_produto, 'quantidade': float(quantidade_produto)}

print(produtos_totais)
