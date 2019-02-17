    let good_color = "#007410";
    let bad_color = "#7b0100";
    let half_color = "#be9914";

    let delay = settings.delay;

    let stats = {
        wrongAnswers: 0,
        goodAnswers: 0,
        averageScore: 0
    };

    function getAverageScore(){
        stats.averageScore = parseFloat((10 / (stats.goodAnswers + stats.wrongAnswers) * stats.goodAnswers).toFixed(2));
    }

    let current_question = undefined;
    let previous_question = undefined;

      difficult_questions = [];

    function post(path, params) {
    let method = "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    let form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(let key in params) {
        if(params.hasOwnProperty(key)) {
            let hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
    }

    function getWord() {
        let word = questions.splice(Math.floor(Math.random()*questions.length), 1)[0];
        if (word == previous_question && questions.length != 1){
            questions.push(word);
            return getWord();
        }
        if (word == undefined){
            post("/app/test/register/", {
                'average_score': stats.averageScore,
                'difficult_words': JSON.stringify(difficult_questions),
                'csrfmiddlewaretoken': csrf_token
            });
        }else {
          return word;
        }
      }

    function setWord(word) {
        if (settings.question_subject === "question") {
            document.getElementById("question").innerText = word.question;
        } else {
            document.getElementById("question").innerText = word.answer;
        }
        document.getElementById("input_box").value = "";
    }

    function include(arr, obj) {
    for(let i=0; i<arr.length; i++) {
        if (arr[i] == obj) return true;
    }
    return false;
}

    function wrongAnswer(question){
        if (!include(difficult_questions, question)){
            difficult_questions.push(question);
            difficult_questions.push(question);
        }
        questions.push(question);
    }

    function check(){
        let good_answer;
        if (settings.mode === "question") {
            good_answer = current_question.answer;
        } else {
            good_answer = current_question.question;
        }
        let answer = document.getElementById("input_box").value;
        if (answer == good_answer){
            stats.goodAnswers++;
            document.getElementById("answer_indicator").innerText = "Correct";
            document.getElementById("answer_indicator").style.color = good_color;
            document.getElementById("question").style.color = good_color;
        } else {
            stats.wrongAnswers++;
            wrongAnswer(current_question);
            document.getElementById("answer_indicator").innerHTML = "Wrong";
            document.getElementById("answer_indicator").style.color = bad_color;
            document.getElementById("question").style.color = bad_color;
            document.getElementById("correct_answer").innerText = good_answer;
            document.getElementById("wrong_answer").style.display = 'block';
        }
        document.getElementById("question_result").style.display = 'block';
        setTimeout(function () {
            document.getElementById("question_result").style.display = 'none';
            document.getElementById("wrong_answer").style.display = 'none';
            document.getElementById("question").style.color = '#000000';
            getAverageScore();
            previous_question = current_question;
            current_question = getWord();
            setWord(current_question);
        }, delay);
    }

    document.getElementById("input_box").addEventListener("keydown", function(e) {
      if (e.keyCode === 13){
          check();
      }
    });

    function flip(){
        let good_answer;
        if (settings.question_subject === "question") {
            good_answer = current_question.answer;
        } else {
            good_answer = current_question.question;
        }
        document.getElementById('correct_answer_fc').innerText = good_answer;
        document.getElementById('correct_answer_fc').style.display = 'block';
        document.getElementById('flip_button').style.display = 'none';
        document.getElementById('choose_menu').style.display = 'block';
    }

    function reset_flip(){
        document.getElementById("question_result").style.display = 'block';
        setTimeout(function () {
            document.getElementById("question_result").style.display = 'none';
            document.getElementById('flip_button').style.display = 'block';
            document.getElementById('choose_menu').style.display = 'none';
            document.getElementById('correct_answer_fc').style.display = 'none';
            document.getElementById("question").style.color = '#000000';
            getAverageScore();
            previous_question = current_question;
            current_question = getWord();
            setWord(current_question);
        }, delay);
    }

    function good(){
        stats.goodAnswers++;
        document.getElementById("answer_indicator").innerText = "Correct";
        document.getElementById("answer_indicator").style.color = good_color;
        document.getElementById("question").style.color = good_color;
        reset_flip();
    }

    function wrong(){
        stats.wrongAnswers++;
        wrongAnswer(current_question);
        document.getElementById("answer_indicator").innerText = "Wrong";
        document.getElementById("answer_indicator").style.color = bad_color;
        document.getElementById("question").style.color = bad_color;
        reset_flip();
    }

    function half_good(){
        stats.goodAnswers++;
        stats.wrongAnswers++;
        wrongAnswer(current_question);
        document.getElementById("answer_indicator").innerText = "Almost correct";
        document.getElementById("answer_indicator").style.color = half_color;
        document.getElementById("question").style.color = half_color;
        reset_flip();
    }

    current_question = getWord();
    setWord(current_question);


    if (settings.mode === 'flashcards'){
        document.getElementById('translate_mode').style.display = 'none';
    } else if (settings.mode === 'translate'){
        document.getElementById('flashcard_mode').style.display = 'none';
    }