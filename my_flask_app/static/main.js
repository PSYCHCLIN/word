async function checkAnswer() {
    const currentWord = document.getElementById('word').innerText;
    const answer = document.getElementById('answer').value;
    const response = await fetch('/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ current_word: currentWord, answer: answer })
    });
    const result = await response.json();
    alert(result.message);
    if (result.correct) {
        getNextWord();
    }
}

async function getNextWord() {
    const response = await fetch('/next');
    const result = await response.json();
    document.getElementById('word').innerText = result.word;
    document.getElementById('answer').value = '';
}

document.addEventListener('DOMContentLoaded', function() {
    getNextWord();

    document.getElementById('answer').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            checkAnswer();
        }
    });
});