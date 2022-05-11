

from __main__ import *
from array import *
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.emulator import EmulatorHelper
from ghidra.program.model.address import AddressSet

monitor = ConsoleTaskMonitor()
emuHelper = EmulatorHelper(currentProgram)
AF = currentProgram.addressFactory
currEmuFn = None


# To convert bytearray to string
def btos(pBytes):
    s = ""
    for x in pBytes:
        if (x > 32) and (x < 127):
            s = s + chr(x)
        else:
            s = "{0}\\x{1:0{2}x}".format(s, x & 0xff, 2)

    return s


# To print the instruction located at pExecAddr
def printInstr(pExecAddr):
    print("Address: 0x{} ({})".format(pExecAddr, getInstructionAt(pExecAddr)))


# To print CPU context of the emulator
def printCpuContext(pEmu, pFilter=None):
    if pFilter != None:
        reg_filter = pFilter
    else:
        reg_filter = ["pc", "x1", "x2", "x3", "x4", "x5", "x7", "x8", "x10", "x25"]

    for reg in reg_filter:
        reg_value = pEmu.readRegister(reg)
        print("  {} = {:#018x}".format(reg, reg_value))

    return

# to run deobfuscateString()  for each  functions/symbols from the current program
def scanProgram():
    symbolTable = currentProgram.getSymbolTable()

    for symbol in symbolTable.getAllSymbols(False):
        func = getFunctionAt(symbol.getAddress())
        if func == None or func.getProgram() == None:
            continue
        iter = func.getProgram().getListing().getCodeUnits(func.getBody(), True)
        deobfuscateString(iter, func.getName())


# to run deobfuscateString()  only for the specified range
def scanAt(pAddressStart, pAddressEnd, pForceEnd=False):
    addressSet = AddressSet(pAddressStart, pAddressEnd)
    iter = currentProgram.getListing().getCodeUnits(addressSet, True)
    if pForceEnd == True:
        deobfuscateString(iter, pAddressStart, pAddressEnd)
    else:
        deobfuscateString(iter, pAddressStart)
