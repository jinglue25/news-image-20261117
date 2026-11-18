"""Render the fixed news infographic deterministically with local DejaVu fonts."""

from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
MARGIN = 40
TEXT_WIDTH = SIZE - 2 * MARGIN
NAVY = "#11273E"
INK = "#15283A"
GRAY = "#303A43"
RULE = "#C9D2DA"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
OUTPUT = Path(__file__).with_name("entry.png")
DATE_TITLE = "TUESDAY 17 NOVEMBER 2026"
FOOTER = "Events of 17 November 2026, as reported."

STORIES = (
    (
        "UKRAINE",
        "Bridge war",
        "Ukraine hit Crimea's Kerch Bridge for a second straight day. President Zelenskyy hailed "
        'an "unprecedented operation." Russia hit Kyiv bridges and river crossings overnight.',
        "#285D8A",
    ),
    (
        "MIDDLE EAST",
        "Iran hits US radar in Bahrain",
        "Iran's Revolutionary Guard drones hit a US military radar system at Bahrain's Sheikh Isa base. "
        "Bahrain says it intercepted the drones, with no casualties or damage.",
        "#8F4836",
    ),
    (
        "DIPLOMACY",
        "Xi, Trump and Putin to meet Thursday",
        "China confirmed the presidents' first three-way meeting in Shenzhen on Thursday, "
        "19 November, on the sidelines of the APEC leaders' meeting.",
        "#5D4A7D",
    ),
    (
        "EUROPE",
        "Five states plan Rwanda return hub",
        "Germany, Denmark, Austria, Greece and the Netherlands announced a joint facility "
        "in Rwanda for rejected asylum seekers.",
        "#286658",
    ),
    (
        "ASIA-PACIFIC",
        "Japan scrambles jets",
        "Japan launched fighter jets and protested after two suspected Russian aircraft "
        "entered its airspace.",
        "#834256",
    ),
)


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(str(FONT_DIR / name), size)


def summary_lines(text, face):
    """Select a balanced break without changing the supplied text."""
    if face.getlength(text) <= TEXT_WIDTH:
        return (text,)
    words = text.split(" ")
    breaks = (
        (" ".join(words[:index]), " ".join(words[index:]))
        for index in range(1, len(words))
    )
    return min(breaks, key=lambda lines: max(face.getlength(line) for line in lines))


def draw_summary(image, top, text, face):
    lines = summary_lines(text, face)
    assert 1 <= len(lines) <= 2
    assert " ".join(lines) == text
    width = max(int(face.getlength(line)) + 3 for line in lines)
    strip = Image.new("RGB", (width, 68), "white")
    pen = ImageDraw.Draw(strip)
    for index, line in enumerate(lines):
        pen.text((0, index * 34), line, font=face, fill=GRAY, anchor="lt")
    if width > TEXT_WIDTH:
        strip = strip.resize((TEXT_WIDTH, strip.height), Image.Resampling.LANCZOS)
    image.paste(strip, (MARGIN, top))


def draw_entry():
    image = Image.new("RGB", (SIZE, SIZE), "white")
    pen = ImageDraw.Draw(image)
    label, date = font(24, True), font(56, True)
    number, category = font(39, True), font(21, True)
    headline, body, footer = font(40, True), font(29), font(22)

    pen.rectangle((0, 0, SIZE - 1, 140), fill=NAVY)
    pen.text((MARGIN, 23), "WORLD NEWS", font=label, fill="#CEE3F4", anchor="lt")
    assert date.getlength(DATE_TITLE) <= TEXT_WIDTH
    pen.text((MARGIN, 65), DATE_TITLE, font=date, fill="white", anchor="lt")

    for index, (section, title, summary, color) in enumerate(STORIES):
        top = 150 + index * 164
        pen.rectangle((MARGIN, top + 10, MARGIN + 63, top + 73), fill=color)
        pen.text((MARGIN + 32, top + 42), str(index + 1), font=number, fill="white", anchor="mm")
        title_left = 116
        available = SIZE - MARGIN - title_left
        assert category.getlength(section) <= available
        assert headline.getlength(title) <= available
        pen.text((title_left, top + 9), section, font=category, fill=color, anchor="lt")
        pen.text((title_left, top + 34), title, font=headline, fill=INK, anchor="lt")
        draw_summary(image, top + 87, summary, body)
        pen.line((MARGIN, top + 161, SIZE - MARGIN - 1, top + 161), fill=RULE, width=1)

    pen.text((MARGIN, 988), FOOTER, font=footer, fill=GRAY, anchor="lt")
    image.save(OUTPUT, format="PNG", optimize=True)

    with Image.open(OUTPUT) as saved:
        saved.load()
        assert saved.format == "PNG", f"Expected PNG, got {saved.format}"
        assert saved.size == (1024, 1024), f"Unexpected dimensions: {saved.size}"
        assert saved.mode == "RGB", f"Unexpected mode: {saved.mode}"
    data = OUTPUT.read_bytes()
    assert len(data) <= 1024 * 1024, f"entry.png exceeds 1 MiB: {len(data)} bytes"
    print(f"entry.png: {len(data)} bytes, SHA-256 {sha256(data).hexdigest()}")


if __name__ == "__main__":
    draw_entry()
