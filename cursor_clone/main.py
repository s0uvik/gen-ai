from dotenv import load_dotenv
from openai import OpenAI
import json
from .tools.run_command import run_command
from .tools.write_file import write_file
from .tools.read_file import read_file

load_dotenv()

client = OpenAI()

available_tools = {
    "run_command": run_command,
    "write_file": write_file,
    "read_file": read_file,
}


# Load system prompt from file
def load_prompt(filepath: str) -> str:
    """Load prompt from a text file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ Warning: {filepath} not found")


# Load the system prompt
SYSTEM_PROMPT = load_prompt("prompts/system_prompt.txt")

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("🚀 Mini Cursor Clone - AI Code Assistant")
print("Type your coding questions or commands. Type 'q' to quit.\n")

while True:
    try:
        query = input("💬 You: ").strip()

        if query.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye! Happy coding!")
            break

        if not query:
            print("⚠️ Empty input. Please type something.")
            continue

        messages.append({"role": "user", "content": query})

        # Agent loop
        while True:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=messages,
            )

            assistant_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_message})

            try:
                parsed_response = json.loads(assistant_message)
            except json.JSONDecodeError:
                print("❌ Error: Invalid JSON response from AI")
                break

            step = parsed_response.get("step")

            # Handle ACTION step
            if step == "action":
                tool_name = parsed_response.get("function")
                tool_input = parsed_response.get("input")

                if not tool_name or tool_input is None:
                    print("❌ Error: Missing function or input in action step")
                    break

                # Check if tool exists
                if tool_name not in available_tools:
                    print(f"❌ Error: Unknown tool '{tool_name}'")
                    break

                # Handle write_file which needs two parameters
                if tool_name == "write_file":
                    file_path = parsed_response.get("file_path")
                    content = tool_input

                    if not file_path:
                        print("❌ Error: Missing file_path for write_file")
                        break

                    print(f"\n📝 Writing to: {file_path}")
                    output = available_tools[tool_name](file_path, content)
                    print(f"📤 Output: {output}\n")

                # Handle other tools with single parameter
                else:
                    print(f"\n🔧 Executing: {tool_input}")
                    output = available_tools[tool_name](tool_input)
                    print(f"📤 Output:\n{output}\n")

                # Send observation back to AI
                messages.append(
                    {
                        "role": "user",
                        "content": json.dumps(
                            {"step": "observe", "output": str(output)}
                        ),
                    }
                )
                continue

            # Handle OUTPUT step
            elif step == "output":
                content = parsed_response.get("content", "No response provided")
                print(f"\n🤖 Assistant: {content}\n")
                break

            # Handle PLAN step (optional, just continue)
            elif step == "plan":
                plan_content = parsed_response.get("content")
                if plan_content:
                    print(f"📋 Planning: {plan_content}")
                continue

            # Unknown step
            else:
                print(f"⚠️ Unknown step: {step}")
                break

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        break
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        continue
