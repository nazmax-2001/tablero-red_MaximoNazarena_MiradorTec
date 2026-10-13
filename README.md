# Tablero de mediciones de red

Página web estática con los indicadores de las mediciones de red, filtrable por piso.
Se publica gratis en GitHub Pages y se regenera sola cada vez que se actualiza el CSV.

## Estructura

```
data/mediciones.csv          ← los datos (reemplazar este archivo para actualizar)
build.py                     ← lee el CSV y genera docs/index.html
template.html                ← diseño del tablero (gráficos, tablas, filtro por piso)
vendor/plotly-basic.min.js   ← librería de gráficos; se incrusta en la página (funciona sin internet)
requirements.txt
.github/workflows/publicar.yml  ← regenera y publica automáticamente
```

## Publicarlo por primera vez

1. Crear una cuenta en github.com (si no tenés) y un repositorio **público** nuevo, por ejemplo `tablero-red`.
2. Subir todos estos archivos al repo (botón **Add file → Upload files**, arrastrando la carpeta completa,
   incluida la carpeta `.github`).
3. En el repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Ir a la pestaña **Actions**, elegir "Publicar tablero" y apretar **Run workflow**.
5. En 1–2 minutos el tablero queda en `https://<tu-usuario>.github.io/tablero-red/`.

> Si al subir por la web no aparece la carpeta `.github`, creá el archivo a mano:
> **Add file → Create new file**, nombre `.github/workflows/publicar.yml`, y pegá el contenido.

## Colgarlo en la intranet

Pegar este código en la página de la intranet (bloque HTML / iframe / "insertar código"):

```html
<iframe src="https://<tu-usuario>.github.io/tablero-red/"
        style="width:100%; height:1500px; border:0;"
        title="Tablero de mediciones de red"></iframe>
```

## Actualizar los datos

**Manual:** en el repo, entrar a `data/`, **Add file → Upload files**, subir el CSV nuevo con el mismo
nombre `mediciones.csv` y confirmar. El tablero se regenera solo en 1–2 minutos.

**Automático (opcional):** si las respuestas del formulario terminan en una planilla publicada como CSV
(por ejemplo Google Sheets → Archivo → Compartir → Publicar en la web → CSV), cargá ese link en
**Settings → Secrets and variables → Actions → Variables** con el nombre `CSV_URL` y descomentá el bloque
`schedule` en `.github/workflows/publicar.yml`. Desde ahí se actualiza todos los días sin intervención.

> Importante: el CSV tiene que tener las mismas columnas que el actual (`fecha`, `red`, `Piso`, `descarga`,
> `subida`, `ping`, `hora`, `pct_rendimiento`, …). Se aceptan números con coma decimal.

## Probarlo en tu computadora

```bash
pip install -r requirements.txt
python build.py
# abrir docs/index.html en el navegador
```
