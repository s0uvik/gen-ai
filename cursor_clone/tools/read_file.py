def read_file(file_path: str):
    """
    Read content from a file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return content if content else "File is empty"

    except FileNotFoundError:
        return f"❌ File not found: {file_path}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"
