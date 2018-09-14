from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
import time

def get_download_link(url, extensions=[], verbose=False, screenshot='', window_size=(1000,1000)):

	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox') # WARNING: allows to run as root
	options.add_argument('--system-developer-mode') # allow load unpacked extension

	if extensions != None and len(extensions) > 0:
		arg = '--load-extension={}'.format(','.join(extensions))
		options.add_argument(arg)

	if verbose:
		print('ChromeOptions: {}'.format(' '.join(options.arguments)))

	driver = webdriver.Chrome(chrome_options=options)
	driver.set_window_size(*window_size)

	if verbose:
		print('Getting {}'.format(url))
	driver.get(url)

	if screenshot != None:
		if verbose:
			print('Saving screenshot')
		driver.save_screenshot(screenshot)

	if verbose:
		print('Checking if it is happy hour')
	try:
		link = _get_link(driver)
	except NoSuchElementException:
		print('It is not happy hour, we will have to wait')
	else:
		if verbose:
			print('Happy Hour !')
		return link

	# Wait for the 30s timer + 2s delay then click on go to download
	delta = 32
	if verbose:
		print('Starting to wait for {} seconds'.format(delta))
		for i in range(delta):
			print("\r\033[1;31m{} \033[0;33mseconds left".format(delta - i), end='')
			time.sleep(1)
		print("\r\033[0m", end='')
	else:
		time.sleep(30 + random.randint(1,5))

	if verbose:
		print('Navigating to second page')
	xpath = '//*[@id="dl"]/form/table/thead/tr/td[2]/input[2]'
	driver.find_element_by_xpath(xpath).send_keys(Keys.SPACE)

	return _get_link(driver)

# Function to retrieve the download link
def _get_link(driver) -> str:
	xpath = '//*[@id="dl"]/form/table/thead/tr/td[2]/a'
	link = driver.find_element_by_xpath(xpath).get_attribute('href')
	if link[:7] == 'http://':
		link = 'https://' + link[7:]
	return link

if __name__ == '__main__':
	URL = 'https://uptobox.com/'
	import argparse
	parser = argparse.ArgumentParser(
		description='''A script for retrieving download links from uptobox
		NOTE: an adblocker extension is required''')
	parser.add_argument('-q', '--quiet', action='store_true')
	parser.add_argument('-e', '--extensions', action='append',
		help='List of dirpath to extension')
	parser.add_argument('-s', '--screenshot',
		help='Path to a file where to save a screenshot')
	parser.add_argument('PATH',
		help='String to be appended to {}'.format(URL))
	args = parser.parse_args()
	url = URL + args.PATH
	dl_url = get_download_link(url,
		extensions=args.extensions, verbose=not args.quiet,
		screenshot=args.screenshot)
	print(dl_url)
