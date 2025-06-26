import os
import shutil
import subprocess
import tarfile
import zipfile
import logging
from pathlib import Path
from getpass import getuser

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# --- Consts: File names and paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

AIK_ARCHIVE = (PROJECT_DIR / "tools/AIK-Linux-v3.8-ALL.tar.gz").resolve()
AIK_DIR = (PROJECT_DIR / "AIK-Linux").resolve()

FIRMWARE_ID = "12fss4yfklnQssaAWEPjmuelzfivu4EuL"
FIRMWARE_ZIP = (PROJECT_DIR / "assets/Lite M2.zip").resolve()
FIRMWARE_DIR = (PROJECT_DIR / "assets/Lite M2/odinlite_6877_fhd_v1_20221202").resolve()

DUMPS_DIR = (PROJECT_DIR / "dumps").resolve()
TWRPDTGEN_DIR = (PROJECT_DIR / "twrpdtgen").resolve()

# --- Consts: Props ---
USERNAME = getuser()
FILES_TO_DUMP = ["boot.img", "super.img"]
SUPER_PARTS = ["system", "vendor", "product"]
SLOT_SUFFIX = "_a"

# --- ENV Setup ---
os.environ["ENVFS_RESOLVE_ALWAYS"] = "1"

# --- Utility Functions ---
def run(cmd, **kwargs):
    logger.info("Running: %s", " ".join(cmd))
    subprocess.run(cmd, check=True, **kwargs)

def safe_extract_tar(tar_path: Path, dest_dir: Path):
    logger.info("Extracting TAR: %s → %s", tar_path, dest_dir)
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=dest_dir, filter="data")

def safe_extract_zip(zip_path: Path, dest_dir: Path):
    logger.info("Extracting ZIP: %s → %s", zip_path, dest_dir)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

# --- Pipeline Steps ---
def print_consts():
    logger.info("--- Constants ---")
    
    for name, val in [
        ("SCRIPT_DIR", SCRIPT_DIR), ("PROJECT_DIR", PROJECT_DIR),
        ("AIK_ARCHIVE", AIK_ARCHIVE), ("AIK_DIR", AIK_DIR),
        ("FIRMWARE_ID", FIRMWARE_ID), ("FIRMWARE_ZIP", FIRMWARE_ZIP), ("FIRMWARE_DIR", FIRMWARE_DIR),
        ("DUMPS_DIR", DUMPS_DIR), ("TWRPDTGEN_DIR", TWRPDTGEN_DIR),
        ("USERNAME", USERNAME), ("FILES_TO_DUMP", FILES_TO_DUMP),
        ("SUPER_PARTS", SUPER_PARTS), ("SLOT_SUFFIX", SLOT_SUFFIX)
    ]:
        logger.info("%s: %s", name, val)
    logger.info("-----------------")


def prepare_aik():
    if not AIK_DIR.exists():
        safe_extract_tar(AIK_ARCHIVE, PROJECT_DIR)
    else:
        logger.info("AIK-Linux already extracted at %s", AIK_DIR)

def download_firmware():
    if not FIRMWARE_ZIP.exists():
        FIRMWARE_ZIP.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Downloading firmware to %s", FIRMWARE_ZIP)
        import gdown
        gdown.download(id=FIRMWARE_ID, output=str(FIRMWARE_ZIP), quiet=False)
    else:
        logger.info("Firmware already exists: %s", FIRMWARE_ZIP)

def extract_firmware():
    if not FIRMWARE_DIR.exists():
        safe_extract_zip(FIRMWARE_ZIP, FIRMWARE_ZIP.parent)
    else:
        logger.info("Firmware already extracted at %s", FIRMWARE_DIR)

def copy_to_dumps():
    DUMPS_DIR.mkdir(parents=True, exist_ok=True)

    for fname in FILES_TO_DUMP:
        src = FIRMWARE_DIR / fname
        dst = DUMPS_DIR / fname

        if not dst.exists():
            logger.info("Copying %s → %s", src, dst)
            shutil.copy(src, dst)
        else:
            logger.info("Already copied: %s", dst)


def unpack_super_image():
    super_img = DUMPS_DIR / "super.img"
    super_ext4 = DUMPS_DIR / "super.ext4.img"

    if not super_ext4.exists():
        run(["simg2img", str(super_img), str(super_ext4)], cwd=DUMPS_DIR)
    else:
        logger.info("super.ext4.img already exists")

    extracted_flag = DUMPS_DIR / f"system{SLOT_SUFFIX}.img"
    if not extracted_flag.exists():
        run(["lpunpack", str(super_ext4)], cwd=DUMPS_DIR)
    else:
        logger.info("Super.ext4.img already unpacked")

def extract_super_parts():
    for part in SUPER_PARTS:
        img_file = DUMPS_DIR / f"{part}{SLOT_SUFFIX}.img"
        out_dir = DUMPS_DIR / part
        mount_point = DUMPS_DIR / f"{part}_mnt"

        if not out_dir.exists():
            out_dir.mkdir()
            mount_point.mkdir()

            try:
                logger.info("Mounting %s to %s", img_file, mount_point)
                run(["sudo", "mount", "-o", "loop", str(img_file), str(mount_point)])
                run(["sudo", "cp", "-a", f"{mount_point}/.", str(out_dir)])
            finally:
                logger.info("Unmounting %s", mount_point)
                run(["sudo", "umount", str(mount_point)])
                mount_point.rmdir()
        else:
            logger.info("Partition %s already extracted", img_file)


def unpack_ramdisk():
    ramdisk_dir = AIK_DIR / "ramdisk"
    if not ramdisk_dir.exists():
        run([str(AIK_DIR / "unpackimg.sh"), str(DUMPS_DIR / "boot.img")], stdout=subprocess.DEVNULL)
    else:
        logger.info("Ramdisk already unpacked at %s", ramdisk_dir)

def run_twrpdtgen():
    output_dir = TWRPDTGEN_DIR / "output"
    if not output_dir.exists():
        TWRPDTGEN_DIR.mkdir(parents=True, exist_ok=True)
        run(["python3", "-m", "twrpdtgen", str(DUMPS_DIR / "boot.img")], cwd=TWRPDTGEN_DIR, stdout=subprocess.DEVNULL)
    else:
        logger.info("TWRP skeleton already exists at %s", output_dir)

def fix_permissions():
    logger.info("Fixing ownership to %s", USERNAME)
    for path in [FIRMWARE_ZIP.parent, AIK_DIR, DUMPS_DIR, TWRPDTGEN_DIR]:
        run(["sudo", "chown", "-R", USERNAME, str(path)])

# --- Main ---
def main():
    logger.info("=== Starting extraction pipeline ===")
    print_consts()
    prepare_aik()
    download_firmware()
    extract_firmware()
    copy_to_dumps()
    unpack_super_image()
    extract_super_parts()
    unpack_ramdisk()
    run_twrpdtgen()
    fix_permissions()
    logger.info("=== Pipeline completed successfully ===")

if __name__ == "__main__":
    main()