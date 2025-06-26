import subprocess
import logging
from pathlib import Path

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# --- Consts: File names and paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

DUMPS_DIR = (PROJECT_DIR / "dumps/device").resolve()
STDOUT_DUMPS = [
    ("adb shell getprop", "getprop"),
    ("adb shell readelf -d system/bin/vold", "readelf_vold"),
    ("adb shell cat /proc/partitions", "partitions"),
    ("adb shell ls -l /dev/block/by-name", "block_by_name")
]


# --- Main ---
def main():
    logger.info("=== Starting extraction pipeline ===")
    DUMPS_DIR.mkdir(exist_ok=True, parents=True)
    
    for (cmd, fname) in STDOUT_DUMPS:
        OUTPUT_PATH = DUMPS_DIR / fname

        if not OUTPUT_PATH.exists():
            logger.info(f"Running: {cmd}")
            result = subprocess.run(cmd.split(" "), capture_output=True, text=True, check=True)

            OUTPUT_PATH.write_text(result.stdout)

    logger.info("=== Pipeline completed successfully ===")

if __name__ == "__main__":
    main()