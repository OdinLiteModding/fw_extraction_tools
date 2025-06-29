# Android device dump files for alps odinlite_6877_fhd_v1 (odinlite_6877_fhd_v1)

## Device Specifications Odin Lite (M2)
| Basic                   | Spec                                                                         |
| ----------------------- | :--------------------------------------------------------------------------- |
| SoC                     | MediaTek Dimensity 900 (MT6877)                                              |
| CPU                     | 2 x 2.4 GHz Cortex-A78 & 6 x 2.0 GHz Cortex-A55                              |
| GPU                     | Mali-G68 MC4                                                                 |
| Memory                  | 4GB / 6GB                                                                    |
| Shipped Android version | 11                                                                           |
| Storage                 | 64GB / 128GB                                                                 |
| Battery                 | Non-removable Li-Po 6600 mAh                                                 |
| Display Size            | 6 inches                                                                     |
| Display Resolution      | 1920 x 1080 pixels, 16:9 ratio                                               |

## Build
```sh
mkdir -p minTWRP
cd minTWRP
repo init --depth=1 -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp.git -b twrp-11
repo sync

export ALLOW_MISSING_DEPENDENCIES=true
. build/envsetup.sh 
lunch twrp_odinlite_6877_fhd_v1-eng
mka clean
mka recovery -j`nproc` && mka bootimage -j`nproc`
```

## Flash
```sh
fastboot flash boot_a out/target/product/odinlite_6877_fhd_v1/boot.img && fastboot set_active a && fastboot reboot
```

or 

```sh
adb push out/target/product/odinlite_6877_fhd_v1/boot.img /tmp/
```

## TWRP Checklist
Blocking checks
- [x] Correct screen/recovery size
- [x] Working Touch, screen
- [x] Backup to internal/microSD
- [x] Restore from internal/microSD
- [x] reboot to system
- [x] ADB

Medium checks
- [ ] update.zip sideload
- [x] UI colors (red/blue inversions)
- [x] Screen goes off and on
- [x] F2FS/EXT4 Support, exFAT/NTFS where supported
- [x] all important partitions listed in mount/backup lists
- [ ] backup/restore to/from external (USB-OTG) storage (not supported by the device)
- [ ] backup/restore to/from adb (https://gerrit.omnirom.org/#/c/15943/)
- [x] decrypt /data
- [x] Correct date

Minor checks
- [x] MTP export
- [x] reboot to bootloader
- [x] reboot to recovery
- [x] poweroff
- [x] battery level
- [x] temperature
- [ ] encrypted backups
- [ ] input devices via USB (USB-OTG) - keyboard, mouse and disks (not supported by the device)
- [ ] USB mass storage export
- [x] set brightness
- [x] vibrate
- [x] screenshot
- [ ] partition SD card

## TODO
TODO:
- [ ] Port AIK and twrpdtgen to nixos for native flake support
- [ ] Wrtie docs
- [x] Fix scripts (broken paths)
- [x] Fix FBE
- [ ] Move to orange fox
- [ ] Fix adaptable storage encryption
- [ ] Fix system partition access (persist, nvcfg, Protect_F ...)
- [ ] Github actions/Drone builds
- [ ] AWS backed cold build VPS