import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. CONFIGURACIÓN DE ACCESO
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
client = gspread.authorize(creds)

# 2. LEER EL HTML Y EXTRAER FAMILIAS
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Extraer especies y familias del HTML
patron = r'nombre_cientifico:\s*"([^"]+)"[^}]*?familia:\s*"([^"]*)"'
coincidencias = re.findall(patron, html_content)

diccionario_familias = {}
for especie, familia in coincidencias:
    especie_limpia = especie.strip()
    diccionario_familias[especie_limpia] = familia.strip()

print(f"📖 Se encontraron {len(diccionario_familias)} especies con familia en el HTML.")
for esp, fam in list(diccionario_familias.items())[:5]:
    print(f"   - {esp}: {fam}")

# 3. ABRIR LA HOJA DE CÁLCULO
nombre_hoja = "Hoja de cálculo del registro de herpetofauna"
sheet = client.open(nombre_hoja).worksheet("Respuestas de formulario 1")

# 4. VERIFICAR SI YA EXISTE LA COLUMNA "Familia"
encabezados = sheet.row_values(1)
print(f"\n📋 Encabezados actuales: {encabezados}")

if "Familia" not in encabezados:
    # Agregar la columna al final
    nueva_columna = len(encabezados) + 1
    sheet.update_cell(1, nueva_columna, "Familia")
    print(f"✅ Columna 'Familia' agregada en la posición {nueva_columna}.")
    col_familia = nueva_columna
else:
    col_familia = encabezados.index("Familia") + 1
    print(f"✅ La columna 'Familia' ya existe en la posición {col_familia}.")

# 5. LLENAR LAS FAMILIAS
datos = sheet.get_all_values()
actualizados = 0
for i, fila in enumerate(datos):
    if i == 0:  # Saltar encabezado
        continue
    especie = fila[2].strip()  # Columna C
    if especie in diccionario_familias:
        familia = diccionario_familias[especie]
        if fila[col_familia - 1] != familia:
            sheet.update_cell(i + 1, col_familia, familia)
            actualizados += 1

print(f"\n✅ Se actualizaron {actualizados} familias en la hoja.")
print("✅ Proceso completado.")