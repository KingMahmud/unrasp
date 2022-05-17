# Workshops

This folder contains as well resources for my workshops than scripts useful against Android RASP.

## 1. Content

Folder :
- **./ghidra_libs/** : contains external shared libraries needed by libraries you will analyze with Ghidra
- **./ghidra_scripts/** : is the folder you will define into to the Ghidra's Script Manager, and who contains some parts of the exercises
- **./frida/** : contains Frida's scripts / template for this workshop
- **./lib/** : contains additional libraries or headers for Frida or Ghidra
- **./tmp/** : temporary folder


Purposes of each file :
- **./run_interruptor.sh** : shell script to test if Frida + Interruptor works with the crackme and the test device
- **./test_interruptor.js** : is the Frida script launched by `run_interruptor.sh` .
- **./pull_shared_libs.js** : a NodeJS script to pull some common libraries from the connected device to `./ghidra_libs` folder.


## 2. Requirements


Choose one of way below :

*recommended*:

- Using Emulator and following config : Pixel 4XL, No Play Store, Android 9.0 Google APIs (API 28) 
- Using Rooted device 

*not recommended for the workshop*:

- Using not rooted device by patching APK with frida gadget (please prepare it before)

Requirements (Work in progress):

1. If you expect to use emulator, install Android Studio and create new ARM64 + Android 9 or 10 virtual device **WITHOUT PLAY STORE**
2. If you expect to use physical device, it must be rooted (or APK must be pactched to embed frida-gadget)
3. Ensure basic requirements are fulfilled :
    1. nodejs >= 14.x : i hightly encourage to use [NVM](https://github.com/nvm-sh/nvm)
    2. frida, frida tools (frida-ps, ...) : `pip install frida frida-tools`
    3. frida-compile : `npm install -g frida-compile`
    4. apktool 
    5. your favorite decompiler/smalifier : r2, baksmali, ghidra, jadx, jeb, ida, ...
4. Clone this repository
5. Move into *unrasp* folder
6. Extract crackme - when it will be availabke - into `Workspace` folder using `apktool`
7. Install the crackme on your test device/emulator
8. Push `frida-server` and configure permissions (`setenforce 0`, ...)
9. Try app, frida and Interruptor setup :
    1. `cd Workspace`
    2. `frida-compile test_interruptor.js -o test_.js && frida -U -l test_.js -f owasp.mstg.uncrackable2`
