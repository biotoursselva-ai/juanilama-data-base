import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 1. CONFIGURACIÓN DE ACCESO
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
client = gspread.authorize(creds)

# 2. ABRIR TU HOJA
nombre_hoja = "Respuestas de formulario 1"
sheet = client.open("Hoja de cálculo del registro de herpetofauna").worksheet(nombre_hoja)

# 3. LEER TODOS LOS DATOS COMO TABLA
datos = pd.DataFrame(sheet.get_all_records())

print(f"✅ Se encontraron {len(datos)} avistamientos.")

# 4. CLASIFICAR POR GRUPO
print("\n🐸🦎 Clasificación por grupo:")
print(datos["Grupo"].value_counts())

# 5. CONTAR LAS ESPECIES MÁS VISTAS
print("\n📊 Top 5 especies más avistadas:")
print(datos["Especie observada"].value_counts().head(5))

# 6. EXTRAER LOS LINKS DE LAS FOTOS
links_fotos = datos["Evidencia"].tolist()
print(f"\n📷 Se encontraron {len(links_fotos)} links de fotos.")
print("Primeros 2 links:", links_fotos[:2])