#pragma once

// Pin definitions taken from:
//    https://datasheets.raspberrypi.org/pico/pico-datasheet.pdf


// LEDs
#define PIN_LED        (5u)

// Serial
#define PIN_SERIAL1_TX (16u)
#define PIN_SERIAL1_RX (17u)

#define PIN_SERIAL2_TX (8u)
#define PIN_SERIAL2_RX (9u)

// SPI
#define PIN_SPI0_MISO  (0u)
#define PIN_SPI0_MOSI  (3u)
#define PIN_SPI0_SCK   (2u)
#define PIN_SPI0_SS    (1u)

#define PIN_SPI1_MISO  (12u)
#define PIN_SPI1_MOSI  (15u)
#define PIN_SPI1_SCK   (14u)
#define PIN_SPI1_SS    (13u)

// Wire
#define PIN_WIRE0_SDA  (24u)
#define PIN_WIRE0_SCL  (25u)

#define PIN_WIRE1_SDA  (22u)
#define PIN_WIRE1_SCL  (23u)

// Custom functions
#define CAN_INT	       (4u)

// GPS module
#define GPS_TX         (20u)
#define GPS_RX	       (21u)

// Onboard temp. sensor
#define ONEWIRE        (23u)

// Power switch for modules
#define POWER_EN       (26u)
#define POWER_FAULT    (27u)

// GSM module extras
// pull KEY low
#define GSM_KEY        (18u)
#define GSM_CARRIER    (19u)

// 1 Hz signal from RTC
#define HZ_RTC	       (22u)

#define SERIAL_HOWMANY (3u)
#define SPI_HOWMANY    (2u)
#define WIRE_HOWMANY   (2u)

#include "../generic/common.h"
