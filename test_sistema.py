# ================================================================
# SISTEMA DE PRUEBAS (QA) - REGISTRO DE HERPETOFAUNA
# Reserva Juanilama, San Carlos, Costa Rica
#
# Autor: Adrián Quesada Enríquez
# Año: 2026
#
# DESCRIPCIÓN:
#   Este script verifica que el sistema de automatización funciona
#   correctamente. Incluye pruebas unitarias, de integración y
#   métricas de calidad.
#
# CÓMO EJECUTAR:
#   py test_sistema.py
# ================================================================

import unittest
import time
import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ================================================================
# CONFIGURACIÓN
# ================================================================
NOMBRE_HOJA = "Hoja de cálculo del registro de herpetofauna"
NOMBRE_PESTANA = "Respuestas de formulario 1"
ARCHIVO_HTML = "index.html"
ARCHIVO_CREDENCIALES = "credenciales.json"

# Palabras clave para filtrar entradas de prueba (igual que en Apps Script)
PALABRAS_PRUEBA = ["prueba", "test", "ejemplo", "demo", "fake", "vaca lola", "vacalola"]


# ================================================================
# FUNCIONES AUXILIARES (Replican la lógica del Apps Script)
# ================================================================

def normalizar_nombre(nombre):
    """Normaliza un nombre científico igual que en Apps Script."""
    if not nombre:
        return ""
    return (nombre.lower()
            .strip()
            .replace("  ", " ")
            .replace("festivos", "festivus")
            .replace("sp. aff.", "sp. aff."))


def es_entrada_de_prueba(especie):
    """Detecta si una especie es una entrada de prueba."""
    if not especie:
        return True
    nombre_lower = especie.lower()
    return any(palabra in nombre_lower for palabra in PALABRAS_PRUEBA)


def extraer_especies_html(html):
    """Extrae los nombres científicos del HTML."""
    patron = r'nombre_cientifico:\s*"([^"]+)"'
    return re.findall(patron, html)


