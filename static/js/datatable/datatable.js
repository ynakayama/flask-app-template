jQuery(function($){
    $("#datatable").DataTable({
      "language": {
        "sEmptyTable":     "該当の明細はございません",
        "sInfo":           " _TOTAL_ 件中 _START_ から _END_ まで表示",
        "sInfoEmpty":      " 0 件中 0 から 0 まで表示",
        "sInfoFiltered":   "（全 _MAX_ 件より抽出）",
        "sInfoPostFix":    "",
        "sInfoThousands":  ",",
        "sLengthMenu":     "_MENU_ 件表示",
        "sLoadingRecords": "読み込み中...",
        "sProcessing":     "処理中...",
        "sSearch":         "検索:",
        "sZeroRecords":    "一致する明細はございません",
        "oPaginate": {
          "sFirst":    "先頭",
          "sLast":     "最終",
          "sNext":     "次",
          "sPrevious": "前"
        },
        "oAria": {
          "sSortAscending":  ": 列を昇順に並べ替えるにはアクティブにする",
          "sSortDescending": ": 列を降順に並べ替えるにはアクティブにする"
        }
      },
      lengthMenu:[5, 10, 15, 20, 50, 100],
      displayLength: 5,
      stateSave: false,
      order: [],
      "columnDefs": [
        {"targets": 0, "searchable": false},
        {"targets": 1, "searchable": false}
      ]
   })
});
