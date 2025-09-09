

import argparse
import shutil
from pathlib import Path
import sys
from typing import Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли з SRC у DEST, "
                    "сортує їх у піддиректорії за розширеннями."
    )
    parser.add_argument("src", type=Path, help="Шлях до вихідної директорії (SRC)")
    parser.add_argument(
        "dest",
        nargs="?",
        default=Path("dist"),
        type=Path,
        help="Шлях до директорії призначення (DEST). За замовчуванням: dist",
    )
    return parser.parse_args()


def safe_mkdir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f"[PERMISSION] Немає прав для створення директорії: {path}\n  → {e}", file=sys.stderr)
        raise
    except OSError as e:
        print(f"[OSERROR] Не вдалося створити директорію: {path}\n  → {e}", file=sys.stderr)
        raise


def unique_destination(dest_dir: Path, filename: str) -> Path:
    """
    Генерує унікальне ім'я в папці призначення, якщо такий файл вже існує.
    file.ext -> file.ext, file_1.ext, file_2.ext, ...
    """
    dest_path = dest_dir / filename
    if not dest_path.exists():
        return dest_path

    stem = dest_path.stem
    suffix = dest_path.suffix
    counter = 1
    while True:
        candidate = dest_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def copy_file_to_ext_bucket(file_path: Path, dest_root: Path) -> Optional[Path]:
    """
    Копіює один файл до підпапки за розширенням.
    Повертає шлях до створеного файлу або None у разі помилки.
    """
    # Розширення без крапки; якщо немає — використовуємо "_noext"
    ext = file_path.suffix.lower().lstrip(".") or "_noext"
    bucket_dir = dest_root / ext
    try:
        safe_mkdir(bucket_dir)
        target = unique_destination(bucket_dir, file_path.name)
        shutil.copy2(file_path, target)
        print(f"[OK] {file_path}  →  {target}")
        return target
    except PermissionError as e:
        print(f"[PERMISSION] Немає доступу до файлу: {file_path}\n  → {e}", file=sys.stderr)
    except FileNotFoundError as e:
        print(f"[MISSING] Файл не знайдено (можливо, видалено під час обробки): {file_path}\n  → {e}", file=sys.stderr)
    except OSError as e:
        print(f"[OSERROR] Помилка під час копіювання {file_path}\n  → {e}", file=sys.stderr)
    except Exception as e:
        print(f"[UNKNOWN] Несподівана помилка з {file_path}\n  → {e}", file=sys.stderr)
    return None


def recurse_and_copy(src_dir: Path, dest_root: Path) -> None:
    """
    Рекурсивно проходить по src_dir.
    - Якщо елемент — директорія: рекурсивний виклик.
    - Якщо файл — копіюємо у відро (bucket) за розширенням у dest_root.
    Пропускаємо симлінки на директорії, щоб уникнути циклів.
    """
    try:
        entries = list(src_dir.iterdir())
    except PermissionError as e:
        print(f"[PERMISSION] Немає доступу до директорії: {src_dir}\n  → {e}", file=sys.stderr)
        return
    except FileNotFoundError as e:
        print(f"[MISSING] Директорія зникла: {src_dir}\n  → {e}", file=sys.stderr)
        return
    except OSError as e:
        print(f"[OSERROR] Не вдалося прочитати директорію: {src_dir}\n  → {e}", file=sys.stderr)
        return

    for entry in entries:
        # Пропустити симлінки на директорії (запобігання циклам)
        try:
            if entry.is_symlink():
                # Якщо це симлінк на файл — спробуємо копіювати як файл,
                # якщо на директорію — пропускаємо.
                try:
                    target = entry.resolve(strict=False)
                    if target.is_dir():
                        print(f"[SKIP] Симлінк на директорію пропущено: {entry} -> {target}")
                        continue
                except OSError:
                    # Якщо не вдалось резолвити — спробуємо поводитись як із файлом нижче
                    pass

            if entry.is_dir():
                # Не переносимо DEST всередину DEST (захист від самокопіювання)
                if entry.resolve() == dest_root.resolve():
                    print(f"[SKIP] Призначення всередині джерела: {entry}")
                    continue
                recurse_and_copy(entry, dest_root)
            elif entry.is_file():
                copy_file_to_ext_bucket(entry, dest_root)
            else:
                # Напр., сокети/пристрої — пропускаємо
                print(f"[SKIP] Непідтримуваний тип: {entry}")
        except PermissionError as e:
            print(f"[PERMISSION] Немає доступу до елемента: {entry}\n  → {e}", file=sys.stderr)
        except OSError as e:
            print(f"[OSERROR] Помилка доступу до елемента: {entry}\n  → {e}", file=sys.stderr)
        except Exception as e:
            print(f"[UNKNOWN] Несподівана помилка з елементом: {entry}\n  → {e}", file=sys.stderr)


def main() -> int:
    args = parse_args()
    src: Path = args.src
    dest: Path = args.dest

    # Перевірки
    if not src.exists():
        print(f"[ERROR] Вихідна директорія не існує: {src}", file=sys.stderr)
        return 1
    if not src.is_dir():
        print(f"[ERROR] SRC має бути директорією: {src}", file=sys.stderr)
        return 1

    try:
        safe_mkdir(dest)
    except Exception:
        return 1

    print(f"Починаю копіювання:\n  SRC : {src.resolve()}\n  DEST: {dest.resolve()}\n")
    recurse_and_copy(src, dest)
    print("\nГотово.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
