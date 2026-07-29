import sys
import os

# Unbuffer stdout so logs display live in Pella's console
os.environ["PYTHONUNBUFFERED"] = "1"
print(">>> Bootstrapping Maple ManagementRx Bot...", flush=True)

current_dir = os.path.dirname(os.path.abspath(__file__))

# Find bot.py location dynamically
search_paths = [
    os.path.join(current_dir, "maple-management-rx"),
    current_dir
]

bot_dir = None
for path in search_paths:
    if os.path.exists(os.path.join(path, "bot.py")):
        bot_dir = path
        break

if bot_dir:
    print(f">>> Found bot.py in: {bot_dir}", flush=True)
    if bot_dir not in sys.path:
        sys.path.insert(0, bot_dir)
    os.chdir(bot_dir)
else:
    print(f">>> CRITICAL ERROR: bot.py not found in {search_paths}", flush=True)

if __name__ == "__main__":
    print(">>> Launching bot script...", flush=True)
    import bot
    bot.main()
    print(f">>> Found bot.py in: {bot_dir}", flush=True)
    if bot_dir not in sys.path:
        sys.path.insert(0, bot_dir)
    os.chdir(bot_dir)
else:
    print(f">>> CRITICAL: bot.py not found in {search_paths}", flush=True)
    print(f">>> Directory content of {current_dir}: {os.listdir(current_dir)}", flush=True)

if __name__ == "__main__":
    print(">>> Launching bot script...", flush=True)
    import bot
    bot.main()


