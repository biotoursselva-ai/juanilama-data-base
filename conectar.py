import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. CONFIGURACIÓN DE ACCESO
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
client = gspread.authorize(creds)

# 2. ABRIR TU HOJA DE CÁLCULO
nombre_hoja = "Hoja de cálculo del registro de herpetofauna"
sheet = client.open(nombre_hoja).sheet1

# 3. LEER Y VER LOS DATOS
print(f"✅ Conectado a la hoja: {nombre_hoja}")
registros = sheet.get_all_records()
print(f"📊 Se encontraron {len(registros)} avistamientos registrados.")
print("--------------------------------------------------")

# 4. Mostramos los primeros 3 registros con tus columnas reales
for registro in registros[:3]:
    print(f"📅 Fecha: {registro.get('Fecha')}")
    print(f"🐸 Especie: {registro.get('especie obdervada')}")  # Columna de nombre científico
    print(f"🦎 Grupo: {registro.get('grupo')}")
    print(f"📍 Transecto: {registro.get('transecto encontrado')}")
    print(f"📝 Comportamiento: {registro.get('comportamiento observado')}")
    print(f"📷 Evidencia: {registro.get('evidencia')}")
    print(f"👁️ Observadores: {registro.get('observadores')}")
    print(f"💡 Etapa: {registro.get('etapa')}")
    print(f"🕐 Hora: {registro.get('hora')}")
    print(f"🌿 Microhábitat: {registro.get('microhabitat')}")
    print(f"💬 Notas: {registro.get('notas')}")
    print("==========================================")