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


def update_index(name: str, totalLines: int):
    printStart("Updating index...")
    indexPath = "ziyarah/index.json"
    slug = name.lower().replace(" ", "-")
    entry = {
        "id": slug,
        "total_lines": totalLines,
        "languages": ["ar", "en", "transliteration"],
        "title": {
            "ar": "",
            "en": name,
            "transliteration": name
        },
        "description": ""
    }

    # Load existing index or create new list
    if os.path.exists(indexPath):
        with open(indexPath, "r", encoding="utf-8") as f:
            try:
                index = json.load(f)
            except json.JSONDecodeError:
                index = []
    else:
        index = []

    # Remove old entry with same id if exists
    index = [item for item in index if item.get("id") != slug]

    # Append new entry
    index.append(entry)

    # Save updated index
    with open(indexPath, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    printDone(f"Updated index with {slug}.")


def add_ziyarah_data(inputFile: str, name: str):
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

        for langCode, idx in languages:
            lines = [b[idx] for b in blocks]
            data = {
                "id": slug,
                "title": name,
                "language": langCode,
                "text": lines
            }
            outPath = f"ziyarah/text/{langCode}/{slug}.json"
            printStart(f"Writing to {outPath}...")
            with open(outPath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            printDone(f"Wrote {len(lines)} lines.")
        
        update_index(name=name, totalLines=len(blocks))

    except FileNotFoundError:
        printError(f"Error: File '{inputFile}' not found.")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")


if __name__ == "__main__":
    ziyarahName = "name here"
    totalLines = add_ziyarah_data(inputFile="raw.txt", name=ziyarahName)

