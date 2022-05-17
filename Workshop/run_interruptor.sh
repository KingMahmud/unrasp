#!/usr/bin/env bash

frida-compile ./test_interruptor.js -o tmp/test_interruptor.js && frida -U -l tmp/test_interruptor.js -f owasp.mstg.uncrackable2
