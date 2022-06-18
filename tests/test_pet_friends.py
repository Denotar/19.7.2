from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_key, invalid_pet_id, too_long_pet_name
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """Проверяем возможность авторизации с неверным email"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    print("\nAccess Denied because of bad email")


def test_get_api_key_with_bad_pass(email=valid_email, password=invalid_password):
    """Проверяем возможность авторизации с неверным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    print("\nAccess Denied because of bad password")


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем возможность получения списка питомцев с неверным ключем"""
    status, result = pf.get_list_of_pets(invalid_key, filter)

    assert status == 403
    print("\n403 because of invalid pet id")


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_too_big_age(name='Барбоскин', animal_type='двортерьер',
                                     age='400', pet_photo='images/cat1.jpeg'):
    """Проверяем возможность создаия питомца с слишком большим возрастом"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert int(age) not in range(0, 50)
    print("\nACHTUNG ACHTUNG ACHTUNG \nWorks with bad age")


def test_add_new_pet_with_negative_age(name='Барбоскин', animal_type='двортерьер',
                                     age='-4', pet_photo='images/cat1.jpeg'):
    """Проверяем возможность создаия питомца с отрицательным возрастом"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert int(age) not in range(0, 50)
    print("\nACHTUNG ACHTUNG ACHTUNG \nWorks with bad age")


def test_add_new_pet_with_no_name(name='', animal_type='двортерьер',
                                  age='400', pet_photo='images/cat1.jpeg'):
    """Проверяем возможность создаия питомца с пустым имененем"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    print("\nACHTUNG ACHTUNG ACHTUNG \nWorks with no name")


def test_add_new_pet_without_one_arg(name='Барбоскин', animal_type='cat',
                                     age='4'):
    """Проверяем вомзожность создания питомца с недостаточным количеством аргументов"""
    print("\nFAILED is expected result for this test")
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)
    assert status == 200


def test_add_new_pet_with_extra_arg(name='бобик', animal_type='cat',
                                     age='4', pet_photo='images/cat1.jpeg', color='red'):
    """Проверяем возможность создания питомца с дополнительным аргументов"""
    print("\nFAILED is expected result for this test")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo, color)
    assert status == 200


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_deleting_unknown_pet():
    """Проверяем возможность удаления питомца с несуществующим id"""
    print("\nFAILED is expected result for this test")
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    total_pets = len(my_pets['pets'])
    status, _ = pf.delete_pet(auth_key, invalid_pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert len(my_pets['pets']) == total_pets - 1


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_too_long_pet_name(name=too_long_pet_name, animal_type='Котэ', age=5):
    """Проверяем отсутствие возможности делать слишком длинные имена питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert len(result['name']) <= 15

    else:
        raise Exception("There is no my pets")