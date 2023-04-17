$('body').append(`
    <input type="hidden" id="attributes_list" name="attributes_list" value="[]">
`);

input_attributes = document.querySelector('#attributes_list');

const attributes = {
    list: [],
    list_use: [],
    change: function () {
        //remove use param
        list_clear = [];
        for (const attribute of attributes.list) {
            list_clear.push({
                name: attribute.name,
                type: attribute.type,
                value: attribute.value
            });
        }
        input_attributes.value = JSON.stringify(list_clear);
        
        attributes.table.refresh();
        attributes.table.table_has_empty();
    },
    quiz_init : function (questions=0) {
        $('#button_reset_use_attribute').attr('onClick', 'attributes.not_use_all()');
        
        if(questions == 0){
            $('#use_attributes').css('display','none');
            attributes.table.table_use_visible = true;
        }else{
            for (const question of questions) {
                for (const attribute of question.attributes) {
                    attributes.add_all(attribute.name, attribute.type, attribute.value);
                }
            }
        }
    },
    add_all: function (name, type, value, used = false) {
        //check if attribute is in list
        for (const attribute of attributes.list) {
            if(attribute.name == name){
                return;
            }
        }
        attributes.list.push({
            name: name,
            type: type,
            value: value,
            use: used
        });
    },
    add_new: function (name, type, value) {
        attributes.add_all(name, type, value, true);
        attributes.list_use.push({
            name: name,
            type: type,
            value: value
        });
        attributes.change();
    },
    remove: function (name) {
        attributes.list_use = attributes.list_use.filter(function (attribute) {
            return attribute.name != name;
        });

        //search in list to is attribute and set use false
        for (const attribute_list of attributes.list) {
            if(attribute_list.name == name){
                attribute_list.use = false;
                break;
            }
        }
    },
    not_use_all: function () {
        for (const attribute of attributes.list) {
            attribute.use = false;
        }
        attributes.list_use = [];

        attributes.change();
    },
    get: function (use_list) {
        for(const attribute of use_list){
            attributes.use(attribute.name, attribute.type, attribute.value);
            //search in list to is attribute and set use true
            for (const attribute_list of attributes.list) {
                if(attribute_list.name == attribute.name){
                    attribute_list.use = true;
                    break;
                }
            }
        }
    },
}

attributes.table = {
    table_use_visible: false,
    add: function (name, type, value) {
        attributes.add_new(name, type, value);
        if (attributes.table.table_use_visible == true) {
            $('#use_attributes').slideDown();
        }
    },
    remove(tr_id) {
        tr = $(tr_id);
        attributes_name = $(tr).children()[0].innerHTML;
        attributes_type = $(tr).children()[1].innerHTML;
        attributes_value = $(tr).children()[2].innerHTML;

        attributes.remove(attributes_name);

        attributes.change();
    },
    print(attribute, click_to_add=false) {

        del = `
        <td>
            <button type="button" class="btn btn-danger" onclick="attr_delete('#attr_${attribute.name}')">Remover</button>
        </td>`;
        if(!click_to_add){
            del = '';
        }

        return `
        <tr id="attr_${attribute.name}"  ${!click_to_add ? 'onClick="attr_add(\''+attribute.name+'\', \''+attribute.type+'\', \''+attribute.value+'\')"' : ''}>
            <td>${attribute.name}</td>
            <td>${attribute.type}</td>
            <td>${attribute.value}</td>
            ${del}
        </tr>
        `;
    },
    refresh: function () {
        use_list = '';
        all_list = '';

        $table_use = $('#table_use_attribute');
        $table_all = $('#table_all_attribute');

        for (const attribute of attributes.list) {
            if(attribute.use == true){
                use_list += attributes.table.print(attribute, true);
            }else{
                all_list += attributes.table.print(attribute, false);
            }
        }

        $($table_use).html(use_list);
        $($table_all).html(all_list);
    },
    table_has_empty: function () {
        $table_use = $('#table_use_attribute');
        $table_all = $('#table_all_attribute');
        if($($table_use).html() == ''){
            $('#use_attributes').slideUp();
        } else {
            $('#use_attributes').slideDown();
        }
        if($($table_all).html() == ''){
            $('#all_attributes').slideUp();
        } else {
            $('#all_attributes').slideDown();
        }
        
    }
}
attributes.ui = {
    new: function (name, type, value) {
        name = name.toLowerCase();
        //capitalize first letter
        name = name.charAt(0).toUpperCase() + name.slice(1);

        if(name == '' || type == '' || value == '' || type == 'Escolha...'){
            return false;
        }

        for (const attribute of attributes.list) {
            if(attribute.name == name){
                return false;
            }
        }

        attributes.table.add(name, type, value);

        attributes.ui.reset();

        return true;
    },
    reset: function () {
        $('#attribute_name').val('');
        $('#attribute_type').val('');
        $('#attribute_value').val('');

        attributes.change();
    }
}

function attr_delete(id){
    attributes.table.remove(id);
}
function attr_add(id){
    attributes.table.add(id);
}

$('#question-div');

$('#button_attribute').on('click', function () {
    deu_certo = attributes.ui.new($('#attribute_name').val(), $('#attribute_type').val(), $('#attribute_value').val());
    if(!deu_certo){
        Swal.fire({
            title: 'Erro',
            text: 'Atributo já cadastrado, ou parâmetros inválidos!',
            icon: 'error',
            confirmButtonText: 'Ok'
        });
    }
});

$('#button_reset_use_attribute').on('click', function () {
    attributes.not_use_all();
    attributes.ui.reset();
});

$('#type_attribute').on('change', function () {
    if($(this).val() == 'porcent'){
        $('#explicao_burra').html(`
            <small> No final, usaremos um valor para calcular a aprovação de um atributo, somando todos os seus valores.. </small>
            `);
    }
    if($(this).val() == 'boolean'){
        $('#explicao_burra').html(`
            <small> Ao final do quiz, esse valor será convertido em um ponto unitário no cálculo comparativo geral. </small>
        `);
    }
});