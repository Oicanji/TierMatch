quiz.result = {
    init: function (stats) {
        html = `
            <div class="container p-5 mt-3 w-100 shadow rounded">
                <h3>Você terminou o quiz "${quiz.data.name}"!</h3>
                <p>Veja abaixo os resultados:</p>
                <div class="row" id="graficos">
                    <div class="col-md-6 col-sm-6">
                        <canvas id="render_booleans"></canvas>
                    </div>
                    <div class="col-md-6 col-sm-6">
                        <canvas id="render_percent"></canvas>
                    </div>
                </div>
                <hr class="mt-3 mb-3">
                <div class="super-allow-list mt-3 mn-1">
                    <h5>${quiz.super_allow}:</h5>
                </div>
                <hr class="mt-1 mb-1">
                <div class="allow-list mt-1 mn-1">
                    <h5>${quiz.allow}:</h5>
                </div>
                <hr class="mt-1 mb-1">
                <div class="deny-list mt-1 mn-1">
                    <h5>${quiz.deny}:</h5>
                </div>
            </div>
        `;
        document.querySelector('body '+ quiz.div_main).innerHTML = html;

        quiz.result.render_booleans(stats);
        quiz.result.render_porcent(stats);
        quiz.result.render_lists(stats);
    },
    render_lists: function (stats) {
        items_allow = 0;
        items_deny = 0;
        items_super_allow = 0;

        for(var i = 0; i < stats.length; i++) {
            //create a div 50px x 50px with the image
            var item = document.createElement('div');
            item.classList.add('list-item');
            item.style.backgroundImage = `url(${stats[i].image})`;
            item.style.backgroundSize = 'cover';
            item.style.backgroundPosition = 'center';
            item.style.width = '50px';
            item.style.height = '50px';
            item.style.margin = '5px';
            item.style.borderRadius = '30%';
            item.style.display = 'inline-block';
            item.style.boxShadow = '0px 0px 5px 0px rgba(0,0,0,0.75)';
            item.style.cursor = 'pointer';
            item.setAttribute('data-toggle', 'tooltip');
            item.setAttribute('data-placement', 'top');
            item.setAttribute('title', stats[i].name);
            
            switch(stats[i].answer) {
                case 'super_allow':
                    document.querySelector('div.super-allow-list').appendChild(item);
                    items_super_allow++;
                    break;
                case 'allow':
                    document.querySelector('div.allow-list').appendChild(item);
                    items_allow++;
                    break;
                case 'deny':
                    document.querySelector('div.deny-list').appendChild(item);
                    items_deny++;
                    break;
            }
        }
        if(items_super_allow == 0) {
            var item = document.createElement('p');
            item.innerHTML = 'Não há itens nesta lista';
            document.querySelector('div.super-allow-list').appendChild(item);
        }
        if(items_allow == 0) {
            var item = document.createElement('p');
            item.innerHTML = 'Não há itens nesta lista';
            document.querySelector('div.allow-list').appendChild(item); 
        }
        if(items_deny == 0) {
            var item = document.createElement('p');
            item.innerHTML = 'Não há itens nesta lista';
            document.querySelector('div.deny-list').appendChild(item);
        }

        if(items_super_allow == 0 && items_allow == 0) {
            // remover '#graficos'
            $('#graficos').html(`
                <div class="col-md-12 col-sm-12 p-4">
                    <p class="text-center">Não há gráficos para serem exibidos</p>
                </div>`);
        }
    },

    render_booleans: function (stats) {
        // Cria um novo elemento canvas
        var canvas = document.createElement('canvas');
        canvas.id = 'render_booleans';
        canvas.width = 400;
        canvas.height = 400;
    
        // Adiciona o canvas ao body
        document.querySelector('body').appendChild(canvas);
    
        // Cria um objeto vazio para armazenar as somas de cada nome
        var sumByName = {};
    
        // Itera sobre o objeto stats e adiciona os valores booleanos ao objeto "sumByName"
        for (var i = 0; i < stats.length; i++) {
            double_value = false;
            if (stats[i].stats == undefined) continue; // Se o objeto stats não existir, pula para a próxima iteração
            if (stats[i].answer == 'deny') continue; // Se a resposta for "deny", pula para a próxima iteração
            if (stats[i].answer == 'super_allow') double_value = true; // Se a resposta for "super_allow", o valor booleano será duplicado
            //percorre o objeto stats
            for (var key in stats[i].stats) {
                //se o valor for booleano
                if (stats[i].stats[key].type == 'boolean') {
                    //adiciona o valor ao objeto sumByName
                    var name = stats[i].stats[key].name;
                    if (!sumByName[name]) sumByName[name] = 0;
                    sumByName[name] += stats[i].stats[key].value ? 1 : 0;
                    if (double_value) sumByName[name] += stats[i].stats[key].value ? 1 : 0;
                }
            }
        }
    
        // Converte o objeto sumByName em um array de objetos com as propriedades "name" e "value"
        var booleans = [];
        for (var name in sumByName) {
            booleans.push({
                name: name,
                value: sumByName[name]
            });
        }
    
        // Cria um array de cores para as fatias do gráfico, com base no nome do objeto
        var colors = [];
        for (var i = 0; i < booleans.length; i++) {
            colors.push(randomColor());
        }
    
        // Cria o gráfico de pizza
        var ctx = document.getElementById('render_booleans').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: booleans.map(function (item) { return item.name; }),
                datasets: [{
                    backgroundColor: colors,
                    data: booleans.map(function (item) { return item.value; })
                }]
            }
        });
    },
    
    render_porcent: function (stats) {
        // Itera sobre o objeto stats e adiciona os objetos do tipo "porcentage" ao array "porcentages"
        var porcentages = [];
        for (var i = 0; i < stats.length; i++) {
            double_value = false;
            if (stats[i].stats == undefined) continue; // Se o objeto stats não existir, pula para a próxima iteração
            if (stats[i].answer == 'deny') continue; // Se a resposta for "deny", pula para a próxima iteração
            if (stats[i].answer == 'super_allow') double_value = true; // Se a resposta for "super_allow", o valor booleano será duplicado
            //percorre o objeto stats
            for (var key in stats[i].stats) {
                //se o valor for porcentage
                if (stats[i].stats[key].type == 'porcentage') {
                    //adiciona o objeto ao array
                    if (double_value) porcentages.push(stats[i].stats[key]);
                    porcentages.push(stats[i].stats[key]);
                }
            }
        }

        // Calcula a média das porcentagens com o mesmo nome
        var porcentagesByName = {};
        porcentages.forEach(function (item) {
            if (porcentagesByName[item.name] === undefined) {
                porcentagesByName[item.name] = {
                    value: item.value,
                    count: 1
                };
            } else {
                porcentagesByName[item.name].value += item.value;
                porcentagesByName[item.name].count++;
            }
        });
        var porcentagesAverages = [];
        for (var key in porcentagesByName) {
            var avg = porcentagesByName[key].value / porcentagesByName[key].count;
            porcentagesAverages.push({
                name: key,
                value: avg
            });
        }

        // Cria as cores para os dados do gráfico
        var colors = [];
        for (var i = 0; i < porcentagesAverages.length; i++) {
            color_no_transparency = randomColor();
            color_with_transparency = color_no_transparency + '55';
            colors.push(color_with_transparency);
        }

        // Cria o gráfico de radar
        var ctx = document.createElement('canvas');
        ctx.setAttribute('id', 'render_percent');
        // Adiciona no lugar do canvas render_percent
        document.querySelector('#render_percent').replaceWith(ctx);

        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: porcentagesAverages.map(function (item) { return item.name; }),
                datasets: [{
                    data: porcentagesAverages.map(function (item) { return item.value; }),
                    backgroundColor: colors
                }]
            },
            options: {
                tooltips: { enabled: false },
                hover: { mode: null },
                plugins: {
                    datalabels: {
                        display: false
                    }
                },
                title: {
                    display: true,
                    text: 'Porcentages Radar Chart'
                }
            }
        });

    },

    format: function(){
        value = {
            "answer": quiz.data.id,
            "answers": quiz.logic.respost,
        }
        return value;
    },

    send: function(){
        $.ajax({
            url: 'http://localhost:3000/quiz',
            type: 'POST',
            data: JSON.stringify(quiz.logic.format()),
            contentType: 'application/json',
            error: function (data) {
                quiz.ui.alert('Erro ao enviar os dados', 'error');
                console.log(data);
            }
        });
    }
}

var coolors = [
    "#ff595e",
    "#ff924c",
    "#ffca3a",
    "#c5ca30",
    "#8ac926",
    "#36949d",
    "#1982c4",
    "#4267ac",
    "#577590",
    "#565aa0",
    '#6a4c93'
];

function randomColor() {
    if(coolors.length == 0){
        var hex = "#";
        for (var j = 0; j < 6; j++) {
            hex += Math.floor(Math.random() * 16).toString(16);
        }
        return hex;
    }
    select = Math.floor(Math.random() * coolors.length);
    
    color_select = coolors[select];
    coolors.splice(select, 1);
    return color_select;    
}