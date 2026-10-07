#!/usr/bin/env python3
"""Convert all .txt cheatsheet files to styled HTML pages."""

import os
import html
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "html"
OUTPUT_DIR.mkdir(exist_ok=True)

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #1a1a2e;
    color: #e0e0e0;
    min-height: 100vh;
}
header {
    background: #16213e;
    border-bottom: 2px solid #0f3460;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    position: sticky;
    top: 0;
    z-index: 10;
}
header a {
    color: #e94560;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
header a:hover { text-decoration: underline; }
h1 {
    font-size: 1.4rem;
    font-weight: 700;
    color: #53d8fb;
    letter-spacing: 0.03em;
}
main {
    max-width: 960px;
    margin: 0 auto;
    padding: 24px;
}
pre {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 20px 24px;
    overflow-x: auto;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    font-size: 0.85rem;
    line-height: 1.65;
    white-space: pre-wrap;
    word-break: break-word;
}
.cmd  { color: #7ee787; }          /* $ shell commands */
.cmt  { color: #8b949e; }          /* # comments */
.hdr  { color: #f0c040; font-weight: bold; }  /* section headers */
.url  { color: #79c0ff; }
"""

INDEX_CSS = CSS + """
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
    margin-top: 8px;
}
.card {
    background: #16213e;
    border: 1px solid #0f3460;
    border-radius: 8px;
    padding: 14px 16px;
    text-decoration: none;
    color: #e0e0e0;
    transition: border-color 0.15s, background 0.15s;
    font-size: 0.9rem;
}
.card:hover {
    border-color: #53d8fb;
    background: #1e2a4a;
    color: #53d8fb;
}
.subtitle {
    color: #8b949e;
    font-size: 0.8rem;
    margin-top: 4px;
}
.section-title {
    color: #8b949e;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 28px 0 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid #21262d;
}
"""

def title_from_stem(stem: str) -> str:
    return stem.replace('_', ' ').title()

def convert_line(line: str) -> str:
    """Apply span classes to a single pre-escaped line."""
    stripped = line.lstrip()
    indent = line[:len(line) - len(stripped)]
    escaped = html.escape(line)
    escaped_stripped = html.escape(stripped)
    escaped_indent = html.escape(indent)

    if stripped.startswith('$ ') or stripped == '$':
        return f'<span class="cmd">{escaped}</span>'
    if stripped.startswith('# ') or stripped == '#':
        return f'<span class="cmt">{escaped}</span>'
    # Section header: non-indented line ending with ':' or all-caps word
    if not indent and stripped.endswith(':') and len(stripped) < 60 and '\n' not in stripped:
        return f'<span class="hdr">{escaped}</span>'
    return escaped

def txt_to_html(txt_path: Path) -> Path:
    stem = txt_path.stem
    title = title_from_stem(stem)
    text = txt_path.read_text(encoding='utf-8', errors='replace')

    lines = text.splitlines()
    body_lines = [convert_line(l) for l in lines]
    body = '\n'.join(body_lines)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <a href="../html/index.html">&#8592; Index</a>
  <h1>{html.escape(title)}</h1>
</header>
<main>
  <pre>{body}</pre>
</main>
</body>
</html>
"""
    out_path = OUTPUT_DIR / (stem + '.html')
    out_path.write_text(html_content, encoding='utf-8')
    return out_path

# Group files by rough category
CATEGORIES = {
    'Python': ['python_general', 'python_concurrency', 'python_pandas', 'python_numpy', 'python_pytest'],
    'Data / Serialization': ['database', 'database_DBT', 'big_query', 'Snowflake', 'snowflake',
                              'redis', 'parquet_pyarrow', 'avro', 'flatbuffers', 'protobuffers',
                              'msgpack', 'orc', 'json', 'toml', 'Markup_YAML_XML_etc'],
    'Cloud / Infra': ['aws', 'cloud_infra_system', 'docker', 'kubernetes', 'AirFlow', 'kafka'],
    'DevOps / CI': ['devops_sre', 'jenkins', 'github', 'git', 'svn', 'monitoring'],
    'Languages': ['cpp', 'cpp_17', 'rust', 'scala', 'lisp'],
    'Finance': ['finance_bonds', 'finance_futures', 'finance_options', 'finance_swap'],
    'Software Engineering': ['desgin_patterns', 'REST', 'agile', 'agile_scrum',
                              'company_culture_mircosoft', 'agile'],
    'AI / ML': ['ai', 'machine_learning_intro_coursera', 'machine_learning_adv_algo_coursera'],
    'Reference': ['speeds_CPU_Mem_Disk_NW', 'unix', 'todo'],
}

def build_index(txt_files: list[Path]) -> None:
    stems = {p.stem for p in txt_files}

    # Build category sections
    assigned = set()
    sections_html = ''
    for cat, members in CATEGORIES.items():
        cards = ''
        for m in members:
            if m in stems:
                cards += f'<a class="card" href="{html.escape(m)}.html">{html.escape(title_from_stem(m))}</a>\n'
                assigned.add(m)
        if cards:
            sections_html += f'<div class="section-title">{html.escape(cat)}</div>\n<div class="grid">{cards}</div>\n'

    # Uncategorized
    other = sorted(stems - assigned)
    if other:
        cards = ''.join(f'<a class="card" href="{html.escape(m)}.html">{html.escape(title_from_stem(m))}</a>\n' for m in other)
        sections_html += f'<div class="section-title">Other</div>\n<div class="grid">{cards}</div>\n'

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cheatsheets</title>
<style>{INDEX_CSS}</style>
</head>
<body>
<header>
  <h1>Cheatsheets</h1>
</header>
<main>
{sections_html}
</main>
</body>
</html>
"""
    (OUTPUT_DIR / 'index.html').write_text(index_html, encoding='utf-8')

def main():
    txt_files = sorted(BASE_DIR.glob('*.txt'))
    print(f"Converting {len(txt_files)} files...")
    for p in txt_files:
        out = txt_to_html(p)
        print(f"  {p.name} -> {out.relative_to(BASE_DIR)}")
    build_index(txt_files)
    print(f"\nDone. Open: {OUTPUT_DIR / 'index.html'}")

if __name__ == '__main__':
    main()
