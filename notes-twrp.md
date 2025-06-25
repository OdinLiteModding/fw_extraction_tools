cd minTWRP
export ALLOW_MISSING_DEPENDENCIES=true
. build/envsetup.sh 
lunch twrp_odinlite_6877_fhd_v1-eng
mka recovery -j`nproc`
mka bootimage -j`nproc`
make -j$(nproc --all) recoveryimage

guides:
- https://alaskalinuxuser3.ddns.net/2023/09/19/where-do-i-start-zero-to-twrp-for-a-phone-with-no-custom-roms-or-recovery
  - https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp
  - https://gitlab.com/alaskalinuxuser/device_cat_s42g/-/commit/d70f81bcc4b23484d82cc9ab66163cb258653210
- https://xdaforums.com/t/tool-android-image-kitchen-unpack-repack-kernel-ramdisk-win-android-linux-mac.2073775/
- https://xdaforums.com/t/editing-system-img-inside-super-img-and-flashing-our-modifications.4196625/
- https://gist.github.com/lopestom/a5e6b690028cedd47d7e648a1035b358
- https://gist.github.com/TobidieTopfpflanze/c162f551ffc4a2be21dbd168371ef347
- https://blog.realogs.in/android-device-tree-bringup/
- https://gist.github.com/lopestom/c4a2648958db5c3db03d32033a3583cd#21-parts-of-recovery-ramdisk
- https://gist.github.com/lopestom/a5e6b690028cedd47d7e648a1035b358

random links:
- https://xdaforums.com/t/guide-how-to-port-roms-to-your-device-aosp.2483143/
- https://xdaforums.com/t/guide-how-to-port-roms-to-your-device.1957219/
- https://xdaforums.com/t/guide-how-to-port-different-roms-to-your-device-for-cm-aosp-aokp.2545618/
- https://xdaforums.com/t/guide-porting-roms-between-two-similar-devices.2675345/
- https://xdaforums.com/t/guide-how-to-make-a-device-tree-for-your-phone.3698419/
- https://xdaforums.com/t/how-to-create-device-tree-for-android-rom-building.3498355/
- https://xdaforums.com/t/guide-a-noob-guide-on-building-your-own-custom-kernel-on-win10-arm-arm64-mtk.3775494/
- https://stackoverflow.com/questions/8251741/how-to-speed-up-mm-in-module-making-of-aosp
- https://proandroiddev.com/how-fast-are-your-android-ci-builds-and-why-it-matters-a4309e40981f

tools:
- https://github.com/twrpdtgen/twrpdtgen/tree/master
- https://github.com/osm0sis/Android-Image-Kitchen/tree/AIK-Linux
- https://xdaforums.com/t/tool-android-image-kitchen-unpack-repack-kernel-ramdisk-win-android-linux-mac.2073775/
- https://github.com/PabloCastellano/extract-dtb
- https://github.com/moetayuko/split-appended-dtb
- https://github.com/sebaubuntu-python/aospdtgen/tree/master/aospdtgen
- https://github.com/bkerler/mtkclient
- list - https://github.com/Akipe/awesome-android-aosp?tab=readme-ov-file


TODO:
- nixos ports:
  - AIK + mtkclient