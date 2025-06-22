"""Reads blocks from raw.txt and writes Arabic, transliteration, and English lines to separate files and metadata to result.json."""
import json, os



# ITEM
ZIYARAH_NAME = "Salawat Zarrab Isfahani"
DESCRIPTION = """
💠 Signifance of this Dua

• This salwat is ascribed to Abu'l-Hasan al-Zarrab al-Isfahani.

• Shaykh al-Tusi and Sayyid Ibn Tawus have included this famous invocation with the recommended rites of Friday afternoons. Confirming its significance and writing down the series of its reporters, Sayyid Ibn Tawus adds, “This invocation is reported from our master Imam al-Mahdi, peace be upon him." As for Shaykh al-Tusi, he says, “This invocation is reported from the Patron of the Age, Imam al-Mahdi, peace be upon him. It was shown to Abu'l-Hasan al-Zarrab in Makkah

💠 Background

Narrated through a chain by Sayed Ibn Tawoos and Shiekh Tosi may Allah's mercy be upon them through a chain going to Yaqob ibn Yosif AlZarrab AlGassani that in 281 AH on his Haj pilgrimage to MECA from Asfahan along with a group of opposers and some went ahead and rented a room to stay in what was referred to as Dar-e-Khadija also called Dar-e-Rizza (AS). In it was a dark-skinned old lady to whom I had asked who are you? And why is this placed called Dar-Rizza?
I'm a one of their followers and Al Hassan ibn Ali (AS) arranged for me to live in it! As I was his servant!
I was very pleased to hear this and stayed in the place along with my opposing mates and stayed in one room whilst shutting the door using a heavy stone. As we were there, we used to see a glowing man entering the place without the door or stone moving from its place and he used to enter another room to which the old lady did not allow us to go to.
After seeing this I requested the old lady to meet me as I wanted to enquire about the person. She replied by saying that the man advices you to be careful with whom you are dealing with as they mean you harm. I was surprised as indeed I had a quarrel in relation to a debt with my companions. I further enquired and asked the lady about her relationship to Imam Rizza (AS). She explained that she was Imam Hassan's servant and the Imam had told her that she would serve the last Imam AJT.
Someone not so fluent in Arabic had requested me to carry out Hajj on his behalf and paying for my expenses and handing me a letter. I had brought 30 Dinars with me with the intention of placing them in Maqam Ibrahim (AS) but as I was taking to my self-thinking that it's better to hand it to a son of bibi Fatima (the man with the glowing face came to my mind) and handed the amount to the old lady. She came back after a while saying
He says, we have no right over these, do keep them in the place you had intended to do so, yet in return take something in return for this Rizvi lady!
I letter I had with me had the last Imam's signature and was from Al Qasim ibn Alaa from Azerbaijan and I requested the old lady to confirm that its indeed the master's signature.
She went and came back confirm so and giving me good tidings through this Salawat through another letter!Only this time it was from the man with the glowing face with his signature ….the Hujjat (AJT) stating that this is the way Salawat should be recited!

Sayed ibn Tawoos states that this salawat should not be left out for a reason shown to us by Allah (subhan hoo)…

Najmus saaqib pg 1092

This blessed report is mentioned in some other reliable books1; it is narrated from the past scholars through numerous chains of narrators and in some of them in all the places it is mentioned: O Allah, bless…and so on. And in no report is time fixed for recitation of this supplication, except that Sayyid Raziuddin Ali bin Taaoos in Jamaalul Usboo, Pg. 301 after the mention of effective supplication after the Asr Prayer on Friday has said: If you leave the post prayer litanies of Asr Prayer in Friday due to some excuse, you must never omit these Salawat in any case from the aspect that the Almighty Allah has informed us about it. It can be concluded from this blessed statements that nothing is impossible from his lofty rank; as clarified in the previous chapter that the gate of His Eminence is open.

1 Madinatul Maajis, vol. 8, pp. 123-130; Dalaaelul Imaamah, pp. 546- 551; Jamaalul Usboo, pp. 301-306; Behaarul Anwaar, vol. 52, pp. 17-22
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
    