This is the file format specification for the `*.tic` format used by TIC-80.

# Overview

TIC-80 cartridge files consist of several chunks of data, which contain the various assets of a game (i.e. the code, sprites, map, audio and cover image).

# Chunk Format

Each chunk consists of a 4-byte header, followed by the chunk data. This pattern is then repeated for each chunk.

| Offset | Bits (7...0) | Description |
| --- | --- | --- |
| 0 | `BBBCCCCC` | B = Bank number (0...7), C = Chunk type (0...31) |
| 1...2 | `SSSSSSSS` | Size of chunk (16 bits, max. 65535 bytes) |
| 3 | | Reserved for future use |
| 4+ | `DDDDDDDD` | Chunk data |

The 16-bit size value is stored in [little-endian](https://en.wikipedia.org/wiki/Endianness#Little-endian) order. That is to say, offset 1 stores the eight **least-significant** bits, while offset 2 stores the eight **most-significant** bits.

~~There is a bug; when saving a full 65536 characters (the **actual** maximum size for TIC-80 code), the 16-bit size number will wrap around. This causes the code editor to become empty, and interprets the code's text as if it were the following chunks.~~

# Chunk Types

Certain chunk types are of fixed size, for example the sprite sheets and map, and these are zero-extended such that sprite pixels and map cells have a zero value. Other chunks ignore the `B` bank bits as described previously.

The following numbers are based on the `ChunkType` enum in [cart.c](https://github.com/nesbox/TIC-80/blob/21b84d1f714966422228cbbb492e26dce250d26e/src/cart.c#L28):

## 1 (`0x01`) - Tiles
This represents the BG sprites (0...255). This is copied to `0x4000`...`0x5FFF`.

## 2 (`0x02`) - Sprites
This represents the FG sprites (256...511). This is copied to `0x6000`...`0x7FFF`.

## 3 (`0x03`) - Cover
This is the GIF image file that is displayed to the user in SURF mode and appears on the website. The bank bits are ignored.

## 4 (`0x04`) - Map
This represents the map data. This is copied to `0x8000`...`0xFF7F`.

## 5 (`0x05`) - Code (Uncompressed)
This represents the code, in [ASCII](https://en.wikipedia.org/wiki/ASCII) text format.

Note: 0.80 removed support for code banks. As a workaround, it loads each individual bank with a newline separated between them, starting at bank 7 (which appears at the top) and working backwards to bank 0. The bank number is otherwise considered deprecated with this chunk type.

## 6 (`0x06`) - Flags (0.80)
This represents the sprite flags data. This is copied to `0x14404`...`0x14603`.

## 9 (`0x09`) - SFX
This represents the sound effect data. This is copied to `0x100E4`...`0x11163`.

## 10 (`0x0A`) - Waveforms
This represents the sound wave-table data. This is copied to `0x0FFE4`...`0x100E3`.

## 12 (`0x0C`) - Palette
This represents the palette data. Prior to 0.70.6, the bank bits were ignored and the palette was used across all graphics/map banks. In 0.70.6 and above, each bank gets its own palette.

This chunk type is 96 bytes long: 48 bytes for the `SCN` palette, followed by 48 bytes for the `OVR` palette. The `SCN` palette is copied to `0x3FC0`...`0x3FEF`.

Note: If no palette chunk is specified for bank 0, then the bank will have the DB16 palette for `SCN`, and the `OVR` palette will be left blank. This preserves compatibility with ancient carts without a palette chunk defined.

## 13 (`0x0D`) - Music Patterns (pre-0.80)
This represents the music pattern data. This is copied to `0x11164`...`0x13E63`. This is the old variation which is deprecated. In 0.80, it is automatically converted to a new format used by type 15 (`0x0F`).

## 14 (`0x0E`) - Music Tracks
This represents the music track data. This is copied to `0x13E64`...`0x13FFB`.

## 15 (`0x0F`) - Music Patterns (0.80)
This represents the music pattern data. This is copied to `0x11164`...`0x13E63`. This is a new variation with support for effect commands.

## 16 (`0x10`) - ZLIB Compressed Code (0.80)
This represents the code, but compressed. If the code editor goes beyond the 64K chunk limit, TIC-80 will compress the code down as long as the compressed result never goes above 64K. The bank bits seem to be ignored.

Any chunk type not described above is reserved for future use and should likely be avoided.