#!/usr/bin/env python3
"""
Descarga todas las imágenes, GIFs y videos publicados por un usuario de X.
Requisito: pip install -U gallery-dl
"""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Descarga el multimedia de un usuario de X")
    p.add_argument("usuario", help="Nombre de usuario, con o sin @")
    p.add_argument("-o", "--salida", default="descargas_x", help="Carpeta de destino")

    auth = p.add_mutually_exclusive_group(required=True)
    auth.add_argument(
        "--navegador", help="Leer cookies de: firefox, chrome, edge, brave..."
    )
    auth.add_argument(
        "--cookies", help="Ruta a un archivo cookies.txt (formato Netscape)"
    )

    p.add_argument("--solo", choices=["imagenes", "videos"], help="Filtrar por tipo")
    p.add_argument(
        "--metadatos", action="store_true", help="Guardar un .json por cada archivo"
    )
    p.add_argument("--pausa", type=float, default=1.0, help="Segundos entre peticiones")
    args = p.parse_args()

    usuario = args.usuario.lstrip("@").strip()
    carpeta = Path(args.salida).expanduser() / usuario
    carpeta.mkdir(parents=True, exist_ok=True)

    cmd = [
        "gallery-dl",
        "-D",
        str(carpeta),
        "-f",
        "{date:%Y-%m-%d}_{tweet_id}_{num}.{extension}",
        "--download-archive",
        str(carpeta / "archivo.sqlite3"),
        "--sleep-request",
        str(args.pausa),
    ]

    if args.navegador:
        cmd += ["--cookies-from-browser", args.navegador]
    else:
        cmd += ["--cookies", args.cookies]

    if args.solo == "imagenes":
        cmd += ["--filter", "extension in ('jpg', 'jpeg', 'png', 'webp')"]
    elif args.solo == "videos":
        cmd += ["--filter", "extension == 'mp4'"]

    if args.metadatos:
        cmd.append("--write-metadata")

    cmd.append(f"https://x.com/{usuario}/media")

    print(f"Descargando multimedia de @{usuario} en {carpeta.resolve()}\n")
    resultado = subprocess.run(cmd)

    if resultado.returncode == 0:
        print("\n✔ Descarga completada.")
    else:
        print(
            f"\n✘ gallery-dl terminó con código {resultado.returncode}. "
            "Revisa las cookies y vuelve a ejecutar; lo ya descargado se omitirá."
        )
    sys.exit(resultado.returncode)


if __name__ == "__main__":
    main()
