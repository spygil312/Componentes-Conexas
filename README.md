# Componentes conexas

Aplicación educativa e interactiva para explorar grafos y comprender cómo se determinan sus componentes conexas. Permite construir un grafo manualmente o generar uno aleatorio, visualizar su matriz de adyacencia y seguir paso a paso el proceso de análisis.

## Probar la aplicación

### Versión web

Usa la aplicación directamente desde el navegador, sin instalar nada:

**[Abrir Componentes conexas en GitHub Pages](https://spygil312.github.io/Componentes-Conexas/)**

### Aplicación para Windows

Descarga el ejecutable empaquetado desde la última versión publicada:

**[Descargar Componentes_Conexas.exe](https://github.com/spygil312/Componentes-Conexas/releases/latest/download/Componentes_Conexas.exe)**

También puedes consultar todas las versiones en [GitHub Releases](https://github.com/spygil312/Componentes-Conexas/releases).

## Funcionalidades

- Elegir el número de nodos del grafo.
- Crear un grafo manualmente o generar uno aleatorio.
- Visualizar y editar el grafo y su matriz de adyacencia.
- Identificar las componentes conexas y revisar el proceso paso a paso.
- Consultar el historial de las acciones realizadas.

## Ejecutar la versión de Python

Se requiere Python y NumPy. Desde una terminal, entra en la carpeta `Python` y ejecuta:

```powershell
python -m pip install numpy
python Componentes_Conexas.py
```

Para reconstruir el ejecutable, instala PyInstaller y, desde esa misma carpeta, ejecuta:

```powershell
python -m pip install pyinstaller
python -m PyInstaller Componentes_Conexas.spec --distpath .
```
