import sys
import time

from core.errors import OriginFileError, OriginLanguageError, format_origin_error
from core.executor import executor


def open_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as source_file:
            code = []
            for line in source_file:
                stripped_line = line.strip()
                if stripped_line:
                    code.append(stripped_line)
            return code
    except FileNotFoundError:
        raise OriginFileError(f"Файл '{file_path}' не знайдено") from None
    except OSError as exc:
        raise OriginFileError(f"Не вдалося відкрити файл '{file_path}': {exc}") from None


def main(file_path):
    start_time = time.time()
    file_code = open_file(file_path)
    executor(file_code)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.6f} seconds")


def run_cli(argv):
    if len(argv) < 2:
        print("FileError: Потрібно передати шлях до файлу програми")
        return 1

    try:
        main(argv[1])
        return 0
    except OriginLanguageError as error:
        print(format_origin_error(error))
        return 1
    except Exception as error:
        print(f"InternalError: інтерпретатор впав усередині Python: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(run_cli(sys.argv))
