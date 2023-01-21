#!/usr/bin/env python3
import os
import sys
import json

def BuildFlashMenu(name, flashsize, fssizelist):
    for fssize in fssizelist:
        if fssize == 0:
            fssizename = "no FS"
        elif fssize < 1024 * 1024:
            fssizename = "Sketch: %dKB, FS: %dKB" % ((flashsize - fssize) / 1024, fssize / 1024)
        else:
            fssizename = "Sketch: %dMB, FS: %dMB" % ((flashsize - fssize) / (1024 * 1024), fssize / (1024 * 1024))
        mn="%d_%d" % (flashsize, fssize)
        print("%s.menu.flash.%s=%dMB (%s)" % (name, mn, flashsize / (1024 * 1024), fssizename))
        print("%s.menu.flash.%s.upload.maximum_size=%d" % (name, mn, flashsize - 4096 - fssize))
        print("%s.menu.flash.%s.build.flash_length=%d" % (name, mn, flashsize - 4096 - fssize))
        print("%s.menu.flash.%s.build.eeprom_start=%d" % (name, mn, int("0x10000000",0) + flashsize - 4096))
        print("%s.menu.flash.%s.build.fs_start=%d" % (name, mn, int("0x10000000",0) + flashsize - 4096 - fssize))
        print("%s.menu.flash.%s.build.fs_end=%d" % (name, mn, int("0x10000000",0) + flashsize - 4096))

def BuildDebugPort(name):
    print("%s.menu.dbgport.Disabled=Disabled" % (name))
    print("%s.menu.dbgport.Disabled.build.debug_port=" % (name))
    for p in ["Serial", "Serial1", "Serial2"]:
        print("%s.menu.dbgport.%s=%s" % (name, p, p))
        print("%s.menu.dbgport.%s.build.debug_port=-DDEBUG_RP2040_PORT=%s" % (name, p, p))

def BuildDebugLevel(name):
    for l in [ ("None", ""), ("Core", "-DDEBUG_RP2040_CORE"), ("SPI", "-DDEBUG_RP2040_SPI"), ("Wire", "-DDEBUG_RP2040_WIRE"),
               ("All", "-DDEBUG_RP2040_WIRE -DDEBUG_RP2040_SPI -DDEBUG_RP2040_CORE"), ("NDEBUG", "-DNDEBUG") ]:
        print("%s.menu.dbglvl.%s=%s" % (name, l[0], l[0]))
        print("%s.menu.dbglvl.%s.build.debug_level=%s" % (name, l[0], l[1]))

def BuildFreq(name):
    for f in [ 133,  50, 100, 120, 125, 150, 175, 200, 225, 240, 250, 275, 300]:
        warn = ""
        if f > 133: warn = " (Overclock)"
        print("%s.menu.freq.%s=%s MHz%s" % (name, f, f, warn))
        print("%s.menu.freq.%s.build.f_cpu=%dL" % (name, f, f * 1000000))

def BuildOptimize(name):
    for l in [ ("Small", "Small", "-Os", " (standard)"), ("Optimize", "Optimize", "-O", ""), ("Optimize2", "Optimize More", "-O2", ""),
               ("Optimize3", "Optimize Even More", "-O3", ""), ("Fast", "Fast", "-Ofast", " (maybe slower)"), ("Debug", "Debug", "-Og", "") ]:
        print("%s.menu.opt.%s=%s (%s)%s" % (name, l[0], l[1], l[2], l[3]))
        print("%s.menu.opt.%s.build.flags.optimize=%s" % (name, l[0], l[2]))

def BuildRTTI(name):
    print("%s.menu.rtti.Disabled=Disabled" % (name))
    print("%s.menu.rtti.Disabled.build.flags.rtti=-fno-rtti" % (name))
    print("%s.menu.rtti.Enabled=Enabled" % (name))
    print("%s.menu.rtti.Enabled.build.flags.rtti=" % (name))

