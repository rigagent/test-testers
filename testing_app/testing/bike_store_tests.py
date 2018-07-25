import json
import unittest
import urllib2
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

SELENIUM_WD_URL = "http://192.168.16.2:4444/wd/hub"
TEST_URL = "http://192.168.16.4:8000"
JSON_URL = "https://raw.githubusercontent.com/rigagent/test-testers/master/app/bikes.json"
# JSON_URL = "https://jujhar.com/bikes.json"


class BikeStoreTests(unittest.TestCase):
  '''
  This test suite verifies the page of Bike Store site.
  '''

  @classmethod
  def setUpClass(cls):
    options = ChromeOptions()
    desired_capabilities = options.to_capabilities()
    # desired_capabilities["platform"] = "Linux"
    cls.driver = webdriver.Remote(command_executor=SELENIUM_WD_URL,
                                  desired_capabilities=desired_capabilities)

  @classmethod
  def tearDownClass(cls):
    cls.driver.close()

  def setUp(self):
    self.driver.get(TEST_URL)
    try:
      response = urllib2.urlopen(JSON_URL)
      self.bikes_dict = json.loads(response.read())
    except urllib2.HTTPError, e:
      print e.fp.read()

  @property
  def _grid_content(self):
    """
    This is a property allows us to get the Selenium WebDriver object
    of all content of the grid on the page.
    :return: list of objects
    """
    return self.driver.find_elements_by_class_name("panel-primary")

  @property
  def _checkboxes(self):
    """
    This is a property allows us to get the Selenium WebDriver object
    of all checkboxes on the page.
    :return: list of objects
    """
    return self.driver.find_elements_by_xpath("//input[@type='checkbox']")

  @property
  def _checkbox_tags(self):
    """
    This is a property allows us to get the Selenium WebDriver object
    of all tags of checkboxes on the page.
    :return: list of objects
    """
    return self.driver.find_elements_by_xpath("//input[@type='checkbox']/following-sibling::span")

  def _find_count_bikes_classes(self, bike_class):
    """
    This is a method to find the count of bike classes by appropriate class.
    :param bike_class: this current class of bike
    :return: count of bike classes
    """
    count = 0
    for n in range(len(self.bikes_dict["items"])):
      if bike_class in self.bikes_dict["items"][n]["class"]:
        count += 1
    return count

  def _get_dict_of_sorted_bikes_by_class(self):
    """
    This is a method to get the dictionary of sorted bikes by appropriate class.
    :return: dictionary of bikes
    """
    dict_of_bikes = {}
    for n in range(len(self._checkboxes)):
      # Here we find the lable located near the checkbox
      bike_class_name = self._checkbox_tags[n].text.lower()
      self._checkboxes[n].click()

      # Here we form the data structure like {'bike_class': ['bike_name1', 'bike_name2', ... ], ... }
      bike_names = [m.find_element_by_class_name("panel-heading").text for m in self._grid_content]
      dict_of_bikes[bike_class_name] = bike_names

      # Uncheck flag backward
      self._checkboxes[n].click()
    return dict_of_bikes

  def test_page_title(self):
    """
    This test case verifies that page of site has right title.
    1.- Open the page of Bike Store site
    2.- Check title of the page
    """
    self.assertEqual("Bike Store", self.driver.title,
                     "The title of page has another name than was expected...")

  def test_names_of_bikes_in_grid_content(self):
    """
    This test case verifies that names of bikes in content of the grid on the page
    have right values as it was expected.
    1.- Open the page of Bike Store site
    2.- Compare each name of bike on the page with name of bike from given JSON data
    """
    for n in range(len(self.bikes_dict["items"])):
      bike_name = self._grid_content[n].find_element_by_class_name("panel-heading")
      self.assertEqual(bike_name.text, self.bikes_dict["items"][n]["name"],
                       "The content of the grid on the page has another bike name than it was expected...")

  def test_image_links_of_bikes_in_grid_content(self):
    """
    This test case verifies that image links of bikes in content of the grid on the page
    have right values as it was expected.
    1.- Open the page of Bike Store site
    2.- Compare each image link of bike on the page with image link of bike from given JSON data
    """
    for n in range(len(self.bikes_dict["items"])):
      bike_image_link = self._grid_content[n].find_element_by_tag_name("img").get_attribute('src')
      self.assertEqual(bike_image_link, self.bikes_dict["items"][n]["image"]["thumb"],
                       "The content of the grid on the page has another bike link than it was expected...")

  def test_descriptions_of_bikes_in_grid_content(self):
    """
    This test case verifies that descriptions of bikes in content of the grid on the page
    have right values as it was expected.
    1.- Open the page of Bike Store site
    2.- Compare each description of bike on the page with description of bike from given JSON data
    """
    for n in range(len(self.bikes_dict["items"])):
      bike_description = self._grid_content[n].find_element_by_class_name("desc")
      self.assertEqual(bike_description.text, self.bikes_dict["items"][n]["description"],
                       "The content of the grid on the page has another bike description than it was expected...")

  def test_classes_of_bikes_in_grid_content(self):
    """
    This test case verifies that classes of bikes in content of the grid on the page
    have right values as it was expected.
    1.- Open the page of Bike Store site
    2.- Compare the number of bike classes on the page with number of bike classes from given JSON data
    3.- Compare each class of bike on the page with classes of bike from given JSON data
    """
    for n in range(len(self.bikes_dict["items"])):
      bike_classes = self._grid_content[n].find_element_by_class_name("panel-footer").find_elements_by_class_name("capitalise")
      self.assertEqual(len(bike_classes), len(self.bikes_dict["items"][n]["class"]),
                       "The number of classes for appropriate bike on the page is not equal to expected values...")
      for m in range(len(bike_classes)):
        self.assertTrue(str(self.bikes_dict["items"][n]["class"][m]).capitalize() in str(bike_classes[m].text),
                        "The bike is in another class than it was expected...")

  def test_checkboxes_on_the_page(self):
    """
    This test case verifies the work of all 3 checkboxes on the page.
    1.- Open the page of Bike Store site
    2.- Find and click on the first checkbox
    3.- Compare the number of all classes of bikes on the page with classes of bike from given JSON data after checkbox is selected
    4.- Uncheck this checkbox
    5.- Compare the the same as was in step #3 but for page with full amount of content
    6.- Repeat steps #2-5 for all remaining checkboxes
    """
    for n in range(len(self._checkboxes)):
      # Here we find the lable located near the checkbox
      bike_class_name = self._checkbox_tags[n].text.lower()
      self.assertFalse(self._checkboxes[n].is_selected(), "The checkbox is selected...")
      self._checkboxes[n].click()
      self.assertTrue(self._checkboxes[n].is_selected(), "The checkbox isn't selected...")

      # It's enough just to compare the number of grids on the page (actual result)
      # with the number of class references in JSON object (expected result)
      self.assertEqual(len(self._grid_content), self._find_count_bikes_classes(bike_class_name),
                       "The number of contents on the page after appropriate checkbox selecting is not equal to expected values...")

      # Uncheck flag backward
      self._checkboxes[n].click()
      self.assertFalse(self._checkboxes[n].is_selected(), "The checkbox is selected...")

      # Here we compare the number of grids on the page (actual result)
      # with number of all items in JSON object (expected result)
      self.assertEqual(len(self._grid_content), len(self.bikes_dict["items"]),
                       "The number of contents on the page after appropriate checkbox reseting is not equal to expected values...")

  def test_refresh_the_page(self):
    """
    This test case verifies the work of all 3 checkboxes on the page.
    1.- Open the page of Bike Store site
    2.- Get information (e.g. names of bikes for appropriate class) about content in the grid on the page
    3.- Refresh the page
    4.- Repeat step #2
    5.- Compare information (e.g. in dictionaries) in regards to before and after page refreshing
    """
    bikes_before_page_refreshing = self._get_dict_of_sorted_bikes_by_class()
    self.driver.refresh()
    bikes_after_page_refreshing = self._get_dict_of_sorted_bikes_by_class()
    self.assertEqual(bikes_before_page_refreshing, bikes_after_page_refreshing,
                     "The content of the page after page refreshing is not equal to content before refreshing...")


if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(BikeStoreTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
