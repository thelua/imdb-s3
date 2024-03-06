import sqlite3
import csv

conn = sqlite3.connect('imdb.sqlite3')
cursor = conn.cursor()

def criar_banco_de_dados():

    cursor.execute('''
                DROP TABLE IF EXISTS filme
                   '''
    )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filme (
            tconst TEXT PRIMARY KEY,
            titleType TEXT,
            primaryTitle TEXT,
            originalTitle TEXT,
            startYear INTEGER,
            endYear INTEGER
        )
    ''')

    cursor.execute('''
                DROP TABLE IF EXISTS profissao
                   '''
    )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profissao (
            tconst TEXT,
            ordering INTEGER,
            nconst TEXT,
            category TEXT,
            job TEXT,
            characters TEXT,
            FOREIGN KEY (tconst) REFERENCES filme (tconst),
            PRIMARY KEY (tconst, ordering)
        )
    ''')

    cursor.execute('''
                DROP TABLE IF EXISTS nome
                   '''
    )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nome (
            nconst TEXT PRIMARY KEY,
            primaryName TEXT,
            primaryProfession TEXT,
            knownForTitles TEXT
        )
    ''')

    with open('descompactado/title.basics.tsv', 'r', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo, delimiter='\t')
        for row in reader:
            inserir_filme(row['tconst'], row['titleType'], row['primaryTitle'], row['originalTitle'], row['startYear'], row['endYear'])

    with open('descompactado/title.principals.tsv', 'r', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo, delimiter='\t')
        for row in reader:
            inserir_profissao(row['tconst'], row['ordering'], row['nconst'], row['category'], row['job'], row['characters'])

    with open('descompactado/name.basics.tsv', 'r', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo, delimiter='\t')
        for row in reader:
            inserir_nome(row['nconst'], row['primaryName'], row['primaryProfession'], row['knownForTitles'])

    conn.commit()
    conn.close()

def inserir_filme(tconst, titleType, primaryTitle, originalTitle, startYear, endYear):
    cursor.execute('''
        INSERT OR IGNORE INTO filme (tconst, titleType, primaryTitle, originalTitle, startYear, endYear)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tconst, titleType, primaryTitle, originalTitle, startYear, endYear))

def inserir_profissao(tconst, ordering, nconst, category, job, characters):
    cursor.execute('''
        INSERT OR IGNORE INTO profissao (tconst, ordering, nconst, category, job, characters)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tconst, ordering, nconst, category, job, characters))

def inserir_nome(nconst, primaryName, primaryProfession, knownForTitles):
    cursor.execute('''
        INSERT OR IGNORE INTO nome (nconst, primaryName, primaryProfession, knownForTitles)
        VALUES (?, ?, ?, ?)
    ''', (nconst, primaryName, primaryProfession, knownForTitles))