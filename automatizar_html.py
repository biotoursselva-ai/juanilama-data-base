import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# 1. CONFIGURACIÓN DE ACCESO
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
client = gspread.authorize(creds)

# 2. ABRIR LA HOJA VIEJA
nombre_hoja = "Hoja de cálculo del registro de herpetofauna"
sheet = client.open(nombre_hoja).sheet1

# 3. LEER LOS DATOS
registros = sheet.get_all_records()
print(f"✅ Conectado a la hoja: {nombre_hoja}")
print(f"📊 Se encontraron {len(registros)} avistamientos.")

# 4. LEER EL HTML ACTUAL
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 5. IDENTIFICAR LAS ESPECIES QUE YA ESTÁN EN EL HTML
especies_existentes = re.findall(r'nombre_cientifico:\s*"([^"]+)"', html_content)
print(f"🔍 Especies que ya están en el HTML: {len(especies_existentes)}")

# 6. IDENTIFICAR ESPECIES NUEVAS
especies_nuevas = []
for reg in registros:
    especie = reg.get("Especie observada")
    if especie and especie not in especies_existentes:
        if especie not in [e["nombre_cientifico"] for e in especies_nuevas]:
            especies_nuevas.append({
                "nombre_cientifico": especie,
                "clase": reg.get("grupo", ""),
                "nota": reg.get("comportamiento observado", ""),
                "imagen": reg.get("evidencia", "")
            })

print(f"🆕 Especies nuevas encontradas: {len(especies_nuevas)}")

# 7. SI HAY ESPECIES NUEVAS, MODIFICAR EL HTML
if len(especies_nuevas) > 0:
    print("✍️ Agregando especies nuevas al HTML...")
    
    nuevos_objetos = ""
    for esp in especies_nuevas:
        objeto = f"""    {{ nombre_cientifico: "{esp['nombre_cientifico']}", nombre_comun: "", nombre_ingles: "", familia: "", habitat: "", estado: "", imagen: "{esp['imagen']}", clase: "{esp['clase']}", nota: "{esp['nota']}" }},\n"""
        nuevos_objetos += objeto
    
    html_content = html_content.replace(
        "const especiesData = [",
        f"const especiesData = [\n{nuevos_objetos}"
    )
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ ¡Listo! Se agregaron {len(especies_nuevas)} especies nuevas al archivo 'index.html'.")
else:
    print("✅ No se encontraron especies nuevas. Tu página web ya está actualizada.")