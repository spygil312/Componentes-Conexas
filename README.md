# Componentes conexas

Aplicación interactiva para construir grafos, consultar su matriz de adyacencia y encontrar sus componentes conexas.

## Usar en el navegador

La página se publica con GitHub Pages desde la carpeta `HTML`:

<https://spygil312.github.io/Componentes-Conexas/>

El flujo de GitHub Actions la despliega al subir cambios a la rama `main`. En GitHub, configura **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Descargar para Windows

Descarga el ejecutable desde la sección **Releases**:
<https://github.com/spygil312/Componentes-Conexas/releases/download/v1.0.0/Componentes_Conexas.exe>

Para publicar o actualizarlo, crea una Release en GitHub, adjunta `Componentes_Conexas.exe` y publícala. El archivo está excluido del repositorio mediante `.gitignore`; se puede adjuntar a la Release directamente desde GitHub.

## Ejecutar desde Python

Se requiere Python y NumPy. Desde la carpeta `Python`, ejecuta:

```powershell
python -m pip install numpy
python Componentes_Conexas.py
```

Para reconstruir el ejecutable con PyInstaller instalado, desde esa misma carpeta:

```powershell
python -m PyInstaller Componentes_Conexas.spec --distpath .
```
