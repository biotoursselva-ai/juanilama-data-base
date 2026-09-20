# Contexto del Proyecto: Registro de Herpetofauna

## Descripción
Sistema de automatización para el registro, procesamiento y publicación de datos sobre la herpetofauna de la Reserva Juanilama, San Carlos, Costa Rica.

## Arquitectura
Google Forms -> Google Sheets -> Google Apps Script -> GitHub -> GitHub Pages

## Archivos clave
- `index.html`: La página web (tarjetas de especies, filtros, búsqueda).
- `descargar_fotos.py`: Descarga fotos de Google Drive.
- `automatizar_html.py`: Detecta especies nuevas y modifica el HTML.
- `subir_a_github.py`: Sube cambios a GitHub.
- `maestro.py`: Script maestro (combina todo lo anterior).
- `test_sistema.py`: Pruebas de calidad.
- `credenciales.json`: Llave de acceso al bot (NO subir a GitHub).
- `.env`: Variables de entorno (token de GitHub, NO subir a GitHub).

## Apps Script (Google)
- Función principal: `alRecibirRespuesta(e)`.
- Se ejecuta automáticamente al enviar el formulario.
- Detecta especies nuevas, genera tarjetas HTML y modifica el `index.html` en GitHub.
- Usa el proxy `wsrv.nl` para convertir links de Drive en imágenes directas.
- Normaliza nombres para evitar duplicados.

## Reglas específicas del proyecto
- No modificar la función `normalizarNombre()` sin avisar.
- No cambiar los índices de las columnas del Sheets (C=Especie, D=Grupo, F=Comportamiento, G=Notas, I=Evidencia, M=Familia).
- No subir archivos grandes (>100 MB) a GitHub.
- Mantener el proxy `wsrv.nl` para las imágenes de Drive.

## Objetivo de Claude Code
Ayudar a mantener, mejorar y depurar el sistema. Priorizar la simplicidad y la seguridad.