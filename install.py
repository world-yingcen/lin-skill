#!/usr/bin/env python3
"""Copy the standalone LIN skill without replacing an existing installation."""
import argparse
import os
from pathlib import Path
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description='安裝 LIN 網頁切版 Skill（複製，不覆蓋舊版）')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--tool', choices=('codex', 'claude'), help='要安裝的 AI 工具')
    group.add_argument('--target', type=Path, help='自訂 Skills 資料夾')
    parser.add_argument('--dry-run', action='store_true', help='只顯示位置，不寫入')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent / 'lin-frontend'
    if not (source / 'SKILL.md').is_file() or not (source / 'references').is_dir():
        parser.error('分享包不完整，請重新取得含 references 的整包資料夾')
    if args.target:
        base = args.target.expanduser().resolve()
    elif args.tool == 'codex' and os.environ.get('CODEX_HOME'):
        base = Path(os.environ['CODEX_HOME']).expanduser().resolve() / 'skills'
    else:
        base = Path.home() / ('.' + args.tool) / 'skills'
    target = base / source.name
    if target.exists() or target.is_symlink():
        print('未安裝：同名路徑已存在，沒有覆蓋。請先核對並移走舊版：%s' % target)
        return 1
    print('來源：%s' % source)
    print('安裝位置：%s' % target)
    if args.dry_run:
        print('試跑完成，未寫入檔案。')
        return 0
    base.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns('.DS_Store', '__pycache__', '*.pyc'))
    print('已安裝。請重新開啟對應 AI 工具，使用 lin-frontend。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
