    let stats = {
        wrongAnswers: 0,
        goodAnswers: 0,
        averageScore: 0
    };

    function getAverageScore(){
        stats.averageScore = parseFloat((10 / (stats.goodAnswers + stats.wrongAnswers) * stats.goodAnswers).toFixed(2));
    }

    let current_question = undefined;

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
      document.getElementById("question").innerText = word.question;
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
        }
        questions.push(question);
    }

    function check(){
        let answer = document.getElementById("input_box").value;
        if (answer == current_question.answer){
            stats.goodAnswers++;
            document.getElementById("answer_indicator").innerText = "Good!";
        } else {
            stats.wrongAnswers++;
            wrongAnswer(current_question);
            document.getElementById("answer_indicator").innerHTML = "Wrong. <br> Correct answer: " + current_question.answer;
        }
        getAverageScore();
        current_question = getWord();
        setWord(current_question);
    }

    document.getElementById("input_box").addEventListener("keydown", function(e) {
      if (e.keyCode === 13){
          check();
      }
    });

    current_question = getWord();
    setWord(current_question);