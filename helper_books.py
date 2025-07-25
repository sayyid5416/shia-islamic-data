from helper_ziyarah import generateIdFromName, printDone, printError, printStart, prepare_file
import json
import shutil
import os



NAME = "Sunan al-Nasa'i - Glossary of Islamic Terms"
AUTHOR = "Ahmad ibn Shu'ayb al-Nasa'i"
TRANSLATOR = ["Nasiruddin al-Khattab", "Abu Khaliyl"]
PUBLISHER = "Darussalam Publishers and Distributors, Riyadh, Saudi Arabia"
ABOUT = """
Sunan al-Nasa'i is one of the six canonical hadith collections in Sunni Islam, compiled by al-Nasa'i (d. 915 CE).

Sunni View: Highly valued, especially for its authenticity; it is considered among the most rigorous in chain verification after Sahih al-Bukhari and Sahih Muslim  
Shia View: Not accepted as reliable due to differing standards for evaluating narrators and legal content
"""
CATEGORY = "Sunni"


ALL_CATEGORIES = [
    "Sunni & Shi'a",
    "Karbala",
    "Sahifa",
    "Marja al-Taqlīd",
    "Sunni"
]



# Generated
ID = generateIdFromName(NAME)
COVER = ""
COVER = f"https://raw.githubusercontent.com/sayyid5416/shia-islamic-data/main/books/covers/{ID}.jpg"

# Location
INDEX_FILE = "books/index.json"
PDF_FILE_PATH = "books/new.pdf"

# Template
"""
{
    "id": "",
    "name": "",
    "author": "",
    "cover": "",
    "translator": [],
    "publisher": "",
    "about": "",
    "size": "",
    "category": "",
}
"""



def format_file_size(bytes_size: int) -> str:
    """Convert file size in bytes to a human-readable string."""
    if bytes_size < 0:
        return "Invalid"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(bytes_size)
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
        
    sizeStr = f"{size:.1f}".removesuffix(".0")
    return f"{sizeStr} {units[i]}"






def add_pdf_file() -> None:
    """Append or update book info in index.json and copy PDF to final path."""
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

        new_entry = {
            "id": ID,
            "name": NAME,
            "author": AUTHOR,
            "translator": TRANSLATOR,
            "publisher": PUBLISHER,
            "about": ABOUT.strip(),
            "size": format_file_size(file_size),
            "category": CATEGORY,
            "cover": COVER,
        }

        for i, item in enumerate(index_data):
            if item.get("id") == ID:
                index_data[i] = new_entry
                break
        else:
            index_data.append(new_entry)

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


def copy_cover_with_name() -> None:
    """Copy cover.jpg to its final path if COVER URL is defined and local file exists."""
    if not COVER:
        return

    printStart("Copying cover image")

    source_cover_path = "books/cover.jpg"
    final_cover_path = f"books/covers/{ID}.jpg"

    if not os.path.exists(source_cover_path):
        printError(f"Source cover not found: {source_cover_path}")
        return

    prepare_file(final_cover_path)
    shutil.copy(source_cover_path, final_cover_path)
    printDone(f"Copied cover to: {final_cover_path}")


def update_cover_in_index() -> None:
    """Copy cover image and update its path in index.json if the book exists."""
    printStart("Updating cover path in index")
    prepare_file(INDEX_FILE)

    with open(INDEX_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise TypeError("index.json must be a list of entries")

        for book in data:
            if book.get("id") == ID:
                book["cover"] = COVER
                break

        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.truncate()
    printDone("Cover path updated in index")



if __name__ == "__main__":
    print("\n------------------ STARTING ------------------\n")

    try:

        add_pdf_file()
        copy_cover_with_name()
        # update_cover_in_index()
        sort_index_file()

    except FileNotFoundError as e:
        printError(f"Error: File not found. {e}")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")

    print("\n------------------ DONE ------------------\n")
