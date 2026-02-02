from Bio import Entrez

def buscar_articulos(terminos, filtros_extra=""):
    Entrez.email = "tu_email@ejemplo.com"
    
    # Verificación de seguridad: si no hay términos, no buscamos nada
    if not terminos or terminos.strip() == "":
        print("⚠️ No hay términos de búsqueda para este suscriptor.")
        return [], "Sin estrategia"

    estrategia = f"({terminos})"
    if filtros_extra:
        estrategia += f" AND ({filtros_extra})"
    
    try:
        handle = Entrez.esearch(db="pubmed", term=estrategia, retmax=5, sort="relevance")
        record = Entrez.read(handle)
        handle.close()
        
        id_list = record.get("IdList", [])
        links = [f"https://pubmed.ncbi.nlm.nih.gov/{id}/" for id in id_list]
        
        return links, estrategia
    except Exception as e:
        print(f"❌ Error en la API de PubMed: {e}")
        return [], estrategia