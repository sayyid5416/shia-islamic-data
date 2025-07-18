"""Reads blocks from raw.txt and writes Arabic, transliteration, and English lines to separate files and metadata to result.json."""
import json, os



# ITEM
ZIYARAH_NAME = "aa - test 2"
DESCRIPTION = """
"""
LANGUAGES = ["en"]
# LANGUAGES = ["ar", "transliteration", "en"]

# FOLDER = "amaal"
# FOLDER = "dhikr"
# FOLDER = "duas"
FOLDER = "salah"
# FOLDER = "sermon"
FOLDER = "ziyarah"

AUDIO_ID = ""

ADD_PREFIX_FOR_SINGLE_LINE = False       # USE WISELY -> If True, adds "INFO: " prefix to single-line blocks; if False, skips them
# ADD_PREFIX_FOR_SINGLE_LINE = True       # USE WISELY -> If True, adds "INFO: " prefix to single-line blocks; if False, skips them



# PATH - Duas
INDEX_JSON_PATH = f"{FOLDER}/index.json"
TEXT_DIR = f"{FOLDER}/text"

# INFO - general
HEADING_PREFIX = "INFO: "
HEADING_PREFIX = "DESC: "
HEADING_PREFIX_LIST = ["INFO: ", "DESC: "]
INPUT_FILE = "raw.txt"

LANGUAGES_ALL = ["ar", "transliteration", "en"]
ALL_FOLDERS = ["amaal", "dhikr", "duas", "salah", "sermon", "ziyarah"]


# INFO - generated
def generateIdFromName(name: str):
    return name.lower().replace(" ", "-")

ZIYARAH_ID = generateIdFromName(ZIYARAH_NAME)



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

    en_path = f"{TEXT_DIR}/en/{ZIYARAH_ID}.json"
    total_lines_text = 0
    if os.path.exists(en_path):
        with open(en_path, "r", encoding="utf-8") as f:
            lines = json.load(f).get("text", [])
            total_lines_text = sum(1 for l in lines if not any(l.startswith(p) for p in HEADING_PREFIX_LIST))

    entry = {
        "id": ZIYARAH_ID,
        "title": ZIYARAH_NAME,
        "description": DESCRIPTION.strip(),
        "total_lines": totalLines,
        "total_lines_text": total_lines_text,
        "languages": LANGUAGES,
        "audio_id": AUDIO_ID,
        "item_type": FOLDER,
    }

    if os.path.exists(INDEX_JSON_PATH):
        with open(INDEX_JSON_PATH, "r", encoding="utf-8") as f:
            try:
                index = json.load(f)
            except json.JSONDecodeError:
                index = []
    else:
        index = []

    index = [item for item in index if item.get("id") != ZIYARAH_ID]
    index.append(entry)

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
        if len(block) == len(LANGUAGES) and not ADD_PREFIX_FOR_SINGLE_LINE:
            continue
        elif len(block) == 1:
            textLine = block[0]
            if not any(textLine.startswith(prefix) for prefix in HEADING_PREFIX_LIST):
                infoLine = f"{HEADING_PREFIX}{textLine}"
            else:
                infoLine = textLine
            blocks[i] = [infoLine] * len(LANGUAGES)
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


def change_ziyarah_metadata(current_id: str, new_title: str | None = None):
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
    updated_id = generateIdFromName(updated_title)

    index = [z for z in index if z.get("id") != current_id]
    index.append(
        {
            "id": updated_id,
            "title": updated_title,
            "description": entry["description"],
            "total_lines": entry["total_lines"],
            "total_lines_text": entry.get("total_lines_text", 0),
            "languages": entry["languages"],
            "audio_id": entry.get("audio_id", ""),
            "item_type": entry.get("item_type", FOLDER),
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
                f.write(line + "\n\n")
            else:
                for line in lines:
                    f.write(line + "\n")
                f.write("\n")
    printDone(f"Generated {INPUT_FILE} with {total_lines} blocks.")


def reorder_json_keys():
    for _folder in ALL_FOLDERS:
        _indexJsonPath = f"{_folder}/index.json"
        with open(_indexJsonPath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        reordered = [
            {
                "id": item["id"],
                "title": item["title"],
                "description": item["description"],
                "total_lines": item["total_lines"],
                "total_lines_text": item.get("total_lines_text", 0),
                "languages": item["languages"],
                "audio_id": item.get("audio_id", ""),
                "item_type": item.get("item_type", _folder),
            }
            for item in data
        ]
        
        reordered.sort(key=lambda x: x.get("id", ""))

        with open(_indexJsonPath, 'w', encoding='utf-8') as f:
            json.dump(reordered, f, ensure_ascii=False, indent=4)


def add_total_lines_without_info_or_desc_to_all_index_files():
    """
    Read file from <folder>/text/<language>/<file>.json for all items in ALL_FOLDERS.
    Adds 'total_lines_text' in index.json (excluding INFO:/DESC: lines).
    """
    for folder in ALL_FOLDERS:
        index_path = f"{folder}/index.json"

        if not os.path.exists(index_path):
            printError(f"{index_path} not found.")
            continue

        with open(index_path, "r", encoding="utf-8") as f:
            try:
                index = json.load(f)
            except json.JSONDecodeError:
                printError(f"{index_path} is invalid.")
                continue

        for entry in index:
            z_id = entry["id"]
            lines = None

            for lang in LANGUAGES_ALL:
                json_path = f"{folder}/text/{lang}/{z_id}.json"
                if os.path.exists(json_path):
                    with open(json_path, "r", encoding="utf-8") as f:
                        lines = json.load(f).get("text", [])
                    break

            if lines is None:
                printError(f"Missing all language files for ID: {z_id}")
                entry["total_lines_text"] = 0
                continue

            entry["total_lines_text"] = sum(
                1 for line in lines if not any(line.startswith(p) for p in HEADING_PREFIX_LIST)
            )

        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=4)
        printDone(f"Updated {index_path}")






if __name__ == "__main__":
    print("\n------------------ STARTING ------------------\n")

    try:
        
        # regenerate_raw_file(ZIYARAH_ID)
        
        # input(">>>>>> Enter to add again")
        
        # add_new_ziyarah_or_update_existing_from_raw()
        
        # change_ziyarah_metadata(
        #     current_id =  "salawat-zarrab-isfahani",
        #     new_title = "Salawat - Zarrab Isfahani",
        # )
        
        # add_total_lines_without_info_or_desc_to_all_index_files()
        reorder_json_keys()

    except FileNotFoundError:
        printError(f"Error: File '{INPUT_FILE}' not found.")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")

    print("\n------------------ DONE ------------------\n")
