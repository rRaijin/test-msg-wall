$(document).ready(function () {

    /*Скрываю/показываю комментарии*/
    $(document).on('click', '.show-content', function () {
        $(this).parent().next().toggleClass('special');
        $(this).parent().next().children().find('.all-comments').toggleClass('special');
    });

    /*Скрипт добавления сообщения на стену*/
    $('.message_form').on('submit', function (e) {
        e.preventDefault();
        var form = $(this);
        $.post(form.attr('action'), form.serialize()).done(function (data) { /*ajax-запрос для добавления сообщения*/
            $('.message-container').prepend( /*Новые сообщения добавляются сверху*/
                "<div class='message-wrapper'>" +
                    "<div class='message-body'>" +
                    "<a class='edit-message'"+"href='"+data.update_url+"'>редактировать сообщение</a>"+
                    "<p class='msg-body'>" + data.body + "</p>" + "Сообщение опубликовано" +
                    "<span class='message-author'>" + data.author + "</span>" +
                    "<span class='message-date'"+"data-url='"+data.create_url+"'"+">" + data.date + "</span>" +
                    "<a class='reply'>комментировать</a>" + "<p class='show-content'>Показать все комментарии</p>" +
                    "</div>" + "<div class='all-comments special'></div>" +
                "</div>"
            );
        });
        form.find("textarea").val(''); /*Чистим форму после добавления сообщения*/
    });

    /*Скрипт для получения формы сообщения для редактирования*/
    $(document).on('click', '.edit-message', function(e) {
        e.preventDefault();
        var edited_obj = $(this).parent(),
            val_for_edit = edited_obj.find('p').first().text(), /*Получаю начальное значение редактируемого сообщения для вставки в форму*/
            action = $(this).attr('href'),
            clone = $('.message_form').clone().attr('action', action).css('display', 'block'); /*Клонирую форму добавления сообщения*/

        $(this).after(clone);
        clone.addClass('edit_message_form').removeClass('message_form');
        $('.edit_message_form p textarea').val(val_for_edit);
        clone.attr('onclick', editmessage()); /*Привязываю к измененному(новому) объекту событие*/
    });

    /*Функция для редактирования сообщения*/
    function editmessage() {
        $('.edit_message_form').on('submit', function (e) {
            e.preventDefault();
            var form = $(this);
            $.post(form.attr('action'), form.serialize()).done(function (data) {
                form.parent().replaceWith(/*Заменяю редактриуемые данные на новые*/
                    "<div class='message-body'>" +
                    "<a class='edit-message'"+"href='"+data.update_url+"'>редактировать сообщение</a>"+
                    "<p class='msg-body'>" + data.body + "</p>" + "Сообщение отредактировано" +
                    "<span class='message-author'>" + data.author + "</span>" +
                    "<span class='message-date'"+"data-url='"+data.create_url+"'"+">" + data.date + "</span>" +
                    "<a class='reply'>комментировать</a>" + "<p class='show-content'>Показать все комментарии</p>" +
                    "</div>"
                );
                $('.void-class').remove();
                form.remove();/*Удаляю форму*/
            });
        });
    }

    /*Скрипт для клонирования формы для добавления комментария*/
    $(document).on('click','.comment, .reply', function(e) {
        var $action = $(this).prev(),
            action = $action.attr('data-url'),
            clone = $('.comment_form').clone().attr('action', action).css('display', 'block');

        $(this).after(clone);
        clone.addClass('add_comment_form').removeClass('comment_form');
        clone.attr('onclick', comment());
    });

    /*Функция для добавления комментария*/
    function comment() {
        $('.add_comment_form').on('submit', function (e) {
            e.preventDefault();
            var form = $(this);
            $.post(form.attr('action'), form.serialize()).done(function (data) {
                form.parent().next().append(
                    "<div class='comment_div'>" +
                    "<div class='comment-wrapper'>" +
                    "<a class='edit-comment'"+"href='"+data.update_url+"'>редактировать комментарий</a>"+
                    "<p class='comment-text'>" + data.body + "</p>" + "Комментарий оставлен" +
                    "<span class='comment-author'>" + data.author + "</span>" +
                    "<span class='comment-date'"+"data-url='"+data.create_url+"'"+">" + data.date + "</span>" +
                    "<a class='reply'>комментировать</a>"+
                    "</div>" + "<div class='all-comments special'>" + "</div>" +
                    "</div>"
                ).addClass('special');
                $('.void-class').remove();
                form.remove();/*Удаляю форму*/
            });
        });
    }

    /*Скрипт для получения формы комментария для редактирования*/
    $(document).on('click', '.edit-comment', function(e) {
        e.preventDefault();
        var edited_obj = $(this).parent(),
            val_for_edit = edited_obj.find('p').first().text(),/*Получаю начальное значение редактируемого сообщения для вставки в форму*/
            action = $(this).attr('href'),
            clone = $('.comment_form').clone().attr('action', action).css('display', 'block');/*Клонирую форму добавления комментария*/

        $(this).after(clone);
        clone.addClass('add_comment_form').removeClass('comment_form');
        $('.add_comment_form p input').val(val_for_edit);
        clone.attr('onclick', editcomment()); /*Привязываю к измененному(новому) объекту событие*/
    });

    /*Функция для редактирования комментария*/
    function editcomment() {
        $('.add_comment_form').on('submit', function (e) {
            e.preventDefault();
            var form = $(this);
            $.post(form.attr('action'), form.serialize()).done(function (data) {
                form.parent().replaceWith( /*Заменяю редактриуемые данные на новые*/
                    "<div class='comment-wrapper'>" +
                    "<a class='edit-comment'"+"href='"+data.update_url+"'>редактировать комментарий</a>"+
                    "<p class='comment-text'>" + data.body + "</p>" + "Комментарий отредактирован" +
                    "<span class='comment-author'>" + data.author + "</span>" +
                    "<span class='comment-date'"+"data-url='"+data.create_url+"'"+">" + data.date + "</span>" +
                    "<a class='reply'>комментировать</a>"+
                    "</div>"
                ).addClass('special');
                $('.void-class').remove();
                form.remove();/*Удаляю форму*/
            });
        });
    }
});