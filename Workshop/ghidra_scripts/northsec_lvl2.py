# TODO write a description for this script
# @author FrenchYeti
# @category _NEW_
# @keybinding RASP, obfuscation, strings
# @menupath
# @toolbar


from __main__ import *
from array import *
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.emulator import EmulatorHelper
from ghidra.program.model.address import AddressSet


REPLACE_STR = False
SCRIPT_NAME = "String_Recover"
CREATE_BOOKMARK = False
CREATE_COMMENT = True
STR_ADDR_BASE = 0x128000
BASE_ADDR = 0x100000
TRACE_EMU = False

START_ADDR = None # Must be a string. "0x10b7e4"
END_ADDR = None # Must be a string.

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

def readMemoryBytes(pAddress, pLen):
    buffer = array('b')
    mm = currentProgram.getMemory()
    offset = 0
    while offset < pLen - 1:
        buffer.append(mm.getByte(pAddress.add(offset)))
        offset = offset + 1

    return buffer

def replaceMemory( pStr, pLen, pFlagAddr, pMemStart):
    i = 0
    print("At {}, write {} (len={})".format( pMemStart, readMemoryBytes(pStr, pLen), pLen))
    # mm = currentProgram.getMemory().getBlock(currentProgram.addressFactory.getAddress(pAddr));
    # while i < pLen:
    #     print(
    #     setByte( AF.getAddress( str(pStr.subtract(pMemStart)+i+BASE_ADDR)), getByte(pStr.add(i)) )
    #     setByte( pFlagAddr, 1)
    #     i = i+1


def mapMemoryRegionContaining(pEmu, pAddrStr):
    dataSeg = currentProgram.getMemory().getBlock(currentProgram.addressFactory.getAddress(pAddrStr))
    buffer = readMemoryBytes(dataSeg.getStart(), dataSeg.getSize())
    pEmu.writeMemory(dataSeg.getStart(), buffer)

    return dataSeg


def deobfuscateString(pCodeUnitIter, pLocName, pAddrEnd=None):
    global currEmuFn
    # c = 0
    # focus = 0
    # obf = 0
    # mode = 1
    flagAddr = None
    dataAddr = None
    startAddr = None
    stopAddr = None
    flagReg = None
    for i in pCodeUnitIter:
        if (i.getMnemonicString() == "ldrb"):
            refs = i.getOperandReferences(1)
            if len(refs) == 0:
                continue

            flagAddr = refs[0].getToAddress()
            if(refs[0].isStackReference() == False):
                if(pAddrEnd != None):
                    print("Not yet implemented")
                else:
                    flagReg = i.getRegister(0)

        elif (i.getMnemonicString() == "tbnz") and ( flagReg != None ):
            if(i.getRegister(0) == flagReg):
                # so, this instruction check flag value,
                startAddr = i.getAddress().add(4)
                stopAddr = i.getOperandReferences(2)[0].getToAddress()
                runEmulator( emuHelper, startAddr, stopAddr, dataAddr, flagAddr, TRACE_EMU)
                print("Run emulator between {} and {}".format(startAddr, stopAddr))



        # ...




def scanProgram():
    symbolTable = currentProgram.getSymbolTable()

    for symbol in symbolTable.getAllSymbols(False):
        func = getFunctionAt(symbol.getAddress())
        if func == None or func.getProgram() == None:
            continue
        iter = func.getProgram().getListing().getCodeUnits(func.getBody(), True)
        deobfuscateString(iter, func.getName())


def scanAt(pAddressStart, pAddressEnd, pForceEnd=False):
    addressSet = AddressSet(pAddressStart, pAddressEnd)
    iter = currentProgram.getListing().getCodeUnits(addressSet, True)
    if pForceEnd == True:
        deobfuscateString(iter, pAddressStart, pAddressEnd)
    else:
        deobfuscateString(iter, pAddressStart)


# To find where char offset is incremented during string deciphering
def searchLenRegister(pEmu, pAddr):
    if pAddr == None:
        return -1

    listing = currentProgram.getListing()
    incr = listing.getCodeUnitAt(pAddr.add(4))
    len = 0
    if (incr.getMnemonicString() == "add"):
        reg = incr.getRegister(0)
        len = pEmu.readRegister(reg)

    return len


# To search "strb" where store location is in the range of encrypted data
def searchStore(pBegin, pEnd, pMemBegin, pMemEnd):
    listing = currentProgram.getListing()
    addr = pBegin
    iLen = 4
    found = False
    target = None# TODO write a description for this script
    loc = None
    # printf("Search store between {} and {} \n".format(pMemBegin, pMemEnd))
    while (addr.equals(pEnd) == False) and (found == False):
        unit = listing.getCodeUnitAt(addr)
        if unit == None:
            print("Error : CodeUnit not found at {} ({} +{})".format(addr, addr.subtract(iLen), o))
            addr = addr.add(iLen)
            continue

        if (unit.getMnemonicString() == "strb"):
            if len(unit.getOperandReferences(1)) > 0:
                to = unit.getOperandReferences(1)[0].getToAddress()
                if (to.subtract(pMemBegin) >= 0) and (to.subtract(pMemEnd) <= 0):
                    loc = unit.getAddress()
                    target = to
                    break

        if (unit.getMnemonicString() == "str"):
            if len(unit.getOperandReferences(1)) > 0:
                to = unit.getOperandReferences(1)[0].getToAddress()
                if (to.subtract(pMemBegin) >= 0) and (to.subtract(pMemEnd) <= 0):
                    loc = unit.getAddress()
                    target = to
                    break

        addr = addr.add(iLen)

    return {'addr': loc, 'data': target}


def runEmulator(pEmu, pStart, pStop, pDump, pFlagAddr, pTrace=False):
    # init PC
    pEmu.writeRegister(pEmu.getPCRegister(), pStart.getUnsignedOffset())

    # reset context ?
    dataSeg = mapMemoryRegionContaining(pEmu, str(hex(STR_ADDR_BASE)))

    while monitor.isCancelled() is False:
        execAddr = pEmu.getExecutionAddress()

        if (pTrace == True):
            printInstr(execAddr)
            printCpuContext(pEmu, ["x8", "w10", "x11", "x25", "x29", "q0", "q1", "q2"])


        if (execAddr == pStop):
            # search where decoded string has been wrote
            outAddr = searchStore(pStart, pStop, dataSeg.getStart(), dataSeg.getStart().add(dataSeg.getSize()))

            if (outAddr == None) or (outAddr['addr'] == None) or (outAddr['data'] == None):
                print("[{}] Error : 0x{}".format(currEmuFn, execAddr) + " location of decoded data has not bee found")
            else:
                len = searchLenRegister(pEmu, outAddr['addr'])
                if len == -1:
                    print("Len is invalid")
                    len = 5

                data = btos(emuHelper.readMemory(outAddr['data'], len))
                print("[{}] from 0x{} . At 0x{} (len:{}) : {}".format(currEmuFn, pStart, outAddr['data'], len, data))

                # create comment
                if REPLACE_STR == True:
                    replaceMemory( outAddr['data'].subtract(len), len, pFlagAddr, dataSeg.getStart())

                if CREATE_COMMENT == True:
                    currentProgram.getListing().setComment(outAddr['data'],
                                                           ghidra.program.model.listing.CodeUnit.REPEATABLE_COMMENT,
                                                           "{}".format(data))

            return

        success = pEmu.step(monitor)

        if (success == False):
            lastError = pEmu.getLastError()
            printerr(
                "Error at 0x{} (from: 0x{} , to: 0x{} ): {}".format(pEmu.readRegister("pc"), pStart, pStop, lastError))
            return

    pEmu.dispose()



if START_ADDR != None and END_ADDR != None:
    scanAt(AF.getAddress(START_ADDR), AF.getAddress(END_ADDR), True)
else:
    scanProgram()
