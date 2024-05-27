from flask import Flask, render_template, request, jsonify
import random
from gtts import gTTS
import os

app = Flask(__name__)

words = {
    'apple': 'яблоко',
    'orange': 'апельсин',
    'banana': 'банан',
    'grape': 'виноград',
    'watermelon': 'арбуз',
    'pineapple': 'ананас',
    'strawberry': 'клубника',
    'blueberry': 'черника',
    'cherry': 'вишня',
    'pear': 'груша'
}

attempts = {word: 0 for word in words.keys()}
guessed_words = []

def get_random_word():
    remaining_words = list(set(words.keys()) - set(guessed_words))
    if not remaining_words:
        return None
    english_word = random.choice(remaining_words)
    return english_word

def speak_word(word):
    tts = gTTS(text=word, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    os.system(f"start {filename}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next', methods=['GET'])
def next_word():
    word = get_random_word()
    if word is None:
        return jsonify({'word': 'Все слова угаданы!'})
    speak_word(word)  # Озвучиваем слово перед отправкой
    return jsonify({'word': word})

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    english_word = data.get('current_word')
    russian_word = words.get(english_word)
    if english_word is None or russian_word is None:
        return jsonify({'message': 'Ошибка: слово не найдено', 'correct': False})
    answer = data['answer'].strip().lower()
    if answer == russian_word.lower():
        guessed_words.append(english_word)
        return jsonify({'message': f"Правильно! Перевод слова '{english_word}' - '{russian_word}'.", 'correct': True})
    else:
        attempts[english_word] += 1
        if attempts[english_word] >= 3:
            guessed_words.append(english_word)
        return jsonify({'message': f"Неправильно. Перевод слова '{english_word}' - '{russian_word}'.", 'correct': False})

if __name__ == '__main__':
    app.run(debug=True, port=80)