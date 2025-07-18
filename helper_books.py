from helper_ziyarah import generateIdFromName, printDone, printError, printStart, prepare_file
import json
import shutil
import os



# Information
NAME = "Peshawar Nights"
AUTHOR = "Sayyid Muhammad al-Musawi al-Shirazi"
TRANSLATOR = ["Hamid Quinlan", "Charles Ali Campbell"]
PUBLISHER = "Ansariyan Publications - Qum"
ABOUT = """
Transcript of dialogues between Sunni scholars and Shi'i author, about major topics relating to Shi'ism including the death of the Prophet (s), successorship, companions, infallibility, Muta' (temporary marriage), and the family of the Prophet.
"""
CATEGORY = "Sunni & Shi'a"


ALL_CATEGORIES = [
    "Sunni & Shi'a",
]



# Generated
ID = generateIdFromName(NAME)

# Location
INDEX_FILE = "books/index.json"
PDF_FILE_PATH = "books/new.pdf"

# Template
"""
{
    "id": "",
    "name": "",
    "author": "",
    "translator": [],
    "publisher": "",
    "about": "",
    "size": "",
    "category": "",
}
"""



def format_file_size(bytes_size: int) -> str:
    """Convert file size in bytes to a human-readable string."""
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(bytes_size)
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
        
    sizeStr = f"{size:.1f}".removesuffix(".0")
    return f"{sizeStr} {units[i]}"






def add_pdf_file() -> None:
    """Append book info to index.json and copy PDF to final path."""
    printStart("Adding new PDF file")

    final_pdf_path = f"books/pdfs/{CATEGORY}/{ID}.pdf"
    prepare_file(final_pdf_path)
    shutil.copy(PDF_FILE_PATH, final_pdf_path)
    printDone(f"Copied PDF to: {final_pdf_path}")

    printStart("Updating index")
    prepare_file(INDEX_FILE)
    file_size = os.path.getsize(final_pdf_path)

    with open(INDEX_FILE, "r+", encoding="utf-8") as f:
        try:
            index_data = json.load(f)
            if not isinstance(index_data, list):
                index_data = [index_data]
        except json.JSONDecodeError:
            index_data = []

        index_data.append({
            "id": ID,
            "name": NAME,
            "author": AUTHOR,
            "translator": TRANSLATOR,
            "publisher": PUBLISHER,
            "about": ABOUT.strip(),
            "size": format_file_size(file_size),
            "category": CATEGORY,
        })

        f.seek(0)
        json.dump(index_data, f, ensure_ascii=False, indent=4)
        f.truncate()

    printDone("Index updated")


def sort_index_file() -> None:
    """Sort index.json list by id and sort keys in each entry."""
    printStart("Sorting Index")
    prepare_file(INDEX_FILE)
    with open(INDEX_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise TypeError("index.json must be a list of entries")

        sorted_data = sorted(data, key=lambda x: x.get("id", "").lower())
        sorted_data = [dict(sorted(item.items())) for item in sorted_data]

        f.seek(0)
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)
        f.truncate()
    printDone("Index sorted")




if __name__ == "__main__":
    print("\n------------------ STARTING ------------------\n")

    try:

        add_pdf_file()
        sort_index_file()

    except FileNotFoundError as e:
        printError(f"Error: File not found. {e}")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")

    print("\n------------------ DONE ------------------\n")