def BuildStackProtect(name):
    print("%s.menu.stackprotect.Disabled=Disabled" % (name))
    print("%s.menu.stackprotect.Disabled.build.flags.stackprotect=" % (name))
    print("%s.menu.stackprotect.Enabled=Enabled" % (name))
    print("%s.menu.stackprotect.Enabled.build.flags.stackprotect=-fstack-protector" % (name))

def BuildExceptions(name):
    print("%s.menu.exceptions.Disabled=Disabled" % (name))
    print("%s.menu.exceptions.Disabled.build.flags.exceptions=-fno-exceptions" % (name))
    print("%s.menu.exceptions.Disabled.build.flags.libstdcpp=-lstdc++" % (name))
    print("%s.menu.exceptions.Enabled=Enabled" % (name))
    print("%s.menu.exceptions.Enabled.build.flags.exceptions=-fexceptions" % (name))
    print("%s.menu.exceptions.Enabled.build.flags.libstdcpp=-lstdc++-exc" % (name))

def BuildBoot(name):
    for l in [ ("Generic SPI /2", "boot2_generic_03h_2_padded_checksum"),  ("Generic SPI /4", "boot2_generic_03h_4_padded_checksum"),
            ("IS25LP080 QSPI /2", "boot2_is25lp080_2_padded_checksum"), ("IS25LP080 QSPI /4", "boot2_is25lp080_4_padded_checksum"),
            ("W25Q080 QSPI /2", "boot2_w25q080_2_padded_checksum"), ("W25Q080 QSPI /4", "boot2_w25q080_4_padded_checksum"),
            ("W25X10CL QSPI /2", "boot2_w25x10cl_2_padded_checksum"), ("W25X10CL QSPI /4", "boot2_w25x10cl_4_padded_checksum"),
            ("W25Q64JV QSPI /4", "boot2_w25q64jv_4_padded_checksum"), ("W25Q16JVxQ QSPI /4", "boot2_w25q16jvxq_4_padded_checksum") ]:
        print("%s.menu.boot2.%s=%s" % (name, l[1], l[0]))
        print("%s.menu.boot2.%s.build.boot2=%s" % (name, l[1], l[1]))

def BuildUSBStack(name):
    print("%s.menu.usbstack.picosdk=Pico SDK" % (name))
    print('%s.menu.usbstack.picosdk.build.usbstack_flags=' % (name))
    print("%s.menu.usbstack.tinyusb=Adafruit TinyUSB" % (name))
    print('%s.menu.usbstack.tinyusb.build.usbstack_flags=-DUSE_TINYUSB "-I{runtime.platform.path}/libraries/Adafruit_TinyUSB_Arduino/src/arduino"' % (name))
    print("%s.menu.usbstack.nousb=No USB" % (name))
    print('%s.menu.usbstack.nousb.build.usbstack_flags="-DNO_USB -DDISABLE_USB_SERIAL -I{runtime.platform.path}/tools/libpico"' % (name))

def BuildCountry(name):
    countries = [ "Worldwide", "Australia", "Austria", "Belgium", "Brazil", "Canada", "Chile", "China", "Colombia", "Czech Republic",
                  "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hong Kong", "Hungary", "Iceland", "India", "Israel",
                  "Italy", "Japan", "Kenya", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malaysia", "Malta", "Mexico",
                  "Netherlands", "New Zealand", "Nigeria", "Norway", "Peru", "Philippines", "Poland", "Portugal", "Singapore", "Slovakia",
                  "Slovenia", "South Africa", "South Korea", "Spain", "Sweden", "Switzerland", "Taiwan", "Thailand", "Turkey", "UK", "USA"]
    for c in countries:
        sane = c.replace(" ", "_").upper()
        print("%s.menu.wificountry.%s=%s" % (name, sane.lower(), c))
        print("%s.menu.wificountry.%s.build.wificc=-DWIFICC=CYW43_COUNTRY_%s" % (name, sane.lower(), sane))

