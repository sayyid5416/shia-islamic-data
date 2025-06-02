"""Reads lines from raw.txt and writes them with total_lines to result.json."""
import json, os


def printStart(msg: str):
    print(f"> {msg}")
    
def printDone(msg: str):
    print(f"    ⩥ {msg}")
    
def printError(msg: str):
    print(f"    [x] {msg}")


def prepare_file(filePath: str):
    # Directory
    dirPath = os.path.dirname(filePath)
    if dirPath and not os.path.exists(dirPath):
        printStart(f"Directory '{dirPath}' not found - creating it.")
        os.makedirs(dirPath, exist_ok=True)
        printDone(f"Created directory: {dirPath}")

    # File
    if not os.path.exists(filePath):
        printStart(f"File '{filePath}' not found - creating it.")
        with open(filePath, "w", encoding="utf-8") as f:
            pass
        printDone(f"Created empty file: {filePath}")
    
    
def extract_text(inputFile: str, outputFile: str):
    try:
        prepare_file(inputFile)
        prepare_file(outputFile)
        
        printStart(f"Reading from {inputFile}...")
        with open(inputFile, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        printDone(f"Total non-empty lines read: {len(lines)}")

        result = {
            "total_lines": len(lines),
            "text": lines
        }

        printStart(f"Writing result to {outputFile}...")
        with open(outputFile, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        printDone("Done.")
        
    except FileNotFoundError:
        printError(f"Error: File '{inputFile}' not found.")
        
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
        
    except Exception as e:
        printError(f"Unexpected error: {e}")


if __name__ == "__main__":
    extract_text(
        inputFile = ".temp/raw.txt",
        outputFile = ".temp/results.json"
    )
