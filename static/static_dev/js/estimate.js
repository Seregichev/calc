$(document).ready(function () {

    
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