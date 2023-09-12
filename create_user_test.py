import sender_stand_request
import data


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""


def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    error_message = "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"
    assert response.json()["message"] == error_message


def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Аааааааааааааааа")


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааa")


def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")


def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")


def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и КО")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Тест 10. Ошибка
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    # Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_firstname(user_body)

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_firstname(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
