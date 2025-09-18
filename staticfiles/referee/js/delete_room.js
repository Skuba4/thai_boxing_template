document.addEventListener('DOMContentLoaded', () => {
    const roomList = document.querySelector('.room-list');

    roomList.addEventListener('click', (e) => {
        if (e.target.classList.contains('deleteRoom')) {
            e.preventDefault();

            const uuid = e.target.dataset.uuid;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/delete_room/${uuid}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        roomList.innerHTML = data.rooms_html;
                    } else {
                        alert('Ошибка при удалении комнаты.');
                    }
                })
                .catch(() => alert('Серверная ошибка.'));
        }
    });
});
