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


def extract_text(inputFile: str, outputFile: str):
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

        arabic = [b[0] for b in blocks]
        translit = [b[1] for b in blocks]
        english = [b[2] for b in blocks]

        base = os.path.splitext(outputFile)[0]
        files = {
            f"{base}_arabic.json": {"text": arabic},
            f"{base}_translit.json": {"text": translit},
            f"{base}_english.json": {"text": english},
            f"{base}_meta.json": {"total_blocks": len(blocks)}
        }

        for path, content in files.items():
            prepare_file(path)
            printStart(f"Writing to {path}...")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=4)
            printDone(f"Wrote {len(content.get('text', [])) if 'text' in content else 1} items.")

    except FileNotFoundError:
        printError(f"Error: File '{inputFile}' not found.")
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        printError(f"Unexpected error: {e}")



if __name__ == "__main__":
    extract_text(
        inputFile=".temp/raw.txt",
        outputFile=".temp/results.json"
    )
