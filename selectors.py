async def safe_text(page, selector, fallback="N/A"):
    try:
        el = page.locator(selector)
        if await el.count() > 0 and await el.is_visible():
            return (await el.text_content()).strip()
    except:
        return fallback
    return fallback
