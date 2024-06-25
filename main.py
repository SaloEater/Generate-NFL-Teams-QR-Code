import qrcode
from PIL import Image, ImageDraw
import os
import re
import math


def sanitize_filename(string):
    # Replace any character that is not alphanumeric or an underscore with an underscore
    return re.sub(r'[^a-zA-Z0-9]', '_', string)


def generate_qr_code(string, qr_size):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,  # No border
    )
    qr.add_data(string)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Resize the QR code to the specified size
    img_resized = img.resize((qr_size, qr_size), Image.NEAREST)

    return img_resized


def generate_qr_code_page(string, output_dir, page_width, page_height, qr_size, gap_size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Calculate number of QR codes per row and column
    num_qr_per_row = (page_width + gap_size) // (qr_size + gap_size)
    num_qr_per_col = (page_height + gap_size) // (qr_size + gap_size)
    num_qr_per_page = num_qr_per_row * num_qr_per_col

    # Create a new page image
    page_img = Image.new('RGB', (page_width, page_height), 'white')

    # Generate QR code image for the string
    qr_img = generate_qr_code(string, qr_size)

    # Paste the QR code images onto the page with gaps
    draw = ImageDraw.Draw(page_img)
    for row in range(num_qr_per_col):
        for col in range(num_qr_per_row):
            x = col * (qr_size + gap_size)
            y = row * (qr_size + gap_size)
            page_img.paste(qr_img, (x, y))

    # Save the page image with the string value as filename
    sanitized_string = sanitize_filename(string)
    img_filename = f"{output_dir}/page_{sanitized_string}.png"
    page_img.save(img_filename)
    print(f"Page for '{string}' saved as {img_filename}")


def main():
    # Example set of strings
    strings = ["Arizona Cardinals",
    "Atlanta Falcons",
    "Baltimore Ravens",
    "Buffalo Bills",
    "Carolina Panthers",
    "Chicago Bears",
    "Cincinnati Bengals",
    "Cleveland Browns",
    "Dallas Cowboys",
    "Denver Broncos",
    "Detroit Lions",
    "Green Bay Packers",
    "Houston Texans",
    "Indianapolis Colts",
    "Jacksonville Jaguars",
    "Kansas City Chiefs",
    "Las Vegas Raiders",
    "Los Angeles Chargers",
    "Los Angeles Rams",
    "Miami Dolphins",
    "Minnesota Vikings",
    "New England Patriots",
    "New Orleans Saints",
    "New York Giants",
    "New York Jets",
    "Philadelphia Eagles",
    "Pittsburgh Steelers",
    "San Francisco 49ers",
    "Seattle Seahawks",
    "Tampa Bay Buccaneers",
    "Tennessee Titans",
    "Washington Commanders"
    ]

    # Output directory to save QR code pages
    output_dir = "qr_code_pages"

    # Page size (4x6 inches) in pixels (assuming 300 dpi)
    dpi = 300
    page_width = 4 * dpi
    page_height = 6 * dpi

    # QR code size in pixels
    qr_size = 200  # Each QR code is 21 modules * 10 pixels/module
    gap_size = 5  # Gap between QR codes

    # Generate QR code page for each string
    for string in strings:
        generate_qr_code_page(string, output_dir, page_width, page_height, qr_size, gap_size)
        return


if __name__ == "__main__":
    main()
