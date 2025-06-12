document.addEventListener('DOMContentLoaded', function () {
    const judgeList = document.getElementById('judge-list');
    const addJudgeBtn = document.getElementById('addJudgeBtn');

    if (!judgeList) return;

    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    // функция для AJAX
    async function sendRequest(url, method, body = null) {
        try {
            const response = await fetch(url, {
                method,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    ...(body ? {'Content-Type': 'application/json'} : {})
                },
                body: body ? JSON.stringify(body) : null
            });
            return await response.json();
        } catch (error) {
            console.error('Ошибка AJAX:', error);
            alert('Ошибка соединения');
        }
    }

    function updateJudgeList(data) {
        if (data?.success && data.judges_html) {
            judgeList.innerHTML = data.judges_html;
        } else {
            alert(data?.error || 'Ошибка обновления списка судей.');
        }
    }

    // активация/удаление судьи
    judgeList.addEventListener('click', async function (event) {
        event.preventDefault();
        const target = event.target;
        const judgeId = target.dataset.id;
        const uuidRoom = judgeList.dataset.uuid;

        if (!judgeId || !uuidRoom) return;

        if (target.classList.contains('activeJudge')) {
            const data = await sendRequest(`/active_judge/${uuidRoom}/${judgeId}/`, 'POST');
            updateJudgeList(data);
        } else if (target.classList.contains('deleteJudge')) {
            if (confirm("Вы уверены, что хотите удалить этого судью?")) {
                const data = await sendRequest(`/delete_judge/${uuidRoom}/${judgeId}/`, 'POST');
                updateJudgeList(data);
            }
        }
    });

    // модальное окно (один раз создаётся, не дублируется)
    function initJudgeModal() {
        if (document.getElementById('addJudgeContainer')) return;

        const modalHtml = `
            <div id="addJudgeContainer" class="modal-overlay">
                <div class="modal-content">
                    <span id="closeAddJudge" class="close">&times;</span>
                    <form id="addJudgeForm">
                        <label for="judgeUsername">Имя пользователя:</label>
                        <input type="text" id="judgeUsername" required>
                        <button type="submit">Добавить</button>
                        <button type="button" id="cancelAddJudge">Отмена</button>
                    </form>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        const modal = document.getElementById('addJudgeContainer');
        const form = document.getElementById('addJudgeForm');
        const usernameInput = document.getElementById('judgeUsername');

        function closeModal() {
            modal.style.display = 'none';
            form.reset();
        }

        modal.addEventListener('click', event => {
            if (event.target === modal || event.target.id === 'closeAddJudge' || event.target.id === 'cancelAddJudge') {
                closeModal();
            }
        });

        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const username = usernameInput.value.trim();
            const uuidRoom = judgeList.dataset.uuid;

            if (!username) return alert('Введите имя пользователя.');

            const data = await sendRequest(`/add_judge/${uuidRoom}/`, 'POST', {username});
            updateJudgeList(data);
            closeModal();
        });
    }

    if (addJudgeBtn) {
        addJudgeBtn.addEventListener('click', function () {
            initJudgeModal();
            document.getElementById('addJudgeContainer').style.display = 'flex';
        });
    }
});
