from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
import cv2
import pyocr
from PIL import Image
import time


def main():
	sushida_url = 'http://typingx0.net/sushida/play.html'
	DRIVER_PATH = 'somewhere' # TODO
	img_name = 'screenshot.png'

	chrome_service = fs.Service(executable_path=DRIVER_PATH)
	options = Options()
	driver = webdriver.Chrome(service=chrome_service, options=options)
	window = (900, 900+123)
	driver.set_window_size(*window)
	driver.get(sushida_url)

	target_xpath = '//*[@id="game"]/div'
	webgl_element = driver.find_element_by_xpath(target_xpath)
	actions = ActionChains(driver)
	actions.move_to_element(webgl_element).perform()

	time.sleep(5)

	center_x, center_y = (250, 250)
	actions = ActionChains(driver)
	actions.move_to_element_with_offset(webgl_element, center_x, center_y).click().perform()

	time.sleep(2)

	center_x, center_y = (250, 300)
	actions.move_to_element_with_offset(webgl_element, center_x, center_y).click().perform()

	time.sleep(1)

	target_xpath = '/html/body'
	element = driver.find_element_by_xpath(target_xpath)
	element.send_keys(" ")

	time.sleep(3)

	# main loop for typing
	while True:
		driver.save_screenshot(img_name)
		img = cv2.imread(img_name)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = img[350:390, 250:-290]
		_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)



		cv2.imwrite('processed_' + img_name, img)

		tools = pyocr.get_available_tools()
		tool = tools[0]
		res = tool.image_to_string(
			Image.open('processed_'+img_name), 
			lang='eng'
		)

		if len(res) == 0:
			break

		element.send_keys(res)
		time.sleep(1)

	time.sleep(10)

	driver.quit()
	driver.close()

if __name__ == '__main__':
	main()