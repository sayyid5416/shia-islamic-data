"""Reads blocks from raw.txt and writes Arabic, transliteration, and English lines to separate files and metadata to result.json."""
import json, os


def printStart(msg: str):
    print(f"> {msg}")
    
def printDone(msg: str):
    print(f"    ⩥ {msg}")
    
def printError(msg: str):
    print(f"    [x] {msg}")


def prepare_file(filePath: str):
    dirPath = os.path.dirname(filePath)
    if dirPath and not os.path.exists(dirPath):
        printStart(f"Directory '{dirPath}' not found - creating it.")
        os.makedirs(dirPath, exist_ok=True)
        printDone(f"Created directory: {dirPath}")

    if not os.path.exists(filePath):
        printStart(f"File '{filePath}' not found - creating it.")
        with open(filePath, "w", encoding="utf-8") as f:
            pass
        printDone(f"Created empty file: {filePath}")


def read_blocks(filePath: str) -> list[list[str]]:
    with open(filePath, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f]

    blocks = []
    current_block = []

    for line in raw_lines:
        if line:
            current_block.append(line)
        elif current_block:
            blocks.append(current_block)
            current_block = []

    if current_block:
        blocks.append(current_block)

    return blocks

def extract_text(inputFile: str, name: str):
    try:
        prepare_file(inputFile)

        printStart(f"Reading from {inputFile}...")
        blocks = read_blocks(inputFile)
        printDone(f"Total blocks read: {len(blocks)}")

        if not all(len(b) == 3 for b in blocks):
            printError("Some blocks do not have exactly 3 lines.")
            for i, block in enumerate(blocks):
                if len(block) != 3:
                    printError(f"Block {i+1} has {len(block)} lines: {block}")
            return

        slug = name.lower().replace(" ", "-")
        languages = [("ar", 0), ("transliteration", 1), ("en", 2)]

        for lang_code, idx in languages:
            lines = [b[idx] for b in blocks]
            data = {
                "id": slug,
                "title": name,
                "language": lang_code,
                "text": lines
            }
            out_path = f"ziyarah/text/{lang_code}/{slug}.json"
            prepare_file(out_path)
            printStart(f"Writing to {out_path}...")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            printDone(f"Wrote {len(lines)} lines.")

    except FileNotFoundError:
        printError(f"Error: File '{inputFile}' not found.")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")



if __name__ == "__main__":
    extract_text(
        inputFile="raw.txt",
        name="Ziyarat al-Nahiya"
    )