def BuildIPStack(name):
    print("%s.menu.ipstack.ipv4only=IPv4 Only" % (name))
    print('%s.menu.ipstack.ipv4only.build.libpico=libpico.a' % (name))
    print('%s.menu.ipstack.ipv4only.build.lwipdefs=-DLWIP_IPV6=0 -DLWIP_IPV4=1' % (name))
    print("%s.menu.ipstack.ipv4ipv6=IPv4 and IPv6" % (name))
    print('%s.menu.ipstack.ipv4ipv6.build.libpico=libpico-ipv6.a' % (name))
    print('%s.menu.ipstack.ipv4ipv6.build.lwipdefs=-DLWIP_IPV6=1 -DLWIP_IPV4=1' % (name))

def BuildUploadMethodMenu(name):
    for a, b, c, d, e, f in [ ["default", "Default (UF2)", 256, "picoprobe.tcl", "uf2conv", "uf2conv-network"],
                              ["picotool", "Picotool", 256, "picoprobe.tcl", "picotool", None],
                              ["picoprobe", "Picoprobe", 256, "picoprobe.tcl", "picoprobe", None],
                              ["picodebug", "Pico-Debug", 240, "picodebug.tcl", "picodebug", None] ]:
        print("%s.menu.uploadmethod.%s=%s" % (name, a, b))
        print("%s.menu.uploadmethod.%s.build.ram_length=%dk" % (name, a, c))
        print("%s.menu.uploadmethod.%s.build.debugscript=%s" % (name, a, d))
        # For pico-debug, need to disable USB unconditionally
        if a == "picodebug":
            print("%s.menu.uploadmethod.%s.build.picodebugflags=-UUSE_TINYUSB -DNO_USB -DDISABLE_USB_SERIAL -I{runtime.platform.path}/tools/libpico" % (name, a))
        elif a == "picotool":
            print("%s.menu.uploadmethod.%s.build.picodebugflags=-DENABLE_PICOTOOL_USB" % (name, a))
        print("%s.menu.uploadmethod.%s.upload.maximum_data_size=%d" % (name, a, c * 1024))
        print("%s.menu.uploadmethod.%s.upload.tool=%s" % (name, a, e))
        print("%s.menu.uploadmethod.%s.upload.tool.default=%s" % (name, a, e))
        if f != None:
            print("%s.menu.uploadmethod.%s.upload.tool.network=%s" % (name, a, f))

def BuildHeader(name, vendor_name, product_name, vid, pid, pwr, boarddefine, variant, flashsize, boot2, extra):
    prettyname = vendor_name + " " + product_name
    print()
    print("# -----------------------------------")
    print("# %s" % (prettyname))
    print("# -----------------------------------")
    print("%s.name=%s" % (name, prettyname))
    usb = 0
    if type(pid) == list:
        for tp in pid:
            print("%s.vid.%d=%s" % (name, usb, vid))
            print("%s.pid.%d=0x%04x" % (name, usb, int(tp, 16)))
            usb = usb + 1
    else:
        for kb in [ "0", "0x8000" ]:
            for ms in [ "0", "0x4000" ]:
                for jy in [ "0", "0x0100" ]:
                    thispid = int(pid, 16) | int(kb, 16) | int(ms, 16) | int(jy, 16)
                    print("%s.vid.%d=%s" % (name, usb, vid))
                    print("%s.pid.%d=0x%04x" % (name, usb, thispid))
                    usb = usb + 1
    if type(pid) == list:
        print("%s.build.usbpid=-DSERIALUSB_PID=%s" % (name, pid[0]))
    else:
        print("%s.build.usbpid=-DSERIALUSB_PID=%s" % (name, pid))
    print("%s.build.usbpwr=-DUSBD_MAX_POWER_MA=%s" % (name, pwr))
    print("%s.build.board=%s" % (name, boarddefine))
    print("%s.build.mcu=cortex-m0plus" % (name))
    print("%s.build.variant=%s" % (name, variant))
    print("%s.upload.maximum_size=%d" % (name, flashsize))
    print("%s.upload.wait_for_upload_port=true" % (name))
    print("%s.upload.erase_cmd=" % (name))
    print("%s.serial.disableDTR=false" % (name))
    print("%s.serial.disableRTS=false" % (name))
    print("%s.build.f_cpu=125000000" % (name))
    print("%s.build.led=" % (name))
    print("%s.build.core=rp2040" % (name))
    print("%s.build.ldscript=memmap_default.ld" % (name))
    print("%s.build.boot2=%s" % (name, boot2))
    print("%s.build.vid=%s" % (name, vid))
    if type(pid) == list:
        print("%s.build.pid=%s" % (name, pid[0]))
    else:
        print("%s.build.pid=%s" % (name, pid))
    print('%s.build.usb_manufacturer="%s"' % (name, vendor_name))
    print('%s.build.usb_product="%s"' % (name, product_name))
    if extra != None:
        m_extra = ''
        for m_item in extra:
            m_extra += '-D' + m_item + ' '
        print('%s.build.extra_flags=%s' % (name, m_extra.rstrip()))

def WriteWarning():
    print("# WARNING - DO NOT EDIT THIS FILE, IT IS MACHINE GENERATED")
    print("#           To change something here, edit tools/makeboards.py and")
    print("#           run 'python3 makeboards.py > ../boards.txt' to regenerate")
    print()

def BuildGlobalMenuList():
    print("menu.BoardModel=Model")
    print("menu.flash=Flash Size")
    print("menu.freq=CPU Speed")
    print("menu.opt=Optimize")
    print("menu.rtti=RTTI")
    print("menu.stackprotect=Stack Protector")
    print("menu.exceptions=C++ Exceptions")
    print("menu.dbgport=Debug Port")
    print("menu.dbglvl=Debug Level")
    print("menu.boot2=Boot Stage 2")
    print("menu.wificountry=WiFi Region")
    print("menu.usbstack=USB Stack")
    print("menu.ipstack=IP Stack")
    print("menu.uploadmethod=Upload Method")

def MakeBoard(name, vendor_name, product_name, vid, pid, pwr, boarddefine, flashsizemb, boot2, extra = None):
    fssizelist = [ 0, 64 * 1024, 128 * 1024, 256 * 1024, 512 * 1024 ]
    for i in range(1, flashsizemb):
        fssizelist.append(i * 1024 * 1024)
    BuildHeader(name, vendor_name, product_name, vid, pid, pwr, boarddefine, name, flashsizemb * 1024 * 1024, boot2, extra)
    if name == "generic":
        BuildFlashMenu(name, 2*1024*1024, [0, 1*1024*1024])
        BuildFlashMenu(name, 4*1024*1024, [0, 2*1024*1024])
        BuildFlashMenu(name, 8*1024*1024, [0, 4*1024*1024])
        BuildFlashMenu(name, 16*1024*1024, [0, 8*1024*1024])
    else:
        BuildFlashMenu(name, flashsizemb * 1024 * 1024, fssizelist)
    BuildFreq(name)
    BuildOptimize(name)
    BuildRTTI(name)
    BuildStackProtect(name)
    BuildExceptions(name)
    BuildDebugPort(name)
    BuildDebugLevel(name)
    BuildUSBStack(name)
    if name == "rpipicow":
        BuildCountry(name)
    BuildIPStack(name)
    if name == "generic":
        BuildBoot(name)
    BuildUploadMethodMenu(name)
    MakeBoardJSON(name, vendor_name, product_name, vid, pid, pwr, boarddefine, flashsizemb, boot2, extra)
    
def MakeBoardJSON(name, vendor_name, product_name, vid, pid, pwr, boarddefine, flashsizemb, boot2, extra):
    if type(pid) == list:
        pid = pid[0]
    if extra != None:
        m_extra = ' '
        for m_item in extra:
            m_extra += '-D' + m_item + ' '
    else:
        m_extra = ''
    json = """{
  "build": {
    "arduino": {
      "earlephilhower": {
        "boot2_source": "BOOT2.S",
        "usb_vid": "VID",
        "usb_pid": "PID"
      }
    },
    "core": "earlephilhower",
    "cpu": "cortex-m0plus",
    "extra_flags": "-D ARDUINO_BOARDDEFINE -DARDUINO_ARCH_RP2040 -DUSBD_MAX_POWER_MA=USBPWR EXTRA_INFO",
    "f_cpu": "133000000L",
    "hwids": [
      [
        "0x2E8A",
        "0x00C0"
      ],
      [
        "VID",
        "PID"
      ]
    ],
    "mcu": "rp2040",
    "variant": "VARIANTNAME"
  },
  "debug": {
    "jlink_device": "RP2040_M0_0",
    "openocd_target": "rp2040.cfg",
    "svd_path": "rp2040.svd"
  },
  "frameworks": [
    "arduino"
  ],
  "name": "PRODUCTNAME",
  "upload": {
    "maximum_ram_size": 270336,
    "maximum_size": FLASHSIZE,
    "require_upload_port": true,
    "native_usb": true,
    "use_1200bps_touch": true,
    "wait_for_upload_port": false,
    "protocol": "picotool",
    "protocols": [
      "cmsis-dap",
      "jlink",
      "raspberrypi-swd",
      "picotool",
      "picoprobe"
    ]
  },
  "url": "https://www.raspberrypi.org/products/raspberry-pi-pico/",
  "vendor": "VENDORNAME"
}\n"""\
.replace('VARIANTNAME', name)\
.replace('BOARDDEFINE', boarddefine)\
.replace('BOOT2', boot2)\
.replace('VID', vid.upper().replace("X", "x"))\
.replace('PID', pid.upper().replace("X", "x"))\
.replace('VENDORNAME', vendor_name)\
.replace('PRODUCTNAME', product_name)\
.replace('FLASHSIZE', str(1024*1024*flashsizemb))\
.replace('USBPWR', str(pwr))\
.replace(' EXTRA_INFO', m_extra.rstrip())
    jsondir = os.path.abspath(os.path.dirname(__file__)) + "/json"
    f = open(jsondir + "/" + name + ".json", "w")
    f.write(json)
    f.close()

sys.stdout = open(os.path.abspath(os.path.dirname(__file__)) + "/../boards.txt", "w")
WriteWarning()
BuildGlobalMenuList()

# Raspberry Pi
# MakeBoard("rpipico", "Raspberry Pi", "Pico", "0x2e8a", "0x000a", 250, "RASPBERRY_PI_PICO", 2, "boot2_w25q080_2_padded_checksum")
# MakeBoard("rpipicow", "Raspberry Pi", "Pico W", "0x2e8a", "0xf00a", 250, "RASPBERRY_PI_PICO_W", 2, "boot2_w25q080_2_padded_checksum")

# CanSat Primary Mission
MakeBoard("cansat_primary", "Arctos", "Primary Mission", "0x2e8a", "0x000a", 250, "RASPBERRY_PI_PICO", 16, "boot2_w25q080_2_padded_checksum")

# Firefly Telemetry Unit V2
MakeBoard("firefly_telems_v2", "Firefly", "Telemetry Unit V2", "0x2e8a", "0x000a", 250, "RASPBERRY_PI_PICO", 16, "boot2_w25q080_2_padded_checksum")

# Generic
# MakeBoard("generic", "Generic", "RP2040", "0x2e8a", "0xf00a", 250, "GENERIC_RP2040", 16, "boot2_generic_03h_4_padded_checksum")

sys.stdout.close()
