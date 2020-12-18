const filters = document.getElementById('filters'),
      filtersBtn = document.getElementById('filtersBtn'),
      arrow = document.getElementById('arrow'),
      info = document.getElementById('info');

filters.style.display = 'none';

count = 0;

filtersBtn.addEventListener('click', () => {
    if (count === 0) {
        filters.style.display = 'block';
        count++
        arrow.style.transform = 'rotate(180deg)'
    } else {
        filters.style.display = 'none';
        count = 0;
        arrow.style.transform = 'rotate(0)'
    }
});



$('.select').on('change', function () {
    let value = $(this).val();
    let key = $(this).attr('name');

    $.ajax({
        type: 'GET',
        url: '/query-filter',
        data: key + '=' + value,
        success: function (result) {
            $('.auto-list').html(result);
        },
        error: function () {
            alert("Ошибка выбора фильтров")
        }
    });
});