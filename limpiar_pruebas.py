import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. CONFIGURACIÓN DE ACCESO
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
client = gspread.authorize(creds)

# 2. ABRIR LA HOJA DE CÁLCULO
nombre_hoja = "Hoja de cálculo del registro de herpetofauna"
sheet = client.open(nombre_hoja).worksheet("Respuestas de formulario 1")

# 3. ESPECIES DE PRUEBA A ELIMINAR
especies_prueba = [
    "Crotalus simus",
    "Rana de prueba",
    "La vaca lola",
    "Barni",
    "Ela la vaca",
    "Ultima prueba",
    "Lithobates vibicarius",
    "Lepidophyma flavimaculatum"
]

# 4. LEER TODOS LOS DATOS
datos = sheet.get_all_values()
print(f"📊 Total de filas antes de limpiar: {len(datos)}")

# 5. IDENTIFICAR FILAS A BORRAR (de abajo hacia arriba para no desfasar índices)
filas_a_borrar = []
for i, fila in enumerate(datos):
    if i == 0:  # Saltar encabezado
        continue
    especie = fila[2]  # Columna C (índice 2) = Especie observada
    if especie in especies_prueba:
        filas_a_borrar.append(i + 1)  # +1 porque las filas en Sheets empiezan en 1

# 6. BORRAR LAS FILAS
if filas_a_borrar:
    print(f"🗑️ Se encontraron {len(filas_a_borrar)} filas para borrar.")
    for fila in reversed(filas_a_borrar):  # De abajo hacia arriba
        sheet.delete_rows(fila)
        print(f"✅ Fila {fila} eliminada.")
    print(f"✅ Proceso completado. Quedan {len(datos) - len(filas_a_borrar)} filas.")
else:
    print("✅ No se encontraron especies de prueba para borrar.")