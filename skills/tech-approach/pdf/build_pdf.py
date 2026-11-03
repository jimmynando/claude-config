#!/usr/bin/env python3
"""Build a client's technical-approach PDF in the red SENAI-SP layout.

Usage:
    build_pdf.py <source.html> [--out <file.pdf>] [--force]

The source is an HTML fragment (no <html> or <head>) that starts with a
metadata comment:

    <!--
    client: Semax
    version: 1.0
    -->

Optional metadata: brand (default "SENAI-SP"), program (default "Jornada de IA"),
year (default: this year).

The PDF goes next to the source as <source-name>-v<version>.pdf. An existing
version is never overwritten unless --force is given, so old versions stay intact.

Needs LibreOffice (soffice) and the Carlito font. pdftotext (poppler) is optional
and only used for the final check.
"""
import argparse
import datetime
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARGIN = "2cm"
RED = "#cc1414"
RED_TINT = "#fdf0f0"
GREY_TINT = "#f3f5f8"


def read_source(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\s*<!--(.*?)-->", text, re.S)
    if not match:
        sys.exit(f"{path} must start with a <!-- client: ... version: ... --> comment")
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip().lower()] = value.strip()
    for key in ("client", "version"):
        if not meta.get(key):
            sys.exit(f"{path}: metadata is missing '{key}'")
    meta.setdefault("brand", "SENAI-SP")
    meta.setdefault("program", "Jornada de IA")
    meta.setdefault("year", str(datetime.date.today().year))
    return meta, text[match.end():]


def add_layout_attributes(body):
    """LibreOffice ignores some CSS, so colours, padding and page breaks also go in as HTML."""
    body = re.sub(
        r'(<table class="callout")>(.*?</table>)',
        lambda m: f'{m.group(1)} width="100%" cellpadding="9">' + m.group(2).replace("<td", f'<td bgcolor="{RED_TINT}"'),
        body, flags=re.S)
    body = body.replace("<table>", '<table width="100%" cellpadding="5">')
    body = re.sub(r"<th(?=[\s>])", f'<th bgcolor="{RED}"', body)
    body = body.replace('<td class="label"', f'<td class="label" bgcolor="{GREY_TINT}"')
    body = re.sub(r'<(h[1-3]) class="new-page">', r'<\1 style="page-break-before: always">', body)
    return body


def even_margins(odt_in, odt_out):
    """Give every page the same margin on all four sides."""
    def fix(tag):
        return re.sub(r'fo:margin-(top|bottom|left|right)="[^"]*"',
                      lambda m: f'fo:margin-{m.group(1)}="{MARGIN}"', tag.group(0))

    with zipfile.ZipFile(odt_in) as zin, zipfile.ZipFile(odt_out, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "styles.xml":
                xml = re.sub(r"<style:page-layout-properties[^>]*>", fix, data.decode("utf-8"))
                data = xml.encode("utf-8")
            zout.writestr(item, data)


def soffice(args, workdir):
    # A private profile keeps this from clashing with a LibreOffice window you have open.
    profile = (workdir / "profile").as_uri()
    result = subprocess.run(["soffice", f"-env:UserInstallation={profile}", "--headless", *args],
                            cwd=workdir, capture_output=True, text=True, timeout=180)
    return result.stdout + result.stderr


def check_pages(pdf, brand):
    if not shutil.which("pdftotext"):
        return "skipped page check (pdftotext not installed)"
    text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
    pages = [p for p in text.split("\f") if p.strip()]
    missing = [str(i) for i, page in enumerate(pages, 1) if page.count(brand) < 2]
    if missing:
        return f"{len(pages)} pages; header or footer MISSING on page(s) {', '.join(missing)}"
    return f"{len(pages)} pages; header and footer on every page"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--force", action="store_true", help="overwrite an existing PDF")
    args = parser.parse_args()

    if not shutil.which("soffice"):
        sys.exit("LibreOffice (soffice) is not installed")

    source = args.source.expanduser().resolve()
    meta, body = read_source(source)
    out = (args.out.expanduser() if args.out
           else source.with_name(f"{source.stem}-v{meta['version']}.pdf")).resolve()
    if out.exists() and not args.force:
        sys.exit(f"{out} already exists; bump the version in {source.name}, or pass --force")

    page = (HERE / "layout.html").read_text(encoding="utf-8")
    for key, value in meta.items():
        page = page.replace("{{" + key + "}}", value)
    page = page.replace("{{body}}", add_layout_attributes(body))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "doc.html").write_text(page, encoding="utf-8")
        # Going through .odt is deliberate: HTML straight to PDF drops the header on even pages.
        log = soffice(["--infilter=HTML (StarWriter)", "--convert-to", "odt:writer8", "doc.html"], tmp)
        if not (tmp / "doc.odt").exists():
            sys.exit(f"HTML to ODT conversion failed:\n{log}")
        (tmp / "final").mkdir()
        even_margins(tmp / "doc.odt", tmp / "final" / "doc.odt")
        log = soffice(["--convert-to", "pdf:writer_pdf_Export", "--outdir", str(tmp), "final/doc.odt"], tmp)
        if not (tmp / "doc.pdf").exists():
            sys.exit(f"ODT to PDF conversion failed:\n{log}")
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(tmp / "doc.pdf", out)

    print(f"wrote {out}")
    print(check_pages(out, meta["brand"]))


if __name__ == "__main__":
    main()
