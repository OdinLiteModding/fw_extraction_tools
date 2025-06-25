import os
import gdown
import zipfile
import tarfile
import shutil
import subprocess

# Enable envfs
os.environ["ENVFS_RESOLVE_ALWAYS"] = "1"

# Unpack AIK-Linux
aik_path = "tools/AIK-Linux-v3.8-ALL.tar.gz"
aik_dir = "AIK-Linux"

if not os.path.isdir(aik_dir):
    with tarfile.open(aik_path, "r:gz") as tar:
        tar.extractall()

# Download lite M2 firmware: https://www.ayntec.com/pages/software
firmware_path = 'assets/Lite M2.zip'
firmware_dir = os.path.dirname(firmware_path)

id = "12fss4yfklnQssaAWEPjmuelzfivu4EuL"

if not os.path.isfile(firmware_path):
    os.makedirs(firmware_dir, exist_ok=True)
    gdown.download(id=id, output=firmware_path, quiet=False)

    with zipfile.ZipFile(firmware_path, 'r') as zip_ref:
        zip_ref.extractall(firmware_dir)

# Copy files to dumps
dumps_dir = "dumps"

if not os.path.isdir(dumps_dir):
    os.makedirs(dumps_dir, exist_ok=True)

    source_dir = "assets/Lite M2/odinlite_6877_fhd_v1_20221202"
    files_to_copy = ["boot.img", "super.img"]

    for file_name in files_to_copy:
        src_path = os.path.join(source_dir, file_name)
        dst_path = os.path.join(dumps_dir, file_name)
        
        shutil.copy(src_path, dst_path)

# Fixup sparse super.img and extract
if not os.path.isfile(os.path.join(dumps_dir, "super.ext4.img")):
    subprocess.run(["simg2img", "super.img", "super.ext4.img"], cwd=dumps_dir, check=True)

if not os.path.isfile(os.path.join(dumps_dir, "system_a.img")):
    subprocess.run(["lpunpack", "super.ext4.img"], cwd=dumps_dir, check=True)

# Mount and copy system, vendor and product partitions
partitions_to_extract = ["system", "vendor", "product"]
slot_suffix = "_a"

for part in partitions_to_extract:
    part_file = os.path.join(dumps_dir, f"{part}{slot_suffix}.img")
    part_dir = os.path.join(dumps_dir, part)
    mount_point = os.path.join(dumps_dir, f"{part}_mnt")

    if not os.path.isdir(part_dir):
        os.makedirs(part_dir, exist_ok=True)
        os.makedirs(mount_point, exist_ok=True)

        subprocess.run(
            ["sudo", "mount", "-o", "loop", part_file, mount_point],
            check=True
        )

        try:
            subprocess.run(
                ["sudo", "cp", "-a", os.path.join(mount_point, "."), part_dir],
                check=True
            )
        finally:
            subprocess.run(
                ["sudo", "umount", mount_point],
                check=True
            )
            os.rmdir(mount_point)

# Unpack boot.img with AIK
if not os.path.isdir(os.path.join(aik_dir, "ramdisk")):
    subprocess.run(
        [os.path.join(aik_dir, "unpackimg.sh"), os.path.join(dumps_dir, "boot.img")],
        check=True
    )

# Generate tree with twrpdtgen
twrpdtgen_dir = "twrpdtgen"

if (not os.path.isdir(twrpdtgen_dir)) or (not os.path.isdir(os.path.join(twrpdtgen_dir, "output"))):
    os.makedirs(twrpdtgen_dir, exist_ok=True)

    subprocess.run(
        ["python3", "-m", "twrpdtgen", os.path.join("..", dumps_dir, "boot.img")],
        cwd=twrpdtgen_dir,
        check=True
    )

# Fixup the permissions due to root usage
folders_to_fixup = [firmware_dir, aik_dir, dumps_dir, twrpdtgen_dir]
username = "frankoslaw"

for folder in folders_to_fixup:
    subprocess.run(
        ["sudo", "chown", "-R", username, folder],
        check=True
    )