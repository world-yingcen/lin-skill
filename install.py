#!/usr/bin/env python3
"""Install/update LIN and Miffy together, or one selected skill."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MANIFEST = '.lin-frontend-install.json'
SKILLS = ('lin-frontend', 'miffy')


def manifest_name(skill):
    if skill not in SKILLS:
        raise RuntimeError('不支援的 Skill：' + skill)
    return '.' + skill + '-install.json'
REMOTES = {'https://github.com/world-yingcen/lin-skill.git',
           'https://github.com/world-yingcen/lin-skill',
           'git@github.com:world-yingcen/lin-skill.git'}


def hashes(root):
    result = {}
    for item in sorted(root.rglob('*')):
        rel = item.relative_to(root)
        if any(part in {'.DS_Store', '__pycache__'} for part in rel.parts) or item.suffix == '.pyc':
            continue
        if item.is_symlink():
            raise RuntimeError('Skill 內含未支援的捷徑：' + str(rel))
        if item.is_file():
            result[rel.as_posix()] = hashlib.sha256(item.read_bytes()).hexdigest()
    return result


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True,
                          capture_output=True, text=True, timeout=60).stdout.strip()


def checked_manifest(root, base, adopt=False, skill='lin-frontend'):
    target = base / skill
    record = base / manifest_name(skill)
    info = json.loads(record.read_text()) if record.exists() else None
    if info and Path(info.get('source', '')).resolve() != root.resolve():
        raise RuntimeError('安裝紀錄屬於其他來源，未覆蓋。')
    if target.is_symlink():
        if target.resolve() != (root / skill).resolve() or not target.is_dir():
            raise RuntimeError('Skill 捷徑失效或指向其他來源，保留現況。')
        if info and info.get('mode') == 'link':
            return info
        if not info and adopt:
            return None
        raise RuntimeError('Skill 捷徑與安裝紀錄不符；未管理的同來源捷徑可用 --adopt 接管。')
    if info and info.get('mode') == 'link' and target.exists():
        raise RuntimeError('安裝紀錄為捷徑，但目標已被替換，保留現況。')
    if target.exists():
        actual = hashes(target)
        if info:
            if actual != info.get('hashes'):
                raise RuntimeError('本機 Skill 有修改，保留現況，請先核對差異。')
        elif not adopt or actual != hashes(root / skill):
            raise RuntimeError('既有 Skill 未受管理；僅能用 --adopt 接管與來源完全一致的副本。')
    return info


def update_source(root):
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
        raise RuntimeError('必須使用獨立 lin-skill clone，不在案件或上層 repo 更新。')
    if git(root, 'remote', 'get-url', 'origin') not in REMOTES:
        raise RuntimeError('origin 不是指定的 LIN repo，未更新。')
    if git(root, 'branch', '--show-current') != 'main':
        raise RuntimeError('來源不在 main，保留目前分支。')
    if git(root, 'status', '--porcelain'):
        raise RuntimeError('來源有未提交修改，未更新；不 reset、stash 或覆蓋。')
    git(root, 'fetch', 'origin', 'main')
    ahead = git(root, 'rev-list', '--count', 'origin/main..HEAD')
    if ahead != '0':
        raise RuntimeError('來源含本地提交或分歧，保留現況，未合併。')
    git(root, 'merge', '--ff-only', 'origin/main')


def install(root, base, adopt=False, dry_run=False, skill='lin-frontend', mode=None):
    manifest_name(skill)
    source = root / skill
    if not (source / 'SKILL.md').is_file() or not (source / 'references').is_dir():
        raise RuntimeError('來源缺少完整 Skill。')
    if base.resolve() in {root.resolve(), source.resolve()} or source.resolve() in base.resolve().parents:
        raise RuntimeError('安裝目標不可位於 Skill 來源內。')
    info = checked_manifest(root, base, adopt, skill)
    mode = mode or (info.get('mode', 'copy') if info else 'copy')
    if mode not in {'copy', 'link'}:
        raise RuntimeError('不支援的安裝模式。')
    desired = hashes(source)
    if dry_run:
        print('試跑：' + mode + ' ' + skill + ' 至 ' + str(base))
        return
    base.mkdir(parents=True, exist_ok=True)
    target = base / skill
    # Build and verify before swapping. Rollback data exists only during this operation.
    stage = Path(tempfile.mkdtemp(prefix='.lin-install-', dir=str(base)))
    old = stage / 'previous'
    completed = False
    try:
        if mode == 'link':
            (stage / 'new').symlink_to(source.resolve(), target_is_directory=True)
        else:
            shutil.copytree(source, stage / 'new', ignore=shutil.ignore_patterns('.DS_Store', '__pycache__', '*.pyc'))
        if hashes(stage / 'new') != desired:
            raise RuntimeError('來源在複製期間變更，未替換。')
        record = {'source': str(root.resolve()), 'mode': mode}
        if mode == 'copy':
            record['hashes'] = desired
        (stage / 'manifest').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
        checked_manifest(root, base, adopt, skill)
        if target.exists() or target.is_symlink():
            target.rename(old)
        try:
            (stage / 'new').rename(target)
            os.replace(stage / 'manifest', base / manifest_name(skill))
            completed = True
        except Exception:
            if target.is_symlink():
                target.unlink()
            elif target.exists():
                shutil.rmtree(target)
            if old.exists():
                old.rename(target)
            raise
    finally:
        if completed or not old.exists():
            shutil.rmtree(stage)
        else:
            print('回復未完成，保留復原資料：' + str(old), file=sys.stderr)
    print(('已連結：' if mode == 'link' else '已同步：') + str(target) + '；下次呼叫請重新讀取 Skill。')


def main():
    parser = argparse.ArgumentParser(description='LIN／Miffy 安裝與安全更新（不保留舊版備份）')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--tool', choices=['codex', 'claude'])
    group.add_argument('--target', type=Path)
    parser.add_argument('--skill', choices=SKILLS, help='只同步指定 Skill；未指定時一起同步 LIN 與 Miffy')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--link', dest='mode', action='store_const', const='link', help='直接連到 Git 專案，不建立副本')
    modes.add_argument('--copy', dest='mode', action='store_const', const='copy', help='使用獨立副本')
    parser.add_argument('--adopt', action='store_true', help='接管與來源完全相同的舊副本')
    parser.add_argument('--update', action='store_true', help='檢查指定遠端 main 並 fast-forward，再同步')
    parser.add_argument('--status', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    selected = (args.skill,) if args.skill else SKILLS
    root = Path(__file__).resolve().parent
    base = args.target.expanduser().absolute() if args.target else (
        Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
        if args.tool == 'codex' else Path.home() / '.claude/skills')
    try:
        if args.status:
            for skill in selected:
                info = checked_manifest(root, base, skill=skill)
                if not info or not (base / skill).is_dir():
                    raise RuntimeError(skill + ' 未安裝或缺少管理紀錄。')
                if hashes(base / skill) != hashes(root / skill):
                    raise RuntimeError(skill + ' 來源已變更，副本待同步（尚未檢查遠端）。')
            print('來源／安裝內容一致（捷徑直接讀來源）；此狀態不代表已檢查遠端最新版本。')
        elif args.update and not args.dry_run:
            # Existing LIN-only installations can gain Miffy on their next update.
            records = [checked_manifest(root, base, skill=skill) for skill in selected]
            if not any(records):
                raise RuntimeError('先完成安裝，再使用 --update。')
            update_source(root)
            # Run the updated installer, even if source HEAD did not change.
            command = [sys.executable, str(root / 'install.py'), '--target', str(base)]
            if args.skill:
                command.extend(['--skill', args.skill])
            if args.mode:
                command.append('--' + args.mode)
            return subprocess.call(command)
        else:
            # Check every selected copy before replacing any of them.
            for skill in selected:
                source = root / skill
                if not (source / 'SKILL.md').is_file() or not (source / 'references').is_dir():
                    raise RuntimeError(skill + ' 來源缺少完整 Skill。')
                checked_manifest(root, base, args.adopt, skill)
            for skill in selected:
                info = checked_manifest(root, base, args.adopt, skill)
                mode = args.mode or (info.get('mode', 'copy') if info else 'link')
                install(root, base, args.adopt, args.dry_run, skill, mode)
        return 0
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as error:
        print('未完成：' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
