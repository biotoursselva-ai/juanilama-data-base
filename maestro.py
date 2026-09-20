import os
import io
import re
import json
import subprocess
import shutil
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# ==========================================
# CONFIGURACIÓN
# ==========================================
NOMBRE_HOJA = "Hoja de cálculo del registro de herpetofauna"
ARCHIVO_HTML = "index.html"
CARPETA_FOTOS = "Fotos del Registro"

# ==========================================
# 1. CONEXIÓN A GOOGLE SHEETS
# ==========================================
def conectar_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(NOMBRE_HOJA).sheet1
    return sheet, creds

# ==========================================
# 2. LEER DATOS
# ==========================================
def leer_datos(sheet):
    registros = sheet.get_all_records()
    print(f"📊 Se encontraron {len(registros)} avistamientos.")
    return registros

# ==========================================
# 3. DETECTAR ESPECIES NUEVAS
# ==========================================
def detectar_especies_nuevas(registros):
    with open(ARCHIVO_HTML, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    especies_existentes = re.findall(r'nombre_cientifico:\s*"([^"]+)"', html_content)
    print(f"🔍 Especies que ya están en el HTML: {len(especies_existentes)}")
    
    especies_nuevas = []
    for reg in registros:
        especie = reg.get("Especie observada")
        if especie and especie not in especies_existentes:
            if especie not in [e["nombre_cientifico"] for e in especies_nuevas]:
                especies_nuevas.append({
                    "nombre_cientifico": especie,
                    "clase": reg.get("grupo", ""),
                    "nota": reg.get("comportamiento observado", ""),
                    "imagen": reg.get("Evidencia", "")
                })
    
    print(f"🆕 Especies nuevas encontradas: {len(especies_nuevas)}")
    return especies_nuevas, html_content

# ==========================================
# 4. ACTUALIZAR HTML
# ==========================================
def actualizar_html(especies_nuevas, html_content):
    if len(especies_nuevas) == 0:
        print("✅ No hay especies nuevas. El HTML no necesita cambios.")
        return False
    
    nuevos_objetos = ""
    for esp in especies_nuevas:
        objeto = f"""    {{ nombre_cientifico: "{esp['nombre_cientifico']}", nombre_comun: "", nombre_ingles: "", familia: "", habitat: "", estado: "", imagen: "{esp['imagen']}", clase: "{esp['clase']}", nota: "{esp['nota']}" }},\n"""
        nuevos_objetos += objeto
    
    html_content = html_content.replace(
        "const especiesData = [",
        f"const especiesData = [\n{nuevos_objetos}"
    )
    
    with open(ARCHIVO_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Se agregaron {len(especies_nuevas)} especies nuevas al HTML.")
    return True

# ==========================================
# 5. SUBIR A GITHUB
# ==========================================
def subir_a_github():
    try:
        print("📤 Agregando cambios...")
        subprocess.run(["git", "add", "."], check=True)
        
        print("📝 Haciendo commit...")
        subprocess.run(["git", "commit", "-m", "Actualización automática del index.html"], check=False)
        
        print("🚀 Subiendo a GitHub...")
        subprocess.run(["git", "push", "origin", "master"], check=True)
        
        print("✅ ¡Listo! El archivo se subió a GitHub automáticamente.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al subir a GitHub: {e}")
        return False

# ==========================================
# 6. DESCARGAR FOTOS DE DRIVE (OPCIONAL)
# ==========================================
def descargar_fotos(registros, creds):
    if not os.path.exists(CARPETA_FOTOS):
        os.makedirs(CARPETA_FOTOS)
        print(f"📁 Carpeta '{CARPETA_FOTOS}' creada.")
    
    drive_service = build('drive', 'v3', credentials=creds)
    contador = 0
    
    print(f"📥 Descargando fotos de {len(registros)} avistamientos...")
    for reg in registros:
        fecha = str(reg.get("Fecha", "sin-fecha")).replace("/", "-")
        especie = str(reg.get("Especie observada", "sin-especie"))
        evidencia = str(reg.get("Evidencia", ""))
        
        if evidencia and "drive.google.com" in evidencia:
            try:
                if "/d/" in evidencia:
                    file_id = evidencia.split("/d/")[1].split("/")[0]
                elif "id=" in evidencia:
                    file_id = evidencia.split("id=")[1].split("&")[0]
                else:
                    continue
                
                request = drive_service.files().get_media(fileId=file_id)
                nombre_archivo = f"{fecha}_{especie}.jpg"
                ruta_archivo = os.path.join(CARPETA_FOTOS, nombre_archivo)
                
                with io.FileIO(ruta_archivo, 'wb') as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                
                contador += 1
                print(f"✅ Descargada: {nombre_archivo}")
            except Exception as e:
                print(f"❌ Error con {especie}: {e}")
    
    print(f"✅ Se descargaron {contador} fotos.")
    return contador

# ==========================================
# 7. ORGANIZAR FOTOS POR FECHA
# ==========================================
def organizar_fotos():
    if not os.path.exists(CARPETA_FOTOS):
        print(f"❌ La carpeta '{CARPETA_FOTOS}' no existe. No hay fotos para organizar.")
        return
    
    archivos = os.listdir(CARPETA_FOTOS)
    contador = 0
    
    for archivo in archivos:
        if archivo.endswith(".jpg"):
            partes = archivo.split("_")
            if len(partes) >= 1:
                fecha = partes[0]
                subcarpeta = os.path.join(CARPETA_FOTOS, fecha)
                if not os.path.exists(subcarpeta):
                    os.makedirs(subcarpeta)
                
                ruta_origen = os.path.join(CARPETA_FOTOS, archivo)
                ruta_destino = os.path.join(subcarpeta, archivo)
                shutil.move(ruta_origen, ruta_destino)
                contador += 1
    
    print(f"✅ Se organizaron {contador} fotos por fecha.")

# ==========================================
# 8. MENÚ PRINCIPAL
# ==========================================
def menu():
    print("\n" + "="*50)
    print("🤖 SCRIPT MAESTRO - REGISTRO DE HERPETOFAUNA")
    print("="*50)
    print("1. Actualizar HTML y subir a GitHub (rápido)")
    print("2. Descargar fotos de Drive")
    print("3. Organizar fotos por fecha")
    print("4. Hacer TODO (HTML + GitHub + Fotos)")
    print("5. Salir")
    print("="*50)
    
    opcion = input("Elige una opción (1-5): ")
    return opcion

# ==========================================
# 9. EJECUCIÓN PRINCIPAL
# ==========================================
def main():
    sheet, creds = conectar_sheets()
    registros = leer_datos(sheet)
    
    opcion = menu()
    
    if opcion == "1":
        especies_nuevas, html_content = detectar_especies_nuevas(registros)
        actualizar_html(especies_nuevas, html_content)
        subir_a_github()
    elif opcion == "2":
        descargar_fotos(registros, creds)
    elif opcion == "3":
        organizar_fotos()
    elif opcion == "4":
        especies_nuevas, html_content = detectar_especies_nuevas(registros)
        actualizar_html(especies_nuevas, html_content)
        subir_a_github()
        descargar_fotos(registros, creds)
        organizar_fotos()
    elif opcion == "5":
        print("👋 ¡Hasta luego!")
    else:
        print("❌ Opción no válida.")

if __name__ == "__main__":
    main()