import os
import xml.etree.ElementTree as ET
import pandas as pd

diretorio = "/home/fabio/Projects/xmlreader"

planilha_clientes = pd.read_excel("planilha.xlsx", dtype={'cnpj': str})

arquivos_xml = [arquivo for arquivo in os.listdir(
    diretorio) if arquivo.endswith('.xml')]

observacoes = []

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

print(observacoes)
