#!/usr/bin/env python3
"""Build a standalone LIN upload with its complete verified starter."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
IGNORE = shutil.ignore_patterns('.git', '.DS_Store', 'agents', '__pycache__', '*.pyc', 'node_modules')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def validate_baseline(source):
    base = source / 'assets/evo-starter'
    record = json.loads((base / 'SOURCE.json').read_text())
    tree = base / '06-切版'
    required = {'index.html', 'js/main.js', 'image/.gitkeep', 'assets/page-composer-state.json', 'scss/_common.scss', 'scss/_header.scss', 'scss/_footer.scss', 'scss/_index.scss', 'scss/evomni-root.scss'}
    actual = {p.relative_to(tree).as_posix() for p in tree.rglob('*') if p.is_file() and p.name != '.DS_Store'}
    if not required <= actual or actual != set(record['files']):
        raise ValueError('基底缺檔或檔案清單不符')
    for rel, expected in record['files'].items():
        if digest(tree / rel) != expected:
            raise ValueError('基底雜湊不符：' + rel)

def validate_links(package):
    if list(package.rglob('SKILL.md')) != [package / 'SKILL.md']:
        raise ValueError('必須只有根目錄一份 SKILL.md')
    for p in package.rglob('*.md'):
        for href in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if href.startswith(('http:', 'https:', '#', 'mailto:')):
                continue
            target = (p.parent / unquote(href.split('#')[0])).resolve()
            if not target.is_relative_to(package.resolve()) or not target.exists():
                raise ValueError(f'參考連結缺漏：{p.relative_to(package)} -> {href}')

def build(source, output):
    source, output = source.resolve(), output.resolve()
    if output.exists():
        raise ValueError('輸出已存在，不覆蓋：' + str(output))
    if output.is_relative_to(source):
        raise ValueError('輸出不可放在 Skill 來源內')
    validate_baseline(source)
    commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = bool(subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain', '--', '.'], text=True).strip())
    with tempfile.TemporaryDirectory() as temp:
        pkg = Path(temp) / 'Lin-EVO'
        res = pkg / 'resources/Lin-EVO'
        shutil.copytree(source, res, ignore=IGNORE)
        (res / 'SKILL.md').rename(res / 'GUIDE.md')
        for p in res.rglob('*.md'):
            text = re.sub(r'\[([^\]]+)\]\((?:\.\./)+Miffy-EVO/[^)]+\)', r'\1（請讀另行啟用的 Miffy-EVO 對應指南，不使用跨包相對路徑）', p.read_text())
            p.write_text(text)
        shutil.copyfile(ROOT / 'scripts/templates/Lin-EVO-Claude.md', pkg / 'SKILL.md')
        validate_links(pkg)
        validate_baseline(res)
        hashes = {p.relative_to(pkg).as_posix(): digest(p) for p in sorted(pkg.rglob('*')) if p.is_file()}
        (pkg / 'SOURCE.json').write_text(json.dumps({'built_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(), 'source': str(source), 'commit': commit, 'working_tree_modified': dirty, 'files': hashes}, ensure_ascii=False, indent=2) + '\n')
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(pkg.rglob('*')):
                if p.is_file():
                    z.write(p, p.relative_to(pkg.parent))
        with zipfile.ZipFile(output) as z:
            if z.testzip() is not None:
                raise ValueError('ZIP 完整性失敗')
            for rel, expected in hashes.items():
                if hashlib.sha256(z.read('Lin-EVO/' + rel)).hexdigest() != expected:
                    raise ValueError('ZIP 雜湊不符：' + rel)
    print('已建立並驗證：' + str(output))
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'Lin-EVO')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        build(args.source.expanduser(), args.output.expanduser())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'打包未完成：{error}\n')
