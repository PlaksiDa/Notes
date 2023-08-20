import json
import os
import uuid
from datetime import datetime

NOTES_FILE = "notes.json"  # Имя файла для хранения заметок

# Загружает заметки из файла JSON, если файл существует
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    return []

# Сохраняет заметки в файл JSON
def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)

# Создает новую заметку и добавляет ее в список
def create_note(title, body):
    notes = load_notes()
    note_id = str(uuid.uuid4())  # Генерируем уникальный идентификатор с помощью UUID
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = {
        "id": note_id,
        "title": title,
        "body": body,
        "timestamp": timestamp
    }
    notes.append(note)
    save_notes(notes)

# Выводит список заметок, отсортированный по времени создания (от новых к старым)
def read_notes():
    notes = load_notes()
    
    # Сортируем заметки по времени в обратном порядке (от новых к старым)
    sorted_notes = sorted(notes, key=lambda note: note['timestamp'], reverse=True)
    
    for note in sorted_notes:
        print(f"ID: {note['id']}")
        print(f"Заголовок: {note['title']}")
        print(f"Время: {note['timestamp']}")
        print("=" * 30)
    
    selected_id = input("Введите ID заметки для просмотра текста (или '0' для возврата): ")
    if selected_id != '0':
        selected_note = next((note for note in notes if note['id'] == selected_id), None)
        if selected_note:
            print(f"Текст: {selected_note['body']}")
        else:
            print("Заметка не найдена.")

# Редактирует существующую заметку по ее идентификатору
def edit_note(note_id, new_title, new_body):
    notes = load_notes()
    edited = False
    for note in notes:
        if note['id'] == note_id:
            note['title'] = new_title
            note['body'] = new_body
            note['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            edited = True
            break
    
    if edited:
        save_notes(notes)  # Сохраняем изменения в заметках
        return True
    return False

# Удаляет заметку по ее идентификатору
def delete_note(note_id):
    notes = load_notes()
    notes = [note for note in notes if note['id'] != note_id]
    save_notes(notes)

# Основной цикл программы
def main():
    while True:
        print("1. Создать заметку")
        print("2. Читать заметки")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Выйти")
        
        choice = input("Введите ваш выбор: ")
        
        if choice == "1":
            title = input("Введите заголовок заметки: ")
            body = input("Введите текст заметки: ")
            create_note(title, body)
        elif choice == "2":
            read_notes()
        elif choice == "3":
            note_id = input("Введите идентификатор заметки для редактирования: ")
            new_title = input("Введите новый заголовок: ")
            new_body = input("Введите новый текст: ")
            if edit_note(note_id, new_title, new_body):
                print("Заметка успешно отредактирована.")
            else:
                print("Заметка не найдена.")
        elif choice == "4":
            note_id = input("Введите идентификатор заметки для удаления: ")
            delete_note(note_id)
            print("Заметка успешно удалена.")
        elif choice == "5":
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

if __name__ == "__main__":
    main()