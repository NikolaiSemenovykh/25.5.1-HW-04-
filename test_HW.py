import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import email, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome()
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   yield
   pytest.driver.quit()

def test_show_all_pets():
   pytest.driver.implicitly_wait(10)

   pytest.driver.find_element(By.ID, 'email').send_keys(email)
   pytest.driver.find_element(By.ID,'pass').send_keys(password)
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   images = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0

# Задание 25.3.1:
# Написать тест, который проверяет, что на странице со списком питомцев пользователя
# https://petfriends.skillfactory.ru/my_pets:
# 1. Присутствуют все питомцы.
# 2. Хотя бы у половины питомцев есть фото.
# 3. У всех питомцев есть имя, возраст и порода.
# 4. У всех питомцев разные имена.
# 5. В списке нет повторяющихся питомцев.

def test_show_my_pets():
   pytest.driver.find_element(By.ID, 'email').send_keys(email)
   pytest.driver.find_element(By.ID,'pass').send_keys(password)
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   pytest.driver.find_element(By.XPATH, '// a[ @ href = "/my_pets"]').click()

   # Всего животных из статистики:
   stat_all_pets_find = pytest.driver.find_element(By.XPATH, '// div[@class =".col-sm-4 left"]')
   stat_parts = list(stat_all_pets_find.text.split())
   stat_all_pets = int(stat_parts[2])
   #Проверка конкретно под текущий доступ. Если количество питомцев не равно 3, нужно изменить количество
   # assert stat_all_pets == 3


   # 1. Присутствуют все питомцы
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr'))
   )
   all_pets = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
   assert len(all_pets) == stat_all_pets

   # 2. Хотя бы у половины питомцев есть фото
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//img[@style="max-width: 100px; max-height: 100px;"]'))
   )
   photos = pytest.driver.find_elements(By.XPATH, '//img[@style="max-width: 100px; max-height: 100px;"]')
   n = 0
   for i in range(len(photos)):
      if photos[i].get_attribute('src')!= '':
         n = n + 1
   assert n >= len(all_pets)/2

   # 3. У всех питомцев есть имя, возраст и порода
   # 3.1 Имя:
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '// tbody / tr / td[1]'))
   )
   names = pytest.driver.find_elements(By.XPATH, '// tbody / tr / td[1]')
   assert len(names) == len(all_pets)
   # 3.2 Возраст:
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '// tbody / tr / td[3]'))
   )
   ages = pytest.driver.find_elements(By.XPATH, '// tbody / tr / td[3]')
   assert len(ages) == len(all_pets)
   # 3.3 Порода:
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '// tbody / tr / td[2]'))
   )
   breeds = pytest.driver.find_elements(By.XPATH, '// tbody / tr / td[2]')
   assert len(breeds) == len(all_pets)

   # 4. У всех питомцев разные имена
   assert len(set(names)) == len(names)

   # 5. В списке нет повторяющихся питомцев
   # Список списков животных:
   all_pets_list = []

   for i in range(len(all_pets)):
      # Кортеж каждого животного:
      pets_cuple = names[i], ages[i], breeds[i]
      # Список из атрибутов каждого животного:
      pet_list = list(pets_cuple)
      all_pets_list.append(pet_list)

   # Уникальные значения в списке списков:
   unique = []
   for i in range(len(all_pets_list)):
      if all_pets_list[i] in unique:
         continue
      else:
         unique.append(all_pets_list[i])

   # Проверка уникальности животных:
   assert len(unique) == len(all_pets)


