jQuery(($) => {

    // Уменьшаем на 1
    $(document).on("click", ".input-number__minus", function () {
        let total = $(this).next();
        if (total.val() > 1) {
            total.val(+total.val() - 1);
        }
    });

    // Увеличиваем на 1
    $(document).on("click", ".input-number__plus", function () {
        let total = $(this).prev();
        total.val(+total.val() + 1);
    });

    // Запрещаем ввод текста 
    document.querySelectorAll('.input-number__input').forEach(function (el) {
        el.addEventListener('keydown', function (event) {
            // Разрешаем: backspace, delete, tab
            if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 ||
                // Ctrl+A
                (event.keyCode == 65 && event.ctrlKey === true) ||
                // ← →
                (event.keyCode >= 35 && event.keyCode <= 39)) {
                return;
            } else {
                // Только цифры
                if ((event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105)) {
                    event.preventDefault();
                }
            }

        });
    });
});

// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}