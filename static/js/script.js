let liked = $('#like-btn').data('liked'); // Получаем состояние liked из data-атрибута
console.log(liked);

$(document).ready(function() {
    $('#like-btn').on('click', function() {
        const postId = $(this).data('post-id'); // Здесь ID поста

        const action = liked ? 'like' : 'unlike';
        const url = action === 'like' ? `/api/v2/like/${postId}` : `/api/v2/like/${postId}`;
        const method = action === 'like' ? 'DELETE' : 'POST'; // Определяем метод запроса

        $.ajax({
            type: method,
            contentType: 'application/json',
            url: url,
            success: function(data) {
                $('#likes').text(data.likes);
                if (liked) {
                    $('#like-btn').removeClass('btn-success').addClass('btn-secondary');
                } else {
                    $('#like-btn').removeClass('btn-secondary').addClass('btn-success');
                }
                liked = !liked;
            }
        });
    });
});