import requests
import gzip
import shutil
import os
from datetime import datetime
import sqlite3
import time
from bd import criar_banco_de_dados

inicio = time.time()

links = [
    'https://datasets.imdbws.com/title.basics.tsv.gz',
    'https://datasets.imdbws.com/title.principals.tsv.gz', 
    'https://datasets.imdbws.com/name.basics.tsv.gz'   
]

def baixar_e_descompactar(url, caminho_arquivo_entrada, caminho_arquivo_intermediario):
    response = requests.get(url, stream=True)
    with open(caminho_arquivo_entrada, 'wb') as arquivo_local:
        shutil.copyfileobj(response.raw, arquivo_local)

    with gzip.open(caminho_arquivo_entrada, 'rb') as arquivo_comprimido, open(caminho_arquivo_intermediario, 'wb') as arquivo_descomprimido:
        shutil.copyfileobj(arquivo_comprimido, arquivo_descomprimido)

    print(f'Atualização para {url} concluída.')

    os.remove(caminho_arquivo_entrada)


diretorio_entrada = 'dataset'
os.makedirs(diretorio_entrada, exist_ok=True)

diretorio_saida = 'descompactado'
os.makedirs(diretorio_saida, exist_ok=True)

for url in links:
    arquivo_entrada = os.path.basename(url)
    final = arquivo_entrada.replace('.gz', '')

    caminho_arquivo_entrada = os.path.join(diretorio_entrada, arquivo_entrada)
    
    caminho_arquivo_final = os.path.join(diretorio_saida, final)

    hoje = datetime.now().date()
    ultima_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo_entrada)).date() if os.path.exists(caminho_arquivo_entrada) else None

    if ultima_modificacao is None or ultima_modificacao < hoje:
        baixar_e_descompactar(url, caminho_arquivo_entrada, caminho_arquivo_final)
    else:
        print(f'O arquivo {arquivo_entrada} já foi atualizado hoje!')

fim = time.time()
tempo_decorrido = fim - inicio

print(f"Tempo decorrido: {tempo_decorrido} segundos")


def main():
    criar_banco_de_dados()

    conn = sqlite3.connect('imdb.sqlite3')
    cursor = conn.cursor()

    def criar_view():
        try:

            cursor.execute('''
                        DROP VIEW  IF EXISTS top_cem_atores_10_anos
                           ''')

            cursor.execute('''
            CREATE VIEW top_cem_atores_10_anos AS
            SELECT n.nconst, n.primaryName AS ator_nome,
                COUNT(DISTINCT f.tconst) AS qnt_filmes
            FROM filme f
            JOIN profissao p ON f.tconst = p.tconst
            JOIN nome n ON p.nconst = n.nconst
            WHERE f.titleType = 'movie'
            AND f.startYear >= strftime('%Y', 'now', '-10 years')
            AND p.category IN ('actor', 'actress')
            GROUP BY n.primaryName
            ORDER BY qnt_filmes DESC
            LIMIT 100;

            ''')

            cursor.execute('''
            SELECT * FROM top_cem_atores_10_anos
        ''')
            
            diretorio_resultado = 'resultado'
            os.makedirs(diretorio_resultado, exist_ok=True)

            títulos = ["NCONST", "NOME", "FILMES_FEITOS"]
            with open('resultado/top_100_atores.csv', 'w') as f:
                f.write("\t".join(títulos) + "\n") 
                for row in cursor.fetchall():
                    f.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

        except sqlite3.Error as e:
            print(f"Ocorreu um erro na criação da view: {e}")
            conn.rollback()
        finally:
            conn.commit()
            conn.close()

    criar_view()


if __name__ == '__main__':
    main()