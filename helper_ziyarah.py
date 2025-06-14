"""Reads blocks from raw.txt and writes Arabic, transliteration, and English lines to separate files and metadata to result.json."""
import json, os



# ITEM
ZIYARAH_NAME = "Tahajjud - Salatul Layl"
DESCRIPTION = """
AHADEETH ON SALATUL LAYL
Hadith 1
Salatul Layl In the Words of Allah (swt)
Imam as-Sadiq (AS) has said:
"The reward of every good action that a person with true faith performs has been mentioned in the Quran, except for Salatul Layl, since due to the importance (and high status) of it, Allah (SWT) has not explicitly mentioned it and has only said the following (in regards to it):
"Those who forsake their beds to cry unto their Lord in fear and hope, and spend out of that which We have bestowed upon them." Surah as-Sajdah (32:16)

Hadith 2
Purification of the Soul by Salatul Layl
Allah (SWT) in explaining Salatul Layl and those who stay up during the night (doing Ibadaat) has said:
"Surely the rising by night is the firmest way to tread and the best corrective of speech. Surely you have in the day time a long occupation." Surah Muzzammil (73:6-7)
Hadith 3
Salatul Layl and the Nafilah-e-Subh

Allah (SWT) says:
"And in the night, give Him glory too, and at the setting of the stars." Surah Tur (52:49)

Hadith 4
The Worship of the Sincere Ones
Allah (SWT) says:
"And they who pass the night prostrating themselves before their Lord and standing."
Surah Furqaan (25:64)

Hadith 5
Explaining the Pious Ones (Muttaqeen)
Allah (SWT) says:
"They used to sleep but little in the night. And in the morning they asked for forgiveness." Surah Zariyat (51:17-18)


Hadith 6 Seeking Forgiveness at the Time of Sahr
Allah (SWT) says:
"The patient, and the truthful, and the obedient, and those who spend (benevolently) and those who ask forgiveness in the morning times." Surah Ale Imran (3:17)

Hadith 7 Salatul Layl Having Been Waajib (Obligatory) for the Prophet of Allah (SWT)
Allah (SWT) says:
"And during a part of the night, pray Tahajjud beyond what is incumbent on you; maybe your Lord will raise you to a position of great glory." Surah Bani Israeel (17:79)

Hadith 8
Wake up for Salatul Layl
Allah (SWT) says:
(O you who have wrapped up in your garments! Rise to pray in the night except a little.) Surah Muzzammil (73:1-2)

Hadith 9
Wake up for Salatul Layl
"Rise to pray in the night except a little, Half of it, or lessen it a little, Or add to it, and recite the Quran as it ought to be recited."
Surah Muzzammil (73:2-4)

Hadith 10 Those Who Prostrate
Allah (SWT) says:
"And rely on the Mighty, the Merciful. Who sees you when you stand up. And your turning over and over among those who prostrate themselves before Allah." Surah Shuara (26:217-219)

Hadith 11 Describing Those Who Stay Up in the Night
Allah (SWT) says:
"(Can he who passes his night in sajdah (adoration), standing up or on his knees, who dreads the terrors of the life to come and hopes to earn the mercy of his Lord, (be compared to the unbeliever?"
Surah Zumar (39:9)

Hadith 12 Pleasure of Allah (SWT) Imam Ja'far as-Sadiq (AS) has said:"The pleasure of Allah (SWT) lies in Salatul-Layl."

Hadith 13 Sign of True Faith in Allah (SWT) and Belief in the Day of Judgement Imam Muhammad al-Baqir(AS) has said: "One who has true faith in Allah (SWT) and the last day, will not allow the night to pass into the day without performing Salatul-Witr."

Hadith 14 The Greatness of a Believer
Imam Ja'far as-Sadiq (AS) has said: "The greatness of a believer is his Salat in the night and his dignity lies in not asking others for his needs."

Hadith 15
Beauty of the Next Life
Imam Ja'far as-Sadiq (AS) has said: "Allah (SWT) - the Noble and the Great has said that the wealth and children are a beautification of this world and surely the 8 Rakat (of Salatul Layl) that a servant performs at the end of the night is a beautification for the next life."

MERITS
By praying Salatul-Layl one’s livelihood is increased, one passes easily through “Sakaraat” (great and grueling pain a dying person suffers at the time of death) and finds happiness in “Barzakh” (the Spiritual world where the departed souls stay either in happiness or misery, until the Day of Resurrection).
Imam Jaffar Sadiq (a.s.) quotes Imam Ali (as) as saying that the Prophet (saww) said that a person who prays Salatul-Layl gets the following twenty four kinds of benefits:
Secures Allah’s pleasure.
Makes friendship with Angels.
Is the Sunnat of the Prophets (a.s.)
Provides the means to pursue knowledge.
Constitutes the root of our faith.
Keeps one physically fit.
Drives Shaytan away.
Protects one from enemies.
Serves as a means of acceptance of one’s Duas and good deeds.
Increases one’s livelihood.
Intercedes with the Angel of Death.
Lights up the grave.
Provides comfortable bedding in the grave.
Helps answering with ease the questioning of Munkar and Nakir in the grave.
Gives companionship in the grave.
Provides shelter on the Day of Judgment.
Crowns one on the Day of Reckoning.
Clothes one on the Day of Resurrection.
Provides one with light on the Day of Judgment.
Forms a barrier against the fire of Hell.
Gets Allah’s pardon on the Day of Judgment.
Increases the weight of good deeds on the scale.
Helps one crossing the Bridge of “Siraat” without any difficulty.
Forms the key to the Paradise.
"""
LANGUAGES = ["ar", "transliteration", "en"]
FOLDER = "salah"
# FOLDER = "dua"
# FOLDER = "dhikr"
# FOLDER = "ziyarah"



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
    new_description: str | None = None
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
    updated_description = new_description.strip() if new_description is not None else entry.get("description", "")

    index = [z for z in index if z.get("id") != current_id]
    index.append(
        {
            "id": updated_id,
            "title": updated_title,
            "description": updated_description,
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
        
        reorder_json_keys()
    
    except FileNotFoundError:
        printError(f"Error: File '{INPUT_FILE}' not found.")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")
        
    print("\n------------------ DONE ------------------\n")
    