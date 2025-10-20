Crear un ejecutable de la aplicación

Convierte esta aplicación Python en un .exe para Windows siguiendo estos pasos:

✅ Pasos rápidos

Instalar PyInstaller

pip install pyinstaller


Generar el ejecutable

pyinstaller --onefile main.py


--onefile → crea un solo archivo .exe

main.py → archivo principal

Opcional: --noconsole → oculta la consola en apps con GUI

Resultado: dist/main.exe

Incluir archivos adicionales

PyInstaller detecta automáticamente archivos importados (core, ui)

Para icono personalizado:

pyinstaller --onefile --icon=icono.ico main.py


Limpiar archivos innecesarios

Asegúrate de que .gitignore excluya __pycache__/ y .pyc

PyInstaller no incluirá archivos no usados

Distribuir

Comparte solo el .exe

No se requiere Python instalado en la máquina del usuario

💡 Tip: Antes de generar el .exe, prueba la app en la terminal para asegurarte de que todas las dependencias estén incluidas (requirements.txt ayuda a verificarlas).