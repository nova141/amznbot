import asyncio
import random
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from config import PRODUCTS, CHECK_INTERVAL, HEADLESS, DISCORD_WEBHOOK_URL
from logger import structured_log
from checkout import simulate_checkout
from stealth import apply_stealth
from selectors import safe_text
from notifier import notify_discord
from proxy_config import get_random_proxy

ua = UserAgent()

async def human_like_scroll(page):
    height = await page.evaluate("() => document.body.scrollHeight")
    for pos in range(0, height, random.randint(100, 300)):
        await page.mouse.wheel(0, pos)
        await asyncio.sleep(random.uniform(0.2, 0.5))

async def fetch_product_loop(browser, product):
    proxy = get_random_proxy()
    context = await browser.new_context(
        user_agent=ua.random,
        proxy={"server": proxy},
        locale="en-US",
        viewport={"width": 1280, "height": 800}
    )
    await apply_stealth(context)
    page = await context.new_page()

    while True:
        try:
            await page.goto(product["url"], timeout=30000)
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(random.uniform(1.5, 3.0))
            await human_like_scroll(page)

            title = await safe_text(page, "#productTitle")
            seller = await safe_text(page, "#merchant-info")
            price = await safe_text(page, "span.a-offscreen")

            price_val = float(price.replace("$", "").replace(",", "")) if price != "N/A" else 99999

            if product["expected_seller"] in seller and price_val <= product["max_price"]:
                structured_log("Product Available", {"title": title, "price": price_val, "seller": seller})
                notify_discord(f"{title} AVAILABLE at ${price_val} from {seller}", DISCORD_WEBHOOK_URL)
                await simulate_checkout(page)
            else:
                structured_log("Product Unavailable", {"title": title, "price": price_val, "seller": seller})
        except Exception as e:
            structured_log("Error Fetching Product", {"error": str(e), "url": product["url"]}, level="ERROR")

        await asyncio.sleep(random.uniform(*CHECK_INTERVAL))

async def monitor():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        tasks = [fetch_product_loop(browser, prod) for prod in PRODUCTS]
        await asyncio.gather\(*tasks)

