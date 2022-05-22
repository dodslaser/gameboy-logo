from argparse import ArgumentParser
from pathlib import Path
from PIL import Image


def pretty_hex(b: bytes, width: int = 16) -> str:
    pretty = (b[i:i + width].hex(" ") for i in range(0, len(b), width))
    return "\n".join(pretty)


def read_rom(rom: Path, bmp: Path) -> None:
    try:
        with open(rom, "rb") as f:
            f.seek(0x104)
            header = f.read(48)
    except Exception as e:
        print("Could not read header from ROM:", e)
        exit(1)
    else:
        print(f"Read encoded logo from {rom.name}:")
        print(pretty_hex(header, width=6), end="\n\n")

    logo = bytes(
        # Combine nibbles of every other byte
        header[a + b + d] << c & 0xF0 | header[a + b + d + 2] >> 4 - c & 0x0F
        for a in (0, 24)  # Upper/lower 24 bytes
        for b in (0, 1)  # Even/odd bytes
        for c in (0, 4)  # Upper/lower nibbles
        for d in range(0, 21, 4)  # 6 bytes (48 bits) per row
    )

    print("Decoded logo:")
    print(pretty_hex(logo, width=6), end="\n\n")

    try:
        Image.frombytes("1", (48, 8), logo).save(bmp)
    except Exception as e:
        print("Could not write decoded logo:", e)
        exit(1)
    else:
        print(f"Wrote decoded logo to {bmp}")


def write_rom(rom: Path, bmp: Path) -> None:
    try:
        logo = Image.open("mylogo.bmp").tobytes()
    except Exception as e:
        print("Could not read decoded logo:", e)
        exit(1)

    print(f"Read decoded logo from {bmp.name}:")
    print(pretty_hex(logo, width=6), end="\n\n")

    header = bytes(
        # Combine nibbles of every 6th byte (i.e. 1 row down)
        logo[a + b + d] << c & 0xF0 | logo[a + b + d + 6] >> 4 - c & 0x0F
        for a in (0, 24)  # Upper/lower 24 bytes
        for b in range(0, 6)  # 6 bytes (48 bits) per row
        for c in (0, 4)  # Upper/lower nibbles
        for d in (0, 12)  # Header bytes are 12 logo bytes apart
    )

    print("Encoded logo:")
    print(pretty_hex(header, width=6), end="\n\n")

    try:
        with open("mylogo.gb", "wb") as f:
            # Generate a valid gameboy rom by padding with 0x00 to fill out the header
            f.write(bytes(260) + header + bytes(28))
    except Exception as e:
        print("Could not write encoded logo:", e)
        exit(1)
    else:
        print(f"Writing encoded logo to {rom}")


if __name__ == "__main__":
    parser = ArgumentParser()

    subparser = parser.add_subparsers()
    subparser.required = True

    parser_read_rom = subparser.add_parser("read-rom")
    parser_read_rom.add_argument("rom", type=Path)
    parser_read_rom.add_argument("bmp", type=Path)
    parser_read_rom.set_defaults(func=read_rom)

    parser_write_rom = subparser.add_parser("write-rom")
    parser_write_rom.add_argument("bmp", type=Path)
    parser_write_rom.add_argument("rom", type=Path)
    parser_write_rom.set_defaults(func=write_rom)

    args = parser.parse_args()
    args.func(args.rom, args.bmp)
