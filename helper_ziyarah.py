"""Reads blocks from raw.txt and writes Arabic, transliteration, and English lines to separate files and metadata to result.json."""
import json, os



# ITEM
ZIYARAH_NAME = "Dua Nudba"
DESCRIPTION = """
Among the most important supplications within our tradition is Dua al-Nudbah. It is an invocation where we pray for the hastening of the return of our twelfth Imam, Imam Mahdi (p), and also eloquently build a spiritual link with him. We are taught through traditions to recite this particular prayer on the four festive holidays, Eid al-Fitr, Eid al-Adha, Eid al-Ghadeer, and on Fridays.1 This is a beautiful portrayal of what it means to devote ourselves to the Imam of our time during the period of his occultation. Though the Imam is not in our physical company, we have an opportunity to connect with him on a spiritual level and demonstrating our commitment to him by reciting the powerful words of the supplication.

The Importance of Dua al-Nudbah
Dua al-Nudba, or the “supplication of lamentation” is traditionally recited weekly on the day of Friday. The supplication is narrated by Sayed Ibn Tawus, who was one of the greatest scholars within the school of Ahl al-Bayt (p), in one of his famous works.2 Ibn Mashadi, who is also one of the greatest scholars, narrates it in his famous encyclopedic work of supplications and visitations of the Holy Household.3 It is known as the “supplication of lamentation” because it brings the believers to tears during the course of its recitation, due to the fact that the Imam is in occultation when we are in great need and desire for his presence. From its early onset, upon praising God and sending salutations upon the Prophet Muhammad and his progeny (pbut), we immediately enter into the emotional invocation.

Themes of Dua al-Nudbah
There are numerous themes that this invocation emphasizes.

1. God's Wisdom in Choosing Representatives:
Dua al-Nudbah, like many of the other prayers left as a legacy for us by the Holy Household (pbht) begins with a praise of God, and immediately begins to explain God's wisdom in choosing His divine representatives on earth. It is vital to keep in mind that the focal point of this prayer is to connect us with Imam Mahdi (p), and thus the frame of the introduction speaks to God’s chosen guides, the prophets, messengers, and imams. We state, “Praise be to God, the Lord of the worlds. And blessings of God be upon our Leader Muhammad, His Prophet, and on his progeny. O God! All praise is for You for that which You decided upon and resolved in the matter of Your close servants, whom You chosen for Yourself and Your religion.”4
Within a contemporary frame, that guide for us is Imam Mahdi (p), the son of Imam Hassan al-Askari (p).

2. Lamentation Over the Tragedy of the Ahl al-Bayt:
The second theme within the dua is the beginning of the lamentation—lamentation for the oppression that the Prophet and his family had to endure so patiently and gracefully. The Imam eloquently speaks to the merit of Imam Ali (p), but also how quickly his station in the early Muslim community was neglected, eventually leading to his martyrdom and that of his blessed sons. We state, “The community [of people who stood against Ahlulbayt] flocked together to cut off [and abandon] His kinship [Ahlulbayt] and excluded his decedents [from their rightful position in succeeding of the Prophet, and leading the Muslims] except a handful of sincere faithful ones [true Shia] who kept their promise and dutifully upheld the rights of his descendants; Some [of Ahl al-Bayt] were slain, some were taken as captives and some were banished, and [divine] decree was set for them [in bearing the greatest calamities] For which they are expected to receive the best reward).” These lines shake our hearts and core, as we move to the next stage of the prayer, where we earnestly call upon the Awaited Savior (p).

3. Calling Upon Imam Mahdi (p):
Although we may not easily see Imam Mahdi (p) during his occultation, it is imperative that we recognize the potential to still form a strong link to him by finding time to speak with him in solitude as we do during the course of Dua al-Nudbah. We call out to the Imam by some of his titles and attributes. We state, “Where is the everlasting legacy of God which the guiding [prophetic] progeny is never vacant of (i.e., there is always a living representative of God from Ahl al-bayt)? Where is the one intended for eliminating the roots of the oppressors? Where is the one awaited for pulling down the foundations of confusion and hypocrisy? Where is the one hoped for removing oppression and aggression? Where is the one spared for reviving the duties and traditions? ”6
As numerous traditions demonstrate, with the advent of the Imam, peace and justice will be established, overriding injustice and oppression.

4. Demonstration of Our Desperation for the Awaited Savior (p): When supplicating for the Imam (p), it is important that we seek him in a state of desperation because we have such an intense need to be in his company with all the injustice that surrounds us. We should have a true, sincere desire to be in his blessed company. In this dua, we state, “Oh God] grant us his compassion, mercy, prayer, and his benevolence through which we receive ampleness from Your mercy and victory [in achieving the everlasting happiness in paradise]. [Oh God] And by him [through the intercession of Imam Mahdi (p)], accept our prayers, forgive our sins, fulfill our desires, give us means of livelihood, unrestricted, lessen our hardships, and grant us our desires.”7
Through the demonstration of our sincere desire to be in his presence, the aspiration is that God will allow us to be among his helpers and supporters upon the conclusion of his occultation. It is recommended to recite this on Fridays & the 4 Idd days; the Idd ulFitr (1st Shawwal), the Idd al-Azha day (10th of Dhu’l-hijjah), the `Eid al-Ghadir day (18th of Du’l-hijjah).
"""
LANGUAGES = ["ar", "transliteration", "en"]


# PATH - Ziyarah
# INDEX_JSON_PATH = "ziyarah/index.json"
# TEXT_DIR = "ziyarah/text"

# PATH - Dhikr
# INDEX_JSON_PATH = "dhikr/index.json"
# TEXT_DIR = "dhikr/text"

# PATH - Duas
INDEX_JSON_PATH = "duas/index.json"
TEXT_DIR = "duas/text"



# INFO - general
HEADING_PREFIX = "INFO: "
# HEADING_PREFIX = "DESC: "
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

    except FileNotFoundError:
        printError(f"Error: File '{INPUT_FILE}' not found.")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")

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
    
    
    # regenerate_raw_file(ZIYARAH_ID)
    
    # input(">>>>>> Enter to add again")
    
    add_new_ziyarah_or_update_existing_from_raw()
    
    reorder_json_keys()
    
    print("\n------------------ DONE ------------------\n")
    