$(function(){
    function tableData(){
        var index ='';
        var headTxt ='';
        $('.table-responsive table').each(function() {
            $('thead tr th').each(function() {

                index = $(this).index();
                headTxt = $(this).text();

                $('tbody tr').each(function() {
                    $(this).find('td').eq(index).attr('data-th',headTxt);
                });
            });
        });
    }
  tableData();
});