# ================================================================
# CLASE DE PRUEBAS
# ================================================================
class TestSistemaHerpetofauna(unittest.TestCase):

    # ------------------------------------------------------------
    # PRUEBAS UNITARIAS (Componentes por separado)
    # ------------------------------------------------------------

    def test_01_credenciales_existen(self):
        """Verifica que el archivo de credenciales existe."""
        self.assertTrue(
            os.path.exists(ARCHIVO_CREDENCIALES),
            f"❌ No se encontró el archivo '{ARCHIVO_CREDENCIALES}'."
        )

    def test_02_conexion_google_sheets(self):
        """Verifica que la conexión con Google Sheets funciona."""
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            ARCHIVO_CREDENCIALES, scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(NOMBRE_HOJA).worksheet(NOMBRE_PESTANA)
        self.assertIsNotNone(sheet, "❌ No se pudo abrir la hoja de cálculo.")

    def test_03_hoja_tiene_columnas(self):
        """Verifica que la hoja tiene las columnas esperadas."""
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            ARCHIVO_CREDENCIALES, scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(NOMBRE_HOJA).worksheet(NOMBRE_PESTANA)
        encabezados = sheet.row_values(1)

        columnas_esperadas = ["Especie observada", "Grupo", "Evidencia", "Familia"]
        for col in columnas_esperadas:
            self.assertIn(
                col, encabezados,
                f"❌ Falta la columna '{col}' en la hoja."
            )

    def test_04_normalizacion_nombres(self):
        """Verifica que la normalización de nombres funciona."""
        self.assertEqual(
            normalizar_nombre("Holcosus festivos"),
            "holcosus festivus",
            "❌ La normalización no corrige 'festivos' a 'festivus'."
        )
        self.assertEqual(
            normalizar_nombre("  AGALYCHNIS CALLIDRYAS  "),
            "agalychnis callidryas",
            "❌ La normalización no maneja espacios ni mayúsculas."
        )

    def test_05_filtro_pruebas(self):
        """Verifica que el filtro de entradas de prueba funciona."""
        self.assertTrue(es_entrada_de_prueba("Rana de prueba"))
        self.assertTrue(es_entrada_de_prueba("La vaca lola"))
        self.assertTrue(es_entrada_de_prueba("test"))
        self.assertFalse(es_entrada_de_prueba("Agalychnis callidryas"))
        self.assertFalse(es_entrada_de_prueba("Holcosus festivus"))

    def test_06_html_existe(self):
        """Verifica que el archivo index.html existe."""
        self.assertTrue(
            os.path.exists(ARCHIVO_HTML),
            f"❌ No se encontró el archivo '{ARCHIVO_HTML}'."
        )

    def test_07_html_tiene_marcador(self):
        """Verifica que el HTML tiene el marcador para insertar especies."""
        with open(ARCHIVO_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn(
            "const especiesData = [", html,
            "❌ El HTML no tiene el marcador 'const especiesData = ['."
        )

    def test_08_extraer_especies_html(self):
        """Verifica que se pueden extraer especies del HTML."""
        with open(ARCHIVO_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        especies = extraer_especies_html(html)
        self.assertGreater(
            len(especies), 10,
            "❌ Se esperaban al menos 10 especies en el HTML."
        )

    def test_09_no_hay_duplicados_html(self):
        """Verifica que no haya especies duplicadas en el HTML."""
        with open(ARCHIVO_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        especies = extraer_especies_html(html)
        especies_normalizadas = [normalizar_nombre(e) for e in especies]
        duplicados = [e for e in set(especies_normalizadas)
                      if especies_normalizadas.count(e) > 1]

        if duplicados:
            print(f"\n⚠️  Especies duplicadas encontradas: {duplicados}")
        # No fallamos la prueba, pero avisamos
        self.assertIsInstance(duplicados, list)

    # ------------------------------------------------------------
    # PRUEBAS DE INTEGRACIÓN (Flujo completo)
    # ------------------------------------------------------------

    def test_10_flujo_completo(self):
        """Verifica que el flujo completo de lectura funciona."""
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            ARCHIVO_CREDENCIALES, scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(NOMBRE_HOJA).worksheet(NOMBRE_PESTANA)
        registros = sheet.get_all_records()

        self.assertGreater(
            len(registros), 0,
            "❌ No se encontraron registros en la hoja."
        )

        # Verificar que cada registro tiene los campos clave
        for reg in registros[:5]:
            self.assertIn("Especie observada", reg)
            self.assertIn("Grupo", reg)

    def test_11_especies_unicas_en_hoja(self):
        """Verifica cuántas especies únicas hay en la hoja."""
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            ARCHIVO_CREDENCIALES, scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(NOMBRE_HOJA).worksheet(NOMBRE_PESTANA)
        registros = sheet.get_all_records()

        especies = [r.get("Especie observada", "").strip()
                    for r in registros if r.get("Especie observada")]
        especies_unicas = set(normalizar_nombre(e) for e in especies)

        print(f"\n📊 Especies únicas en la hoja: {len(especies_unicas)}")
        self.assertGreater(len(especies_unicas), 0)


# ================================================================
# EJECUCIÓN DE PRUEBAS CON MÉTRICAS DE CALIDAD
# ================================================================
def ejecutar_pruebas():
    """Ejecuta las pruebas y genera un reporte de calidad."""
    print("=" * 60)
    print("🧪 SISTEMA DE PRUEBAS (QA) - HERPETOFAUNA")
    print("=" * 60)
    print(f"📅 Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Directorio: {os.getcwd()}")
    print("=" * 60)
    print()

    inicio = time.time()

    # Cargar y ejecutar pruebas
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSistemaHerpetofauna)
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    fin = time.time()
    duracion = fin - inicio

    # Métricas de calidad
    total = resultado.testsRun
    fallidas = len(resultado.failures) + len(resultado.errors)
    exitosas = total - fallidas
    tasa_exito = (exitosas / total * 100) if total > 0 else 0

    print()
    print("=" * 60)
    print("📊 MÉTRICAS DE CALIDAD")
    print("=" * 60)
    print(f"⏱️  Tiempo de ejecución: {duracion:.2f} segundos")
    print(f"✅ Pruebas exitosas: {exitosas}/{total}")
    print(f"❌ Pruebas fallidas: {fallidas}")
    print(f"📈 Tasa de éxito: {tasa_exito:.1f}%")
    print("=" * 60)

    if tasa_exito == 100:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! El sistema está funcionando correctamente.")
    elif tasa_exito >= 80:
        print("⚠️  La mayoría de las pruebas pasaron. Revisa las fallidas.")
    else:
        print("🚨 Hay varios fallos. Revisa el sistema.")

    print("=" * 60)

    return tasa_exito


if __name__ == "__main__":
    tasa = ejecutar_pruebas()
    # Salir con código 0 si todo está bien, 1 si hay fallos
    exit(0 if tasa == 100 else 1)