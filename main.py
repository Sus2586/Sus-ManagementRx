import sys
import os

# Ensure stdout prints immediately without buffering
os.environ["PYTHONUNBUFFERED"] = "1"
print("==================================================", flush=True)
print(">>> Maple ManagementRx Bot Startup Initializer <<<", flush=True)
print("==================================================", flush=True)

current_dir = os.path.dirname(os.path.abspath(__file__))
print(f">>> Current directory: {current_dir}", flush=True)

# Search for bot.py in current directory and subdirectories
target_dir = None
if os.path.exists(os.path.join(current_dir, "bot.py")):
    target_dir = current_dir
elif os.path.exists(os.path.join(current_dir, "maple-management-rx", "bot.py")):
    target_dir = os.path.join(current_dir, "maple-management-rx")
else:
    # Deep walk search as fallback
    for root, dirs, files in os.walk(current_dir):
        if "bot.py" in files:
            target_dir = root
            break

if target_dir:
    print(f">>> Located bot.py in: {target_dir}", flush=True)
    if target_dir not in sys.path:
        sys.path.insert(0, target_dir)
    os.chdir(target_dir)
else:
    print(f">>> CRITICAL: Could not find bot.py in {current_dir}", flush=True)
    print(f">>> Files in root: {os.listdir(current_dir)}", flush=True)
    sys.exit(1)

if __name__ == "__main__":
    print(">>> Importing bot module...", flush=True)
    try:
        import bot
        print(">>> Bot module imported successfully. Starting bot.main()...", flush=True)
        bot.main()
    except Exception as e:
        print(f">>> ERROR during bot initialization: {e}", flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
