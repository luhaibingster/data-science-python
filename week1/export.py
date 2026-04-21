import os
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

HTML_FILE = "preview.html"
OUTPUT_DIR = "rendered_pages"
PDF_FILE = "brochure_exact.pdf"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    html_path = Path(HTML_FILE).resolve()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1400, "height": 1980},
            device_scale_factor=2
        )

        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(2000)

        pages = page.locator(".page")
        count = pages.count()

        if count == 0:
            browser.close()
            raise RuntimeError("No elements with class '.page' were found.")

        image_files = []

        for i in range(count):
            path = os.path.join(OUTPUT_DIR, f"page_{i+1:02d}.png")
            pages.nth(i).screenshot(path=path)
            image_files.append(path)

        browser.close()

    images = [Image.open(img).convert("RGB") for img in image_files]
    images[0].save(
        PDF_FILE,
        save_all=True,
        append_images=images[1:],
        resolution=300.0
    )

    print(f"Saved to {PDF_FILE}")

if __name__ == "__main__":
    main()