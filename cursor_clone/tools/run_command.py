import subprocess


def run_command(cmd: str):
    """
    Execute a shell command safely and return the output.
    Uses subprocess for better output capture and safety.
    """
    try:
        # Block dangerous commands
        dangerous_keywords = ["rm -rf /", "format", "del /f", ":(){:|:&};:", "dd if="]
        if any(keyword in cmd.lower() for keyword in dangerous_keywords):
            return "⚠️ Dangerous command blocked for safety"

        # Execute command and capture output
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = result.stdout if result.stdout else result.stderr
        return (
            output
            if output
            else f"Command executed successfully (exit code: {result.returncode})"
        )

    except subprocess.TimeoutExpired:
        return "⚠️ Command timed out after 30 seconds"
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"
