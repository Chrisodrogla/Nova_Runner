const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage'],
        defaultViewport: {
            width: 1920,
            height: 1080
        }
    });

    const page = await browser.newPage();
    await page.goto('https://www.airbnb.com/performance/conversion/conversion_rate');

    // Log in
    await page.click('button[aria-label="Continue with email"]');
    await page.waitForSelector('input[inputmode="email"]');
    await page.type('input[inputmode="email"]', process.env.AIRBNB_USER_SECRET);
    await page.click('button[data-testid="signup-login-submit-btn"]');

    await page.waitForTimeout(2000); // Wait for login process

    const currentHtml = await page.content();
    console.log(currentHtml);

    await browser.close();
})();
