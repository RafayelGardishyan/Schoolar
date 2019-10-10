let options = {
    colors: {
        green: "#007410",
        red: "#7b0100",
        yellow: "#be9914"
    }
};

data.current_answer = "";
data.current_question = "";
data.input_answer= "";
data.stats = {
    wrongAnswers: 0,
    goodAnswers: 0,
    averageScore: 0,
    initialQuestionAmount: questions.length,
    totalQuestionAmount: NaN,
    difficultWordsAmount: NaN,
    startTime: [d.getHours(), d.getMinutes(), d.getSeconds()],
    endTime: [NaN, NaN, NaN]
};

let app = new Vue({
    el: test_module,
    delimiters: ['[[', ']]'],
    data: data,
    methods: {
        check_translation: function (event) {
            let correct_answer;
            if (data.settings.mode !== "shuffle"){
                if (data.settings.question_subject === "question"){
                    correct_answer = data.current_answer;
                } else if (data.settings.question_subject === "answer"){
                    correct_answer = data.current_question;
                }
            } else {
                if (data.settings.question_subject === "question"){
                    correct_answer = data.current_question;
                } else if (data.settings.question_subject === "answer"){
                    correct_answer = data.current_answer;
                }
            }


            if (data.settings.case_sensitive === "no") {
            data.input_answer = data.input_answer.toLowerCase();
            correct_answer = correct_answer.toLowerCase();
            }

            if (data.input_answer === correct_answer) {
                data.stats.goodAnswers++;
                data.correct_indicator = "Correct";
                document.getElementById("answer_indicator").style.color = good_color;
                document.getElementById("question").style.color = good_color;
            } else {
                data.stats.wrongAnswers++;
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
                document.getElementById("question").style.color = text_color;
                getAverageScore();
                previous_question = current_question;
                current_question = getWord();
                setWord(current_question);
            }, delay);
        }
    }
});