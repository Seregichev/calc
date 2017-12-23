$(document).ready(function () {

    var items_list = $(".items-list");

    function FilterCategoryItems(filter_category_id, filter_power) {
        var data = {};
        data.filter_category_id = filter_category_id;
        data.filter_power = filter_power;


        var csrf_token = $('.items-list [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        var url = items_list.attr("action");
        console.log(data,url);
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success:function (data) {
                console.log("Request is arrived");
                console.log(data.filtered_item);
                $('.items-list div').html('');
                var items_powers=[];
                $.each(data.filtered_item, function (k, v) {
                    $('.items-list div').append('<p>'+ v.name +' '+ v.power +'</p>');
                    items_powers.push(v.power);
                });
                console.log($.type(items_powers));

                var items_powers = items_powers.filter(function(elem, pos) {
                    return items_powers.indexOf(elem) == pos;
                });
                console.log(items_powers);

                $('.dropdown-power ul').html('');
                $.each(items_powers, function (k, v) {
                    console.log(v);
                    $('.dropdown-power ul').append("<li class='dropdown-li power-dropdown-li' data-power='" +
                        v + "'><a href='#'>" + v + "</a></li>");
                });

            },
            error: function () {
                console.log("ERROR")

            }
        })
    }//

    $(document).on('click','.category-dropdown-li', function () {
        var current_category_name = $(this).data("name");
        var current_category_id = $(this).data("id");
        $(document).find('.button-category').text(current_category_name);
        $('.button-category').data('id',current_category_id);
        $(document).find('.button-power').text('Мощность');
        console.log(current_category_name);

        FilterCategoryItems(filter_category_id=current_category_id);
    });

    $(document).on('click','.power-dropdown-li', function () {
        var current_category_id = $('.button-category').data("id");
        var current_power = $(this).data("power");
        $(document).find('.button-power').text(current_power);
        console.log(current_category_id, current_power);

        FilterCategoryItems(filter_category_id=current_category_id, filter_power=current_power);
    });

    //Стилизуем формы выпадающих списков django в стиле bootstrap
    $('#id_voltage').addClass('form-control');
    $('#id_power').addClass('form-control');
    $('#id_type').addClass('form-control');
    $('#id_atributes').addClass('form-control');
    $('#id_manufacturer').addClass('form-control');
    
    // функция объединения столбца таблицы по вертикали
    function groupCellTable(tbl, coll, first_cell){
        var count = 1; // счетчик для подсчета ячеек которые нужно объединить
        var first_cell_id = tbl.rows[first_cell].cells[coll].id; // id первой ячейки
        var first_cell_context; // переменная для хранения содержания ячейки которая являеться с уникальным содержанием

        // В цикле обходим все ячейки таблицы по указанному столбцу
        for ( var i = 0; i < tbl.rows.length; i++ ) {
            // если выходит повторяющаяся ячейка, то 
            if (first_cell_context == tbl.rows[i].cells[coll].innerHTML){
                count++; // считаем ее
                document.getElementById(first_cell_id).setAttribute('rowspan', count); //вносим изменения в атибут для объединения 
                var remove_cell =  document.getElementById(tbl.rows[i].cells[coll].id); //получаем id текущей ячейки
                remove_cell.parentNode.removeChild(remove_cell); // удаляем текущую ячейку
            }
            // если ячейка уникальная
            else{
                first_cell_id = tbl.rows[i].cells[coll].id; //получаем id ячейки
                first_cell_context = tbl.rows[i].cells[coll].innerHTML; // получаем содержание ячейки для последующего сравнения
                count = 1;
            }

        }
    }

    groupCellTable(document.getElementById('table-estimate'), 0, 1);

});