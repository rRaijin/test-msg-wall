$(document).ready(function () {

    $('.message_form').on('submit', function (e) {
        e.preventDefault();
        var form = $(this);
        console.log(form);
        $.post(form.attr('action'), form.serialize()).done(function (data) {
            console.log(data);
            $('.message-container').prepend(
                "<div class='message-wrapper'>" +
                    "<div>" +
                        "<a class='redit'"+"href='"+data.update_url+"'>"+"edit"+"</a>"+
                        "<p class='msg-body'>" + data.body + "</p>" +
                        "<span class='message-author'>" + data.author + "</span>" +
                        "<span class='message-date'"+"data-url='"+data.create_url+"'"+">" + data.date + "</span>" +
                        "<a class='comment'>comment</a>" +
                    "</div>" +
                    "<div class='all-comments'>" +
                    "</div>" +
                "</div>"
            );
        });
        form.find("textarea").val('');
    });

    $(document).on('click', '.redit', function(e) {
        e.preventDefault();

        var edited_obj = $(this).parent();

        console.log(edited_obj);
        var val_for_edit = edited_obj.find('p').first().text();
        console.log(val_for_edit);
        console.log(this);
        var action = $(this).attr('href'),
            clone = $('.message_form').clone().attr('action', action).css('display', 'block');
        console.log(action);

        $(this).after(clone);
        clone.addClass('add_comment_form').removeClass('message_form');
        $('.add_comment_form p textarea').val(val_for_edit);
        clone.attr('onclick', editcomment());
    });

    $(document).on('click','.comment, .reply', function(e) {
        var $action = $(this).prev(),
            action = $action.attr('data-url'),
            clone = $('.comment_form').clone().attr('action', action).css('display', 'block');
        console.log(action);

        $(this).after(clone);

        clone.addClass('add_comment_form').removeClass('comment_form');
        clone.attr('onclick', comment());
    });

    $(document).on('click', '.edit', function(e) {
        e.preventDefault();

        var edited_obj = $(this).parent();

        console.log(edited_obj);
        var val_for_edit = edited_obj.find('p').first().text();
        console.log(val_for_edit);
        var action = $(this).attr('href'),
            clone = $('.comment_form').clone().attr('action', action).css('display', 'block');

        $(this).after(clone);
        clone.addClass('add_comment_form').removeClass('comment_form');
        $('.add_comment_form p input').val(val_for_edit);
        clone.attr('onclick', editcomment());
    });

    function editcomment() {
        $('.add_comment_form').on('submit', function (e) {
            e.preventDefault();
            var form = $(this);
            $.post(form.attr('action'), form.serialize()).done(function (data) {
                form.parent().replaceWith(
                    "<div class='comment_wrapper'>" +
                    "<a class='edit'"+"href='"+data.update_url+"'>"+"edit"+"</a>"+
                    "<p class='comment-text'>" + data.body + "</p>" +
                    "<span class='comment-author'>" + data.author + "</span>" +
                    "<span class='comment-date'"+"data-url='"+data.create_url+"'"+">" + data.date + "</span>" +
                    "<a class='reply'>reply</a>"+
                    "</div>"
                );
                $('.void-class').remove();
                form.remove();
            });
        });
    }

    function comment() {
        $('.add_comment_form').on('submit', function (e) {
            e.preventDefault();
            var form = $(this);
            $.post(form.attr('action'), form.serialize()).done(function (data) {
                form.parent().next().append(
                    "<div class='comment_div'>" +
                    "<div class='comment_wrapper'>" +
                    "<a class='edit'"+"href='"+data.update_url+"'>"+"edit"+"</a>"+
                    "<p class='comment-text'>" + data.body + "</p>" +
                    "<span class='comment-author'>" + data.author + "</span>" +
                    "<span class='comment-date'"+"data-url='"+data.create_url+"'"+">" + data.date + "</span>" +
                    "<a class='reply'>reply</a>"+
                    "</div>" + "<div class='all-comments'>" + "</div>" +
                    "</div>"
                );
                $('.void-class').remove();
                form.remove();
            });
        });
    }
});