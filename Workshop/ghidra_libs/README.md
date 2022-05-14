# External libraries

The aim of this folder is to hold common external libraries required by libraries analyzed with Ghidra.

This folder can be initialzied by executing the script ``unrasp/Workshop/pull_shared_lib.js``, and fulfilled manually by adding missing libraries.

## About the content

This folder is pre-filled with some common libraries from Motorola One Vision running Android 9 (API 29) to help attendees who encountered difficulties to extract it.


## Usage :

Ensure your device/emulator is connected,  move into `unrasp` folder and run :

```
$ cd Workshop
$ rm *.so
$ nodejs pull_shared_lib.js
```