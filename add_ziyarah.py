"""Reads blocks from raw.txt and writes Arabic, transliteration, and English lines to separate files and metadata to result.json."""
import json, os



# INFO
ZIYARAH_NAME = "After Salat"
ZIYARAH_NAME_ARABIC = "بعد الصلاة"
DESCRIPTION = """
"""


# INFO - general
HEADING_PREFIX = "INFO: "
INPUT_FILE = "raw.txt"


# INFO - generated
ziyarahId = ZIYARAH_NAME.lower().replace(" ", "-")



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



def update_index(totalLines: int):
    """Updates ziyarat index by adding/replacing entry and sorting by id."""
    printStart("Updating index...")
    indexPath = "ziyarah/index.json"
    entry = {
        "id": ziyarahId,
        "total_lines": totalLines,
        "languages": ["ar", "en", "transliteration"],
        "title": {
            "ar": ZIYARAH_NAME_ARABIC,
            "en": ZIYARAH_NAME,
            "transliteration": ZIYARAH_NAME
        },
        "description": DESCRIPTION.strip()
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
    index = [item for item in index if item.get("id") != ziyarahId]

    # Append new entry
    index.append(entry)

    # Sort by id
    index.sort(key=lambda x: x.get("id", ""))

    # Save updated index
    with open(indexPath, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    printDone(f"Updated index with {ziyarahId}.")



def add_ziyarah_data():
    try:
        prepare_file(INPUT_FILE)

        printStart(f"Reading from {INPUT_FILE}...")
        blocks = read_blocks(INPUT_FILE)
        printDone(f"Total blocks read: {len(blocks)}")

        for i, block in enumerate(blocks):
            if len(block) == 1:
                infoLine = f"{HEADING_PREFIX}{block[0]}"
                blocks[i] = [infoLine, infoLine, infoLine]
            elif len(block) != 3:
                printError(f"Block {i+1} has {len(block)} lines: {block}")
                return

        languages = [
            ("ar", 0, ZIYARAH_NAME_ARABIC),
            ("transliteration", 1, ZIYARAH_NAME), 
            ("en", 2, ZIYARAH_NAME)
        ]

        for langCode, idx, title in languages:
            lines = [b[idx] for b in blocks]
            data = {
                "id": ziyarahId,
                "title": title,
                "language": langCode,
                "text": lines
            }
            outPath = f"ziyarah/text/{langCode}/{ziyarahId}.json"
            printStart(f"Writing to {outPath}...")
            with open(outPath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            printDone(f"Wrote {len(lines)} lines.")
        
        update_index(totalLines=len(blocks))

    except FileNotFoundError:
        printError(f"Error: File '{INPUT_FILE}' not found.")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")



if __name__ == "__main__":
    add_ziyarah_data()

