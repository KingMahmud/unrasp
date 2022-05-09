/**
 * This is script is a part of Workshop NSEC2022  material
 *
 * @copyright Reversense 2020 - 2022
 * @author Georges-Bastien Michel (yeti@0xff.ninja)
 */

const _ps_ = require("node:child_process");
const _fs_ = require("node:fs");
const _path_ = require("node:path");
const { cwd } = require("node:process");

// ======== config ========

const SHARED_LIBS = [
    "ld-android.so",
    "libandroid.so",
    "libandroid_runtime.so",
    "libandroidfw.so",
    "libart.so",
    "libbinder.so",
    "libc++.so",
    "libc.so",
    "libcutils.so",
    "libdl.so",
    "libgui.so",
    "libinput.so",
    "liblog.so",
    "libm.so",
    "libnetd_client.so",
    "libsensor.so",
    "libui.so",
    "libutils.so",
    "libz.so"
];

const DEST_FOLDER = _path_.join( cwd(), "ghidra_libs");


// ======== script ========

let res = null;

if(!_fs_.existsSync(DEST_FOLDER)){
    _fs_.mkdirSync(DEST_FOLDER);
}

SHARED_LIBS.map( pLibs => {
    res = _ps_.spawnSync("adb", ["pull","/system/lib64/"+pLibs, _path_.join(DEST_FOLDER,pLibs)], {cwd: cwd() });
    console.log(res.stdout.toString());
});


