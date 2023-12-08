$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;

            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

$(document).on('click','.js-toggle-modal', function(e){
    e.preventDefault();
    // console.log("hello i was clicked");
    $('.js-modal').toggleClass('hidden');
})
.on('click','.js-submit', function(e){
    e.preventDefault();
    // console.log('submit');
    const text = $('.js-post-text').val().trim();
    const $btn = $(this); //js submit button

    if(!text.length){
        return false;
    }

    $btn.prop('disabled', true).text('Posting!');
    $.ajax({
        type: 'POST',
        url : $('.js-post-text').data('post-url'),
        data: {
            text: text,
        },
        success: (dataHtml) => {
            $('.js-modal').addClass('hidden');
            $('#posts-container').prepend(dataHtml);
            $btn.prop('disabled',false).text('New Post');
            $('.js-post-text').val('');
        },
        error: (error) => {
            console.warn(error);
            $btn.prop('disabled',false).text('Error');
        }
    });
})
.on('click','.js-follow', function(e){
    e.preventDefault();
    const action = $(this).attr('data-action');
    $.ajax({
        type: 'POST',
        url : $(this).data('url'),
        data: {
            action : action,
            username : $(this).data('username'),
        },
        success: (data) => {
            $('.js-follow-text').text(data.wording);
            if(action == 'follow'){
                $(this).attr('data-action','unfollow');
            }
            else{
                $(this).attr('data-action','follow');
            }
            $('.js-followers-count').text(data.total_followers);
            $('.js-following-count').text(data.total_following);
            
        },
        error: (error) => {
            console.warn(error);
        }
    });
})
