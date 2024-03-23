let liked = false;

$(document).ready(function() {
    $('#like-btn').on('click', function() {
        const postId = $(this).data('post-id'); // Здесь ID поста

        const action = liked ? 'unlike' : 'like';
        const url = action === 'like' ? `/api/like/${postId}` : `/api/unlike/${postId}`;
        const method = action === 'like' ? 'POST' : 'DELETE'; // Определяем метод запроса

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
