const eventIniquiz = new Event('iniquiz');
var quiz = {

    data: {},

    /**
     * Alias para as respostas
     */
    super_allow: 'Super Aprovado',
    allow: 'Aprovado',
    deny: 'Recusado',

    /**
     * Cores do quiz
     */
    super_allow_color: '#00b4d8',
    allow_color: '#ff595e',
    deny_color: '#f9c74f',

    div_main: 'div.cloud-container',

    start : function(json) {

        //instancias do quiz
        quiz.data = json.quiz;

        quiz.allow = json.quiz.allow_alias;
        quiz.deny = json.quiz.deny_alias;
        quiz.super_allow = json.quiz.super_allow_alias;

        quiz.allow_color = json.quiz.allow_color;
        quiz.deny_color = json.quiz.deny_color;
        quiz.super_allow_color = json.quiz.super_allow_color;

        quiz.ui.colorLoader();

        quiz.ui.loader();
        callback = () => {
            document.dispatchEvent(eventIniquiz)
        }
        quiz.ui.create('quiz', callback);
        
        //set initial question
        quiz.logic.init();
        quiz.ui.setQuestion();
    },
}