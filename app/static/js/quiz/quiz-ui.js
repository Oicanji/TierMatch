quiz.ui = {
    super_allow_icon: '<i class="fa-regular fa-face-grin-stars"></i>',
    allow_icon: '<i class="fa-regular fa-face-grin-hearts"></i>',
    deny_icon: '<i class="fa-regular fa-face-tired"></i>',
    blocked: false,
    create: function (div_id, callback) {
        html = `
        <div class="fade-deny"></div>
        <div class="fade-allow"></div>
        <div class="fade-like"></div>

        <div class="meet-canva m-0 p-0">
            <div class="quiz-title mb-3 mt-3 text-center">
                <h3 class="m-0"></h3>
                <p class="text-muted"></p>
            </div>
            <div class="meet-char draggable" value="">
                <div class="moldure w-100 h-100">
                    <p class="status"></p>
                    <p class="name"></p>
                </div>
            </div>
            <div class="meet-next"></div>
            <div class="meet-option p-2 shadow">
                <div class="row justify-content-center">
                    <div class="col-4">
                        <button class="btn btn-primary btn-block" onclick="quiz.ui.handleFadeLeft();quiz.ui.handleMouseUpButton('left')" data-toggle="tooltip" data-placement="top" title="${quiz.deny}">
                            ${quiz.ui.deny_icon}
                        </button>
                    </div>
                    <div class="col-4">
                        <button class="btn btn-danger btn-block" onclick="quiz.ui.handleFadeRight();quiz.ui.handleMouseUpButton('right')" data-toggle="tooltip" data-placement="top" title="${quiz.allow}">
                            ${quiz.ui.allow_icon}
                        </button>
                    </div>
                    <div class="col-4">
                        <button class="btn btn-warning btn-block text-white" onclick="quiz.ui.handleFadeTop();quiz.ui.handleMouseUpButton('top')" data-toggle="tooltip" data-placement="top" title="${quiz.super_allow}">
                            ${quiz.ui.super_allow_icon}
                        </button>
                    </div>
                </div>
            </div>
        </div>`;
        document.getElementById(div_id).innerHTML = html;

        setTimeout(function () {
            callback();
            quiz.ui.setTitle();
            setTimeout(function () {
                //remove first click bug
                $('.draggable').click();
            }, 500);
        }, 500);
    },
    setTitle: function () {
        document.querySelector('.quiz-title h3').innerHTML = quiz.data.name;
        document.querySelector('.quiz-title p').innerHTML = quiz.data.description;
    },
    setQuestion: function () {
        document.querySelector('.meet-char').style.backgroundImage = `url(${quiz.logic.question.image})`;
        document.querySelector('.meet-char .name').innerHTML = quiz.logic.question.name;
    },
    setNextQuestion: function () {    
        //verificar caso exista mais uma pergunta para colocar no .meet-next, caso contrario deixar o background transparente
        if (quiz.logic.actual_question + 1 < quiz.logic.total_questions) {
            document.querySelector('.meet-next').style.backgroundImage = `url(${quiz.data.questions[quiz.logic.actual_question + 1].image})`;
        } else {
            document.querySelector('.meet-next').style.backgroundImage = `url()`;
        }
    },
    handleMouseUp: function () {
        if(quiz.ui.blocked) quiz.ui.resetPosition();

        event.preventDefault();

        var to_action = {};

        //gets the value of the draggable
        var value = draggable.getAttribute('value');
        if (value.includes('top')) {
            to_action['top'] = "-200%";
        } else {
            if (value.includes('left')) {
                to_action['left'] = "-50%";
            }
            if (value.includes('right')) {
                to_action['left'] = "150%";
            }
        }
        $(draggable).animate(
            to_action, {
            duration: "fast"
        });

        if(value == "") {
            quiz.ui.resetPosition();
        }else{
            if(value.includes('top')){
                value = "top";
            }
            quiz.logic.answer(value);
        }
        quiz.ui.update_fade("");
    },
    handleMouseUpButton: function (value) {
        event.preventDefault();

        var to_action = {};

        if (value.includes('top')) {
            to_action['top'] = "-200%";
        } else {
            if (value.includes('left')) {
                to_action['left'] = "-50%";
            }
            if (value.includes('right')) {
                to_action['left'] = "150%";
            }
        }
        $(draggable).animate(
            to_action, {
            duration: "fast"
        });

        if(value.includes('top')){
            value = "top";
        }
        quiz.logic.answer(value);
    
        quiz.ui.update_fade("");
    },

    resetPosition: function () {
        draggable.style.top = 'var(--title-height)';
        draggable.style.left = '50%';
        draggable.classList.remove('left');
        draggable.classList.remove('right');

        draggable.setAttribute('value', '');

        //esconder todos os tooltips
        $('[data-toggle="tooltip"]').tooltip('hide');
    },
    onMouseMove: function (e) {
        if(quiz.ui.blocked) return;

        const newX = e.clientX - offsetX;
        const newY = e.clientY - offsetY;

        var x_position = 0;
        var y_position = 0;

        //console.log(Math.abs(newY - window.innerHeight / 2));
        if (Math.abs(newX - window.innerWidth / 2) < 100 && Math.abs(newY - window.innerHeight / 2) > 700 && Math.abs(newY - window.innerHeight / 2) < 900) {
            quiz.ui.handleMouseUp();
        } else {
            draggable.style.left = newX + 'px';
            draggable.style.top = newY + 'px';

            if (lastX !== null && newX < lastX) {
                x_position = -1;
            } else if (lastX !== null && newX > lastX) {
                x_position = 1;
            } else {
                x_position = 0;
            }

            //console log if top or bottom
            if (lastY !== null && newY < lastY) {
                y_position = 1;
            } else if (lastY !== null && newY > lastY) {
                y_position = -1;
            } else {
                y_position = 0;
            }

            if (x_position == -1) {
                draggable.classList.remove('right');
                draggable.classList.add('left');
            } else if (x_position == 1) {
                draggable.classList.remove('left');
                draggable.classList.add('right');
            } else if (x_position == 0) {
                draggable.classList.remove('left');
                draggable.classList.remove('right');
            }

            lastX = newX;
            lastY = newY;
        }

        // console.log(e.clientX, e.clientY);

        var end_value = "";

        if (e.clientY < center_of_screen.y - y_trigger) {
            end_value += "top-";
        }
        if (e.clientX < (center_of_screen.x - x_trigger)) {
            end_value += "left";
        } else if (e.clientX > (center_of_screen.x + x_trigger)) {
            end_value += "right";
        } else {
            if (end_value == 'top-') {
                end_value = 'top';
            }
        }
        draggable.setAttribute('value', end_value);

        quiz.ui.update_fade(end_value);
    },
    block: function () {
        quiz.ui.blocked = true;
        //block all buttons
        document.querySelectorAll('.btn').forEach(function (element) {
            element.disabled = true;
        });
    },
    unblock: function () {
        quiz.ui.blocked = false;
        //block all buttons
        document.querySelectorAll('.btn').forEach(function (element) {
            element.disabled = false;
        });
    },

    /**
     * Exibe um loader na tela por um determinado tempo
     * @param {int} seconds 
     */
    loader: function (seconds = 1500) {

        // Crie um elemento `div` para o loader
        const loader = document.createElement('div');

        // Adicione um ícone e a mensagem "carregando..." no elemento `div`
        loader.innerHTML = `
            <div style="text-align:center;">
                <i class="fa-regular fa-face-grin-squint fa-spin fa-5x"></i>
                <p class="mt-3 h5">Carregando</p>
            </div>
        `;

        // Adicione estilos para posicionar o loader no centro da tela
        loader.style.position = 'fixed';
        loader.style.top = '50%';
        loader.style.left = '50%';
        loader.style.transform = 'translate(-50%, -50%)';
        loader.style.zIndex = '9999';

        // Adicione um fundo branco que cubra todos os outros elementos na tela
        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        overlay.style.zIndex = '9998';

        // Adicione o loader e o fundo branco ao corpo do documento
        document.body.appendChild(overlay);
        document.body.appendChild(loader);

        // Esconda o loader após 2000 segundos
        setTimeout(function () {
            overlay.style.display = 'none';
            loader.style.display = 'none';
        }, seconds);
    },

    handleFadeTop: function () {
        event.preventDefault();
        $('.fade-like').addClass('show-this');
        $('.fade-deny').removeClass('show-this');
        $('.fade-allow').removeClass('show-this');

        $('.moldure').addClass('like');
        $('.moldure').removeClass('deny');
        $('.moldure').removeClass('allow');

        $('.moldure .status').html(quiz.super_allow);
    },
    handleFadeBottom: function () {
        event.preventDefault();
        $('.fade-like').removeClass('show-this');

        $('.moldure').removeClass('like');
        $('.moldure').removeClass('deny');
        $('.moldure').removeClass('allow');

        $('.moldure .status').html('');
    },
    handleFadeLeft: function () {
        event.preventDefault();
        $('.fade-deny').addClass('show-this');
        $('.fade-allow').removeClass('show-this');

        $('.moldure').removeClass('like');
        $('.moldure').addClass('deny');
        $('.moldure').removeClass('allow');

        $('.moldure .status').html(quiz.deny);
    },

    handleFadeRight: function () {
        event.preventDefault();
        $('.fade-deny').removeClass('show-this');
        $('.fade-allow').addClass('show-this');

        $('.moldure').removeClass('like');
        $('.moldure').removeClass('deny');
        $('.moldure').addClass('allow');

        $('.moldure .status').html(quiz.allow);
    },

    handleHideAll: function () {
        $('.fade-deny').removeClass('show-this');
        $('.fade-allow').removeClass('show-this');
        $('.fade-like').removeClass('show-this');

        $('.moldure').removeClass('like');
        $('.moldure').removeClass('deny');
        $('.moldure').removeClass('allow');

        $('.moldure .status').html('');
    },


    update_fade: function (right_top) {
        //console.log(right_top);
        if (right_top.includes('top')) {
            quiz.ui.handleFadeTop();
        } else {
            if (right_top.includes('left')) {
                quiz.ui.handleFadeLeft();
            }
            if (right_top.includes('right')) {
                quiz.ui.handleFadeRight();
            }
        }

        if (right_top == "") {
            quiz.ui.handleHideAll();
        }
    },

    colorLoader: function () {
        //set in css root
        document.documentElement.style.setProperty('--deny-color', quiz.deny_color);
        document.documentElement.style.setProperty('--allow-color', quiz.allow_color);
        document.documentElement.style.setProperty('--super-allow-color', quiz.super_allow_color);

        document.documentElement.style.setProperty('--deny-color-50', 'rgba('+hexToRgb(quiz.deny_color)+', 0.5)');
        document.documentElement.style.setProperty('--allow-color-50', 'rgba('+hexToRgb(quiz.allow_color)+', 0.5)');
        document.documentElement.style.setProperty('--super-allow-color-50', 'rgba('+hexToRgb(quiz.super_allow_color)+', 0.5)');
    },

    alert: function (message, type = 'success') {
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        });
        setTimeout(function () {
            Toast.fire({
                    title: message,
                    icon: type,
            })
        }, 500);
    },
}

function hexToRgb(hex){
    // Verifica se o valor de entrada é um hex válido
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
      let c = hex.substring(1).split('');
      // Expande a abreviação de três caracteres para seis caracteres
      if(c.length == 3){
        c = [c[0], c[0], c[1], c[1], c[2], c[2]];
      }
      // Converte os valores hexadecimais em valores decimais
      c = '0x' + c.join('');
      // Retorna o valor RGB em formato de string
      return `${(c>>16)&255},${(c>>8)&255},${c&255}`;
    }
    // Caso contrário, retorna um valor nulo
    return null;
}

let offsetX, offsetY;
let lastX = null;
let lastY = null;

const x_trigger = 200;
const y_trigger = 150;

const center_of_screen = {
    x: window.innerWidth / 2,
    y: window.innerHeight / 2
}

// events for UI
var draggable
//if eventIniquiz is triggered, run this function
document.addEventListener('iniquiz', function () {
    draggable = document.querySelector('.draggable');

    draggable.addEventListener('mousedown', function (e) {
        if(quiz.ui.blocked) return;
        offsetX = e.clientX - draggable.offsetLeft;
        offsetY = e.clientY - draggable.offsetTop;
        document.addEventListener('mousemove', quiz.ui.onMouseMove);
    });

    document.addEventListener('mouseup', function (e) {
        if(quiz.ui.blocked) return;
        document.removeEventListener('mousemove', quiz.ui.onMouseMove);
        lastX = null;
        lastY = null;

        quiz.ui.handleMouseUp();
    });
});

//if window is resized, run this function
window.addEventListener('resize', function () {
    center_of_screen.x = window.innerWidth / 2;
    center_of_screen.y = window.innerHeight / 2;
});