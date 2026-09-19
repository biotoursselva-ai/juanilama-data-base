import re

# 1. LISTA DE ESPECIES DE PRUEBA A ELIMINAR
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

# 2. LEER EL ARCHIVO HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

print(f"📄 Archivo HTML leído. Tamaño original: {len(html_content)} caracteres.")

# 3. ELIMINAR LOS OBJETOS DE LAS ESPECIES DE PRUEBA
# El patrón busca líneas que comiencen con "{ nombre_cientifico: " y contengan una especie de prueba
patron = r'\s*\{ nombre_cientifico: "[^"]+",.*?\},\n'

# Función para reemplazar los objetos de prueba
def eliminar_prueba(match):
    linea = match.group(0)
    for especie in especies_prueba:
        if f'nombre_cientifico: "{especie}"' in linea:
            print(f"🗑️ Eliminando: {especie}")
            return ""  # Eliminar la línea
    return linea  # Mantener la línea

# Aplicar el reemplazo
html_content = re.sub(patron, eliminar_prueba, html_content)

# 4. GUARDAR EL ARCHIVO MODIFICADO
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Archivo HTML limpiado. Nuevo tamaño: {len(html_content)} caracteres.")
print("✅ Proceso completado.")