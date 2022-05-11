var Interruptor = require('./lib/android-arm64-strace.min.js').target.LinuxArm64();
var KAPI = Interruptor.KAPI;


Interruptor.newAgentTracer({
    followThread: false
}).startOnLoad(/\.so$/);