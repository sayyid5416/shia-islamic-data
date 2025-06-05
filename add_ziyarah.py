"""Reads blocks from raw.txt and writes Arabic, transliteration, and English lines to separate files and metadata to result.json."""
import json, os



# INFO
ZIYARAH_NAME = "Syeda Zainab binte Ali (sa) - 2"
DESCRIPTION = """
"""
LANGUAGES = ["ar", "transliteration", "en"]


# INFO - general
HEADING_PREFIX = "INFO: "
# HEADING_PREFIX = "DESC: "
HEADING_PREFIX_LIST = ["INFO: ", "DESC: "]
INPUT_FILE = "raw.txt"
INDEX_JSON_PATH = "ziyarah/index.json"
TEXT_DIR = "ziyarah/text"


# INFO - generated
def getZiyarahId(name: str):
    return name.lower().replace(" ", "-")

ziyarahId = getZiyarahId(ZIYARAH_NAME)



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
    entry = {
        "id": ziyarahId,
        "total_lines": totalLines,
        "languages": LANGUAGES,
        "title": ZIYARAH_NAME,
        "description": DESCRIPTION.strip()
    }

    # Load existing index or create new list
    if os.path.exists(INDEX_JSON_PATH):
        with open(INDEX_JSON_PATH, "r", encoding="utf-8") as f:
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
    with open(INDEX_JSON_PATH, "w", encoding="utf-8") as f:
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
                textLine = block[0]
                if not any(textLine.startswith(prefix) for prefix in HEADING_PREFIX_LIST):
                    infoLine = f"{HEADING_PREFIX}{textLine}"
                else:
                    infoLine = textLine
                blocks[i] = [infoLine, infoLine, infoLine]
            elif len(block) != 3:
                printError(f"Block {i+1} has {len(block)} lines: {block}")
                return

        for idx, langCode in enumerate(LANGUAGES):
            lines = [b[idx] for b in blocks]
            data = {
                "id": ziyarahId,
                "title": ZIYARAH_NAME,
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



def update_ziyarah(old_name: str, new_name: str, new_description: str):
    old_id = getZiyarahId(old_name)
    new_id = getZiyarahId(new_name)

    if not os.path.exists(INDEX_JSON_PATH):
        print(f"[x] {INDEX_JSON_PATH} not found.")
        return

    with open(INDEX_JSON_PATH, "r", encoding="utf-8") as f:
        try:
            index = json.load(f)
        except json.JSONDecodeError:
            print(f"[x] {INDEX_JSON_PATH} is invalid.")
            return

    matched = [z for z in index if z.get("id") == old_id]
    if not matched:
        print(f"[x] No entry with ID: {old_id}")
        return

    # Remove old entry
    index = [z for z in index if z.get("id") != old_id]

    # Add updated entry
    updated = {
        "id": new_id,
        "total_lines": matched[0]["total_lines"],
        "languages": matched[0]["languages"],
        "title": new_name,
        "description": new_description.strip()
    }
    index.append(updated)
    index.sort(key=lambda x: x["id"])

    with open(INDEX_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    print(f"✔ Updated index with ID: {new_id}")

    # Rename text files
    for lang in LANGUAGES:
        old_path = f"{TEXT_DIR}/{lang}/{old_id}.json"
        new_path = f"{TEXT_DIR}/{lang}/{new_id}.json"

        if os.path.exists(old_path):
            with open(old_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            data["id"] = new_id
            data["title"] = new_name

            with open(new_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            os.remove(old_path)
            print(f"✔ Updated: {old_path} → {new_path}")
        else:
            print(f"[!] File not found: {old_path}")






# if __name__ == "__main__":
    add_ziyarah_data()
    
    # update_ziyarah(
    #     "Ziyarat Ale Yasin - Imam Mahdi (ajtfs)",
    #     ZIYARAH_NAME,
    #     DESCRIPTION
    # )