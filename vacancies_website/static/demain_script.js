// if ("content" in document.createElement("template")) {
//
//     var data_file = ['Год',
//         'Динамика уровня средней зарплаты по годам',
//         'Динамика количества вакансий по годам',
//         'Динамика уровня средней зарплаты по годам\nдля профессии Java-разработчика',
//         'Динамика количества вакансий по годам\nдля профессии Java-разработчика'];
//
//     var tbody = document.querySelector("#tableBody");
//     var template = document.querySelector("#rowTemplate");
//
//     var clone = template.content.cloneNode(true);
//     var td = clone.querySelectorAll("td");
//
//     for (var i in clone){
//         for (j in td){
//
//         }
//     }
// }

$.ajax({
    url: 'vacancies_website/static/demain_table.csv',
    dataType: 'text',
}).done(successFunction);

	  function successFunction(data) {
        var allRows = data.split(/\r?\n|\r/);
        var table = '<table>';
        for (var singleRow = 0; singleRow < allRows.length; singleRow++) {
          if (singleRow === 0) {
            table += '<thead>';
            table += '<tr>';
          } else {
            table += '<tr>';
          }
          var rowCells = allRows[singleRow].split(',');
          for (var rowCell = 0; rowCell < rowCells.length; rowCell++) {
            if (singleRow === 0) {
              table += '<th>';
              table += rowCells[rowCell];
              table += '</th>';
            } else {
              table += '<td>';
              table += rowCells[rowCell];
              table += '</td>';
            }
          }
          if (singleRow === 0) {
            table += '</tr>';
            table += '</thead>';
            table += '<tbody>';
          } else {
            table += '</tr>';
          }
        }
        table += '</tbody>';
        table += '</table>';
        $('body').append(table);
      }