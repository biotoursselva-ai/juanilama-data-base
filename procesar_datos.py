import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# 1. CONFIGURACIÓN DE ACCESO
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
client = gspread.authorize(creds)

# 2. ABRIR TU HOJA
nombre_hoja = "Respuestas de formulario 1"
sheet = client.open("Hoja de cálculo del registro de herpetofauna").worksheet(nombre_hoja)

# 3. LEER DATOS
datos = pd.DataFrame(sheet.get_all_records())

# 4. LISTA ACTUAL DE ESPECIES (La que ya tienes en tu index.html)
especies_existentes = [
    "Craugastor bransfordii", "Incilius valliceps", "Craugastor fitzingeri",
    "Agalychnis callidryas", "Boana rufitela", "Bolitoglossa striatula",
    "Smilisca sordida", "Teratohyla spinosa", "Smilisca phaeota",
    "Diasporus diastema", "Scinax elaeochroa", "Dendrobates auratus",
    "Lithobates vaillanti", "Incilius coniferus", "Gymnopis multiplicata",
    "Leptodactylus poecilochilus", "Craugastor crassidigitus", "Scinax boulengeri",
    "Leptodactylus savagei", "Incilius melanochlorus", "Rhinella marina",
    "Dendropsophus ebraccatus", "Craugastor persimilis", "Oophaga pumilio",
    "Basiliscus vittatus", "Bothrops asper", "Micrurus mosquitensis",
    "Rhinoclemmys funerea", "Holcosus festivus", "Imantodes cenchoa",
    "Bothriechis nigroadspersus", "Leptodeira rhombifera", "Leptodeira ornata",
    "Basiliscus plumifrons", "Anolis oxylophus", "Anolis humilis",
    "Chelydra acutirostris", "Mastigodryas melanolomus", "Sibon nebulatus",
    "Clelia clelia", "Corytophanes cristatus", "Porthidium nasutum",
    "Hydromorphus concolor", "Iguana iguana"
]

# 5. IDENTIFICAR ESPECIES NUEVAS
especies_nuevas = datos[~datos["Especie observada"].isin(especies_existentes)]

# 6. GENERAR EL HTML PARA ESPECIES NUEVAS
if len(especies_nuevas) > 0:
    objetos_html = []
    for i, row in especies_nuevas.iterrows():
        objeto = {
            "nombre_cientifico": row["Especie observada"],
            "nombre_comun": "",  # Lo llenas manualmente después
            "nombre_ingles": "", # Lo llenas manualmente después
            "familia": "",       # Lo llenas manualmente después
            "habitat": "",       # Lo llenas manualmente después
            "estado": "",        # Lo llenas manualmente después
            "imagen": row["Evidencia"], # Aquí va el link (pero es de Drive, lo cambias después)
            "clase": row["Grupo"],
            "nota": row["Notas"]
        }
        objetos_html.append(objeto)
    
    # 7. GUARDAR EL ARCHIVO
    with open("especies_nuevas.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(objetos_html, ensure_ascii=False, indent=4))
    
    print(f"✅ Se encontraron {len(objetos_html)} especies nuevas.")
    print("Abre el archivo 'especies_nuevas.txt' y pega los objetos en tu index.html")
else:
    print("✅ No se encontraron especies nuevas. La página ya está actualizada.")