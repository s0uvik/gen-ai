import os


def write_file(file_path: str, content: str):
    """
    Write content to a file safely.
    Creates parent directories if they don't exist.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(
            os.path.dirname(file_path) if os.path.dirname(file_path) else ".",
            exist_ok=True,
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"✅ Successfully wrote {len(content)} characters to {file_path}"

    except Exception as e:
        return f"❌ Error writing file: {str(e)}"
