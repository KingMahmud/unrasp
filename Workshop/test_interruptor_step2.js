var Interruptor = require('./lib/android-arm64-strace.min.js').target.LinuxArm64();
var KAPI = Interruptor.KAPI;


Interruptor.newAgentTracer({
    followThread: false,
    exclude: {
        syscalls: [/mprotect/,/clock_/]
    }
}).startOnLoad(/a1b2\.so$/,{
    threshold: 1
});