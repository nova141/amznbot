from logger import structured_log
import asyncio

async def simulate_checkout(page):
    try:
        await page.get_by_role("button", name="Pre-order now").click()
        structured_log("Clicked Pre-order now")

        await page.goto("https://www.amazon.com/gp/cart/view.html")
        await page.wait_for_timeout(1500)

        await page.click("input[name='proceedToRetailCheckout']", timeout=5000)
        structured_log("Proceeded to checkout")

        await page.fill('input[name="email"]', "test@example.com")
        await page.click('input#continue')
        await page.wait_for_timeout(1000)
        await page.fill('input[name="password"]', "password123")
        await page.click('input#signInSubmit')
        structured_log("Logged in")

        await page.wait_for_selector("input[name='placeYourOrder1']", timeout=10000)
        await page.click("input[name='placeYourOrder1']")
        structured_log("Order placed (simulated)")

    except Exception as e:
        structured_log("Checkout Failed", {"error": str(e)}, level="ERROR")
