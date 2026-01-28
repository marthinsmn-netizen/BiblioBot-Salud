from Bio import Entrez
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
Entrez.email = os.getenv("EMAIL_USER") 
# Agregamos esta línea para evitar el warning si el .env falla por un segundo
if not Entrez.email:
    Entrez.email = "tu_correo@ejemplo.com"

def buscar_articulos(terminos, dias_atras=7):
    try:
        fecha_inicio = (datetime.datetime.now() - datetime.timedelta(days=dias_atras)).strftime("%Y/%m/%d")
        query = f"({terminos}) AND ({fecha_inicio}[PDAT] : 3000[PDAT])"
        handle = Entrez.esearch(db='pubmed', term=query, retmax=5)
        record = Entrez.read(handle)
        handle.close()
        id_list = record.get("IdList", [])
        return [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" for pmid in id_list]
    except Exception as e:
        print(f"Error en PubMed: {e}")
        return []
