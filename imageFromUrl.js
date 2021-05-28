/**
 * @name screenshots
 *
 * @desc Snaps a basic screenshot of the Google Maps Traffic given a URL and saves it a .png file.
 *
 * @see {@link https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md#screenshot}
 */

const puppeteer = require('puppeteer')
const fs = require('fs')
const path = require('path');

(async () => {
	const args = process.argv.slice(2)
	args[0] = unescape(args[0])
	const queryObj = JSON.parse(args[0])
	const url = queryObj.url
	const image_path = decodeURIComponent(queryObj.image_path) //args[1]
	const browser = await puppeteer.launch({ headless: true, args: ['--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox'] })
	const page = await browser.newPage()

	page.on('error', err => {
		console.log('error happen at the page: ', err)
	})

	page.on('pageerror', pageerr => {
		console.log('pageerror occurred: ', pageerr)
	})

	const consoleMessages = []
	page.on('console', msg => { // log out any of the page's console messages
		for (let i = 0; i < msg.args().length; ++i)
			consoleMessages.push(`${i}: ${msg.args()[i]}`)
	})

	await page.setViewport({ width: queryObj.width, height: queryObj.height })

	await page.goto(
		url,
		{ "waitUntil": "networkidle0" } // consider navigation to be finished when there are no more than 0 network connections for at least 500 ms
	).catch((e) => console.log("error1", e)) //works with delay
	consoleMessages.push('hiding controls')
	await page.addStyleTag({
		content: `
			div#omnibox-container { /* hide search box */
				display:none;
			}
			div#minimap { /* hide sattelite button */
				display:none;
			}
			div#runway-expand-button { /* hide street view buttons */
				display:none;
			}
			div.app-vertical-widget-holder.noprint { /* hide zoom and 3d buttons */
				display:none;
			}
			div#vasquette { /* hide sign in button and apps buttons */
				display:none;
			}
			#layer > div > div > div > span > span.widget-layer-toggle { /* hide the toggle traffic button */
				display:none;
			}
			#layer > div > div > div > span > span.widget-layer-traffic-mode-selector > div > div > div > div.goog-inline-block.goog-menu-button-dropdown { /* hide the dropdown */
				display:none;
			}
			#layer > div > div > div.widget-layer.widget-layer-shown { /* make the legend shrink since we hid pieces */
				min-width:unset;
			}
	`})

	consoleMessages.push("image_path")
	consoleMessages.push(image_path)
	// await page.waitForFunction(() => pageLoaded === true) //wait for page to say it's loaded
	fs.unlink(image_path, async (err) => {
		// await page.emulateMedia('screen')
		// create direcotry if it doesn't exist
		const dir = path.dirname(image_path)
		if (!fs.existsSync(dir)) {
			fs.mkdirSync(dir)
		}
		queryObj.consoleMessages = consoleMessages;
		console.log(/*"queryObj",*/ JSON.stringify(queryObj, null, 2));
		await page.screenshot({ path: image_path, type: queryObj.type });
		await browser.close();
	})
}
)()