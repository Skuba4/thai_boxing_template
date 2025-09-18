document.addEventListener('DOMContentLoaded', function () {
    const fightList = document.getElementById('fight-list');
    const addFightBtn = document.getElementById('addFightBtn');
    let currentUuidFight = null;

    if (!fightList) return;
    const uuidRoom = fightList.dataset.uuid || null;

    function createModal() {
        const modalHtml = `
            <div id="universalModal" class="modal-overlay" style="display:none;">
                <div class="modal-content">
                    <span class="close" data-close="true">&times;</span>
                    <div id="modalBody"></div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }

    createModal();

    const universalModal = document.getElementById('universalModal');
    const modalBody = document.getElementById('modalBody');

    function openModal(content) {
        modalBody.innerHTML = content;
        universalModal.style.display = 'flex';
    }

    function closeModal() {
        universalModal.style.display = 'none';
    }

    function sendAjax(url, formData, callback) {
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fightList.innerHTML = data.fights_html;
                    callback();
                } else {
                    alert(data.error || 'Ошибка при установке победителя.');
                }
            })
            .catch(error => console.error('Ошибка AJAX:', error));
    }

    if (addFightBtn) {
        addFightBtn.addEventListener('click', function () {
            openModal(`
                <form id="fightForm">
                    <label>Номер боя:</label>
                    <input type="number" name="number_fight" required>
                    <label>Боец 1:</label>
                    <input type="text" name="fighter_1" required>
                    <label>Боец 2:</label>
                    <input type="text" name="fighter_2" required>
                    <button type="submit">Добавить</button>
                    <button type="button" data-close="true">Отмена</button>
                </form>
            `);

            document.getElementById('fightForm').addEventListener('submit', function (e) {
                e.preventDefault();
                sendAjax(`/create_fight/${uuidRoom}/`, new FormData(this), closeModal);
            });
        });
    }

    fightList.addEventListener('click', function (event) {
        if (event.target.classList.contains('editFight')) {
            event.preventDefault();
            const fightDiv = event.target.closest('.fight');
            if (!fightDiv) return;

            openModal(`
                <form id="editFightForm">
                    <label>Номер боя:</label>
                    <input type="number" name="number_fight" value="${fightDiv.querySelector('.fight-number').textContent.trim()}" required>
                    <label>Боец 1:</label>
                    <input type="text" name="fighter_1" value="${fightDiv.querySelector('.fighter-1').textContent.trim()}" required>
                    <label>Боец 2:</label>
                    <input type="text" name="fighter_2" value="${fightDiv.querySelector('.fighter-2').textContent.trim()}" required>
                    <button type="submit">Сохранить</button>
                    <button type="button" data-close="true">Отмена</button>
                </form>
            `);

            document.getElementById('editFightForm').addEventListener('submit', function (e) {
                e.preventDefault();
                sendAjax(`/edit/${event.target.dataset.id}/`, new FormData(this), closeModal);
            });
        } else if (event.target.classList.contains('deleteFight')) {
            event.preventDefault();
            const uuidFight = event.target.dataset.id;
            if (confirm("Ты точно хочешь удалить этот бой?")) {
                sendAjax(`/delete_fight/${uuidFight}/`, new FormData(), () => {
                });
            }
        } else if (event.target.classList.contains('finalDecision')) {
            event.preventDefault();
            currentUuidFight = event.target.dataset.id;

            if (!currentUuidFight) {
                console.error("Ошибка: UUID боя не найден.");
                alert("Ошибка: не найден ID боя. Попробуй перезагрузить страницу.");
                return;
            }

            openModal(`
                <form id="resultFightForm">
                    <select id="winnerSelect" name="winner" required>
                        <option value="" disabled selected>Выбери победителя</option>
                        <option value="fighter_1">Боец 1</option>
                        <option value="fighter_2">Боец 2</option>
                    </select>
                    <button type="submit">Сохранить</button>
                    <button type="button" data-close="true">Отмена</button>
                </form>
            `);

            document.getElementById('resultFightForm').addEventListener('submit', function (e) {
                e.preventDefault();

                const winner = document.getElementById('winnerSelect').value;
                if (!winner) {
                    alert("Выбери победителя!");
                    return;
                }

                fetch(`/set_winner/${currentUuidFight}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({winner: winner})
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            fightList.innerHTML = data.fights_html;
                            closeModal();
                        } else {
                            alert(data.error || 'Ошибка при установке победителя.');
                        }
                    })
                    .catch(error => {
                        console.error('Ошибка AJAX:', error);
                        alert('Ошибка соединения');
                    });
            });
        }
    });

    universalModal.addEventListener('click', function (event) {
        if (event.target === universalModal || event.target.dataset.close) {
            closeModal();
        }
    });
});
