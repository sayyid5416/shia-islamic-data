"""Reads blocks from raw.txt and writes Arabic, transliteration, and English lines to separate files and metadata to result.json."""
import json, os



# ITEM
ZIYARAH_NAME = "Salawat after Asr on Friday"
DESCRIPTION = """
"""
LANGUAGES = ["en"]
LANGUAGES = ["ar", "transliteration", "en"]
# FOLDER = "salah"
# FOLDER = "duas"
FOLDER = "dhikr"
# FOLDER = "ziyarah"
# FOLDER = "sermon"



# PATH - Duas
INDEX_JSON_PATH = f"{FOLDER}/index.json"
TEXT_DIR = f"{FOLDER}/text"

# INFO - general
HEADING_PREFIX = "INFO: "
HEADING_PREFIX = "DESC: "
HEADING_PREFIX_LIST = ["INFO: ", "DESC: "]
INPUT_FILE = "raw.txt"



# INFO - generated
def getZiyarahId(name: str):
    return name.lower().replace(" ", "-")

ZIYARAH_ID = getZiyarahId(ZIYARAH_NAME)



# ---------------------------- Helpers ---------------------------- #
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

def update_index_after_adding_new_ziyarah(totalLines: int):
    """Updates ziyarat index by adding/replacing entry"""
    printStart("Updating index...")
    entry = {
        "id": ZIYARAH_ID,
        "title": ZIYARAH_NAME,
        "description": DESCRIPTION.strip(),
        "total_lines": totalLines,
        "languages": LANGUAGES,
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
    index = [item for item in index if item.get("id") != ZIYARAH_ID]

    # Append new entry
    index.append(entry)

    # Save updated index
    with open(INDEX_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    printDone(f"Updated index with {ZIYARAH_ID}.")




# ---------------------------- Main functions ---------------------------- #
def add_new_ziyarah_or_update_existing_from_raw():
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
        elif len(block) != len(LANGUAGES):
            printError(f"Block {i+1} has {len(block)} lines: {block}")
            return

    for idx, langCode in enumerate(LANGUAGES):
        lines = [b[idx] for b in blocks]
        data = {
            "id": ZIYARAH_ID,
            "title": ZIYARAH_NAME,
            "language": langCode,
            "text": lines
        }
        outPath = f"{TEXT_DIR}/{langCode}/{ZIYARAH_ID}.json"
        prepare_file(outPath)
        printStart(f"Writing to {outPath}...")
        with open(outPath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        printDone(f"Wrote {len(lines)} lines.")
    
    update_index_after_adding_new_ziyarah(totalLines=len(blocks))


def change_ziyarah_metadata(
    current_id: str,
    new_title: str | None = None,
    # new_description: str | None = None
):
    if not os.path.exists(INDEX_JSON_PATH):
        printError(f"{INDEX_JSON_PATH} not found.")
        return

    with open(INDEX_JSON_PATH, "r", encoding="utf-8") as f:
        try:
            index = json.load(f)
        except json.JSONDecodeError:
            printError(f"{INDEX_JSON_PATH} is invalid.")
            return

    matched = [z for z in index if z.get("id") == current_id]
    if not matched:
        printError(f"No entry with ID: {current_id}")
        return

    entry = matched[0]
    updated_title = new_title or entry["title"]
    updated_id = getZiyarahId(updated_title)
    # updated_description = new_description.strip() if new_description is not None else entry.get("description", "")

    index = [z for z in index if z.get("id") != current_id]
    index.append(
        {
            "id": updated_id,
            "title": updated_title,
            "description": entry["total_lines"],
            "total_lines": entry["total_lines"],
            "languages": entry["languages"],
        }
    )

    with open(INDEX_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    printDone(f"Updated index with ID: {updated_id}")

    if updated_id != current_id or new_title:
        for lang in entry["languages"]:
            old_path = f"{TEXT_DIR}/{lang}/{current_id}.json"
            new_path = f"{TEXT_DIR}/{lang}/{updated_id}.json"

            if os.path.exists(old_path):
                with open(old_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                data["id"] = updated_id
                data["title"] = updated_title

                with open(new_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                os.remove(old_path)
                printDone(f"Renamed {old_path} → {new_path}")
            else:
                printError(f"File not found: {old_path}")

def regenerate_raw_file(ziyarah_id: str):
    """Rebuilds raw.txt from existing JSON files using languages from index.json."""
    if not os.path.exists(INDEX_JSON_PATH):
        printError(f"{INDEX_JSON_PATH} not found.")
        return

    with open(INDEX_JSON_PATH, "r", encoding="utf-8") as f:
        try:
            index = json.load(f)
        except json.JSONDecodeError:
            printError(f"{INDEX_JSON_PATH} is invalid.")
            return

    matched = next((z for z in index if z.get("id") == ziyarah_id), None)
    if not matched:
        printError(f"No entry with ID: {ziyarah_id}")
        return

    languages = matched.get("languages", [])
    lang_data: dict[str, list[str]] = {}

    for lang in languages:
        path = f"{TEXT_DIR}/{lang}/{ziyarah_id}.json"
        if not os.path.exists(path):
            printError(f"Missing file: {path}")
            return
        with open(path, "r", encoding="utf-8") as f:
            lang_data[lang] = json.load(f).get("text", [])

    total_lines = len(next(iter(lang_data.values())))
    if not all(len(lang_data[lang]) == total_lines for lang in languages):
        printError("Mismatch in line counts across language files.")
        return

    printStart("Rebuilding raw.txt...")
    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        for i in range(total_lines):
            lines = [lang_data[lang][i].strip() for lang in languages]
            unique_lines = set(lines)
            if len(unique_lines) == 1:
                line = lines[0]
                if not any(line.startswith(prefix) for prefix in HEADING_PREFIX_LIST):
                    line = f"{HEADING_PREFIX}{line}"
                f.write(line + "\n\n")
            else:
                for line in lines:
                    f.write(line + "\n")
                f.write("\n")
    printDone(f"Generated {INPUT_FILE} with {total_lines} blocks.")

def reorder_json_keys():
    with open(INDEX_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    reordered = [
        {
            "id": item["id"],
            "title": item["title"],
            "description": item["description"],
            "total_lines": item["total_lines"],
            "languages": item["languages"]
        }
        for item in data
    ]
    
    reordered.sort(key=lambda x: x.get("id", ""))

    with open(INDEX_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(reordered, f, ensure_ascii=False, indent=4)
        



if __name__ == "__main__":
    print("\n------------------ STARTING ------------------\n")
    
    try:
        
        # regenerate_raw_file(ZIYARAH_ID)
        
        # input(">>>>>> Enter to add again")
        
        add_new_ziyarah_or_update_existing_from_raw()
        
        # change_ziyarah_metadata(
        #     current_id = "imam-ali-(as)---27th-rajab",
        #     new_title = "Imam Ali (as) - on Mi'raj Day",
        # )
        
        reorder_json_keys()
    
    except FileNotFoundError:
        printError(f"Error: File '{INPUT_FILE}' not found.")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")
        
    print("\n------------------ DONE ------------------\n")
    