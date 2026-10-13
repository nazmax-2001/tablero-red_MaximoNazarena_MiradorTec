"""
Genera el tablero de mediciones de red como una página HTML estática.

Uso:
    python build.py

Lee data/mediciones.csv (o la URL en la variable de entorno CSV_URL, si existe),
limpia los números con coma decimal y escribe docs/index.html usando template.html.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

BASE = Path(__file__).parent
CSV_LOCAL = BASE / "data" / "mediciones.csv"
TEMPLATE = BASE / "template.html"
SALIDA = BASE / "docs" / "index.html"
PLOTLY = BASE / "vendor" / "plotly-basic.min.js"  # librería de gráficos, incluida en la página

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def a_numero(serie: pd.Series) -> pd.Series:
    """Convierte '41,7' -> 41.7 (acepta también números ya numéricos)."""
    return pd.to_numeric(serie.astype(str).str.replace(",", ".", regex=False), errors="coerce")


def cargar() -> pd.DataFrame:
    origen = os.environ.get("CSV_URL") or CSV_LOCAL
    df = pd.read_csv(origen, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]

    for col in ["descarga", "subida", "ping", "pct_rendimiento"]:
        df[col] = a_numero(df[col])

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha", "descarga"])
    return df


def main() -> None:
    df = cargar()

    registros = pd.DataFrame({
        "red": df["red"],
        "piso": df["Piso"],
        "descarga": df["descarga"].round(2),
        "subida": df["subida"].round(2),
        "ping": df["ping"],
        "pct": df["pct_rendimiento"].round(2),
        "hora": df["hora"].astype(int),
        "mes": df["fecha"].dt.month,
        "anio": df["fecha"].dt.year,
    }).to_dict(orient="records")

    ahora = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    meta = {
        "actualizado": ahora.strftime("%d/%m/%Y %H:%M"),
        "desde": df["fecha"].min().strftime("%d/%m/%Y"),
        "hasta": df["fecha"].max().strftime("%d/%m/%Y"),
        "meses": MESES,
    }

    html = TEMPLATE.read_text(encoding="utf-8")
    # Plotly va incrustado para que el tablero funcione sin depender de internet ni de un CDN
    html = html.replace("__PLOTLY__", PLOTLY.read_text(encoding="utf-8").replace("</script>", "<\\/script>"))
    html = html.replace("__DATOS__", json.dumps(registros, ensure_ascii=False))
    html = html.replace("__META__", json.dumps(meta, ensure_ascii=False))

    SALIDA.parent.mkdir(exist_ok=True)
    SALIDA.write_text(html, encoding="utf-8")
    print(f"Tablero generado: {SALIDA} ({len(registros)} mediciones)")


if __name__ == "__main__":
    main()
