#!/usr/bin/env python3
"""Install/update Lin-EVO and Miffy-EVO together, or one selected skill."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MANIFEST = '.Lin-EVO-install.json'
SKILLS = ('Lin-EVO', 'Miffy-EVO')
SOURCE_CONFIG = 'skill-sources.json'
# Old names are only accepted for migration from previously managed installs.
LEGACY = {'Lin-EVO': 'lin-frontend', 'Miffy-EVO': 'miffy'}


def manifest_name(skill):
    if skill not in SKILLS:
        raise RuntimeError('不支援的 Skill：' + skill)
    return '.' + skill + '-install.json'
REMOTES = {'https://github.com/world-yingcen/lin-skill.git',
           'https://github.com/world-yingcen/lin-skill',
           'git@github.com:world-yingcen/lin-skill.git'}
MIFFY_REMOTES = {'https://github.com/world-yingcen/Miffy-EVO.git',
                 'https://github.com/world-yingcen/Miffy-EVO',
                 'git@github.com:world-yingcen/Miffy-EVO.git'}
REMOTE_BY_SKILL = {'Lin-EVO': REMOTES, 'Miffy-EVO': MIFFY_REMOTES}


def source_path(root, skill):
    """Resolve one Skill source, allowing a local split-repo mapping."""
    manifest_name(skill)
    configured = {}
    config = root / SOURCE_CONFIG
    if config.is_file():
        configured = json.loads(config.read_text())
        if not isinstance(configured, dict):
            raise RuntimeError(SOURCE_CONFIG + ' 必須是 JSON 物件。')
    value = configured.get(skill, skill)
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(SOURCE_CONFIG + ' 的 ' + skill + ' 路徑無效。')
    path = Path(value).expanduser()
    return (path if path.is_absolute() else root / path).resolve()


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


def checked_manifest(root, base, adopt=False, skill='Lin-EVO'):
    target = base / skill
    record = base / manifest_name(skill)
    info = json.loads(record.read_text()) if record.exists() else None
    desired_source = source_path(root, skill)
    if info and Path(info.get('source', '')).resolve() != root.resolve():
        raise RuntimeError('安裝紀錄屬於其他來源，未覆蓋。')
    recorded_source = Path(info.get('skill_path', root / skill)).resolve() if info else None
    if target.is_symlink():
        if not target.is_dir():
            raise RuntimeError('Skill 捷徑失效或指向其他來源，保留現況。')
        if info and info.get('mode') == 'link' and target.resolve() == recorded_source:
            return info
        if not info and adopt and target.resolve() == desired_source:
            return None
        raise RuntimeError('Skill 捷徑與安裝紀錄不符；未管理的同來源捷徑可用 --adopt 接管。')
    if info and info.get('mode') == 'link' and target.exists():
        raise RuntimeError('安裝紀錄為捷徑，但目標已被替換，保留現況。')
    if target.exists():
        actual = hashes(target)
        if info:
            if actual != info.get('hashes'):
                raise RuntimeError('本機 Skill 有修改，保留現況，請先核對差異。')
        elif not adopt or actual != hashes(desired_source):
            raise RuntimeError('既有 Skill 未受管理；僅能用 --adopt 接管與來源完全一致的副本。')
    return info


def update_source(root, allowed_remotes=REMOTES):
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
        raise RuntimeError('必須使用獨立 lin-skill clone，不在案件或上層 repo 更新。')
    if git(root, 'remote', 'get-url', 'origin') not in allowed_remotes:
        raise RuntimeError('origin 不是指定的 Skill repo，未更新。')
    if git(root, 'branch', '--show-current') != 'main':
        raise RuntimeError('來源不在 main，保留目前分支。')
    if git(root, 'status', '--porcelain'):
        raise RuntimeError('來源有未提交修改，未更新；不 reset、stash 或覆蓋。')
    git(root, 'fetch', 'origin', 'main')
    ahead = git(root, 'rev-list', '--count', 'origin/main..HEAD')
    if ahead != '0':
        raise RuntimeError('來源含本地提交或分歧，保留現況，未合併。')
    git(root, 'merge', '--ff-only', 'origin/main')


def install(root, base, adopt=False, dry_run=False, skill='Lin-EVO', mode=None):
    manifest_name(skill)
    source = source_path(root, skill)
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
        record = {'source': str(root.resolve()), 'skill_path': str(source), 'mode': mode}
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


def migrate_legacy(root, base, selected, dry_run=False):
    plans = []
    for skill in selected:
        old = base / LEGACY[skill]
        old_record = base / ('.' + LEGACY[skill] + '-install.json')
        if not (old.exists() or old.is_symlink() or old_record.exists()):
            continue
        target = base / skill
        record = base / manifest_name(skill)
        if target.exists() or target.is_symlink() or record.exists():
            raise RuntimeError('新舊 Skill 同時存在，保留現況：' + skill)
        if not old_record.is_file():
            raise RuntimeError('舊 Skill 未受管理，保留現況：' + str(old))
        info = json.loads(old_record.read_text())
        if Path(info.get('source', '')).resolve() != root.resolve():
            raise RuntimeError('舊安裝屬於其他來源，未改名。')
        if old.is_symlink():
            if info.get('mode') != 'link' or old.resolve() != (root / LEGACY[skill]).resolve():
                raise RuntimeError('舊捷徑指向其他來源，未改名。')
        elif not old.is_dir() or hashes(old) != info.get('hashes'):
            raise RuntimeError('舊副本有修改或缺漏，保留現況：' + str(old))
        if not (source_path(root, skill) / 'SKILL.md').is_file():
            raise RuntimeError('改名後來源缺漏：' + skill)
        plans.append((skill, old, old_record, target, record, info))
    if dry_run:
        for skill, *_ in plans:
            print('待遷移：' + LEGACY[skill] + ' → ' + skill)
        return
    for skill, old, old_record, target, record, info in plans:
        old.rename(target)
        try:
            if info.get('mode') == 'link':
                target.unlink()
                target.symlink_to(source_path(root, skill).resolve(), target_is_directory=True)
            old_record.rename(record)
        except Exception:
            if target.is_symlink():
                target.unlink()
                old.symlink_to(root / LEGACY[skill], target_is_directory=True)
            elif target.exists():
                target.rename(old)
            raise
        print('已遷移：' + LEGACY[skill] + ' → ' + skill)


def main():
    parser = argparse.ArgumentParser(description='Lin-EVO／Miffy-EVO 安裝與安全更新（不保留舊版備份）')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--tool', choices=['codex', 'claude'])
    group.add_argument('--target', type=Path)
    parser.add_argument('--skill', choices=(*SKILLS, *LEGACY.values()), help='只同步指定 Skill；未指定時一起同步 Lin-EVO 與 Miffy-EVO')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--link', dest='mode', action='store_const', const='link', help='直接連到 Git 專案，不建立副本')
    modes.add_argument('--copy', dest='mode', action='store_const', const='copy', help='使用獨立副本')
    parser.add_argument('--adopt', action='store_true', help='接管與來源完全相同的舊副本')
    parser.add_argument('--update', action='store_true', help='檢查指定遠端 main 並 fast-forward，再同步')
    parser.add_argument('--status', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.skill in LEGACY.values():
        args.skill = next(name for name, old in LEGACY.items() if old == args.skill)
    selected = (args.skill,) if args.skill else SKILLS
    root = Path(__file__).resolve().parent
    base = args.target.expanduser().absolute() if args.target else (
        Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
        if args.tool == 'codex' else Path.home() / '.claude/skills')
    try:
        migrate_legacy(root, base, selected, dry_run=args.dry_run or args.status)
        if args.status:
            for skill in selected:
                info = checked_manifest(root, base, skill=skill)
                if not info or not (base / skill).is_dir():
                    raise RuntimeError(skill + ' 未安裝或缺少管理紀錄。')
                if hashes(base / skill) != hashes(source_path(root, skill)):
                    raise RuntimeError(skill + ' 來源已變更，副本待同步（尚未檢查遠端）。')
            print('來源／安裝內容一致（捷徑直接讀來源）；此狀態不代表已檢查遠端最新版本。')
        elif args.update and not args.dry_run:
            # Existing Lin-EVO-only installations can gain Miffy-EVO on their next update.
            records = [checked_manifest(root, base, skill=skill) for skill in selected]
            if not any(records):
                raise RuntimeError('先完成安裝，再使用 --update。')
            updated = set()
            for skill in selected:
                source = source_path(root, skill)
                repo = (root.resolve() if source == (root / skill).resolve()
                        else Path(git(source, 'rev-parse', '--show-toplevel')).resolve())
                if repo in updated:
                    continue
                if repo == root.resolve():
                    update_source(repo)
                else:
                    update_source(repo, REMOTE_BY_SKILL[skill])
                updated.add(repo)
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
                source = source_path(root, skill)
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
