import subprocess
from dotenv import load_dotenv

load_dotenv()

try:
    print("📤 Agregando cambios...")
    subprocess.run(["git", "add", "."], check=True)

    print("📝 Haciendo commit...")
    # check=False hace que no falle si no hay cambios
    subprocess.run(["git", "commit", "-m", "Actualización automática del index.html"], check=False)

    print("🚀 Subiendo a GitHub...")
    subprocess.run(["git", "push", "origin", "master"], check=True)

    print("✅ ¡Listo! El archivo se subió a GitHub automáticamente.")
except subprocess.CalledProcessError as e:
    print(f"❌ Error al subir a GitHub: {e}")