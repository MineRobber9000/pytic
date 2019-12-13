This is the file format specification for the `*.tic` format used by TIC-80.

# Overview

TIC-80 cartridge files consist of several chunks of data. These contain the various assets of a game, such as the code, sprites, map, audio, and cover image.

# Chunk Format

Each chunk consists of a 4-byte header, followed by the chunk data. After the chunk data, other chunks will follow afterwards.

| Offset | Bits (7...0) | Description                                      |
| ------ | ------------ | ------------------------------------------------ |
| 0      | `BBBCCCCC`   | B = Bank number (0...7), C = Chunk type (0...31) |
| 1...2  | `SSSSSSSS`   | Size of chunk (16 bits, max. 65535 bytes)        |
| 3      |              | Reserved for future use                          |
| 4+     | `DDDDDDDD`   | Chunk data                                       |

The 16-bit size value is stored in [little-endian](https://en.wikipedia.org/wiki/Endianness#Little-endian) order. That is to say, offset 1 stores the eight **least-significant** bits, while offset 2 stores the eight **most-significant** bits.

There is a bug; when saving a full 65536 characters (the **actual** maximum number for TIC-80 code), the 16-bit size number will wrap around. The code loaded into the editor becomes empty, and it interferes with other chunks.

# Chunk Types

Certain chunk types are zero-extended (e.g. to fill remaining sprite pixel pairs with black, or to fill remaining map cells with 0), but others ignore the `B` bank bits as described previously.

The following numbers are based on the `ChunkType` enum in [tic.c](https://github.com/nesbox/TIC-80/blob/master/src/tic.c):

## 1 (`0x01`) - Tiles
This represents sprites 0...255. This is copied to `0x4000`...`0x5FFF`.

## 2 (`0x02`) - Sprites
This represents sprites 256...511. This is copied to `0x6000`...`0x7FFF`.

## 3 (`0x03`) - Cover
This is the GIF image file that is displayed to the user in SURF mode and appears on the website. The bank bits are ignored.

## 4 (`0x04`) - Map
This represents the map data. This is copied to `0x8000`...`0xFF7F`.

## 5 (`0x05`) - Code
This represents the game code, in [ASCII](https://en.wikipedia.org/wiki/ASCII) text format. Banks other than 0 are discarded in 0.80.0.

## 6 (`0x06`) - Flags (0.80.0)
This represents the sprite flags data, copied to `0x14000`...`0x141FF`. This is not used on versions prior to this.

## 9 (`0x09`) - SFX
This represents the sound effect data. This is copied to `0x100E4`...`0x11163`.

## 10 (`0x0A`) - Waveforms
This represents the sound wavetable data. This is copied to `0x0FFE4`...`0x100E3`.

## 12 (`0x0C`) - Palette
This represents the palette data. This is copied to `0x3FC0`...`0x3FEF` on cart boot. Prior to 0.70.6, the bank bits were ignored and the palette was used across all graphics/map banks. In 0.70.6 and above, each bank gets its own palette.

## 13 (`0x0D`) - Music Patterns
This represents the music pattern data. This is copied to `0x11164`...`0x13E63`.

## 14 (`0x0E`) - Music Tracks
This represents the music track data. This is copied to `0x13E64`...`0x13FFB`.

Any chunk type not described above doesn't have any useful purpose, as of the time of writing.
