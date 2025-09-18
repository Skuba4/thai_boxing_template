document.addEventListener("DOMContentLoaded", function () {
    // ✅ Создаём универсальное модальное окно
    const modal = document.createElement("div");
    modal.classList.add("judge-note-modal");
    modal.innerHTML = `<div id="modal-body"></div>`;
    const overlay = document.createElement("div");
    overlay.classList.add("modal-overlay");

    document.body.appendChild(modal);
    document.body.appendChild(overlay);

    function openModal(content) {
        document.getElementById("modal-body").innerHTML = content;
        modal.style.display = "flex";
        overlay.style.display = "block";
    }

    function closeModal() {
        modal.style.display = "none";
        overlay.style.display = "none";
    }

    function updateFightList() {
        fetch(window.location.href)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const newFightList = doc.getElementById("fight-list");

                if (newFightList) {
                    document.getElementById("fight-list").innerHTML = newFightList.innerHTML;
                }
            })
            .catch(error => console.error("Ошибка обновления боёв:", error));
    }

    // ✅ Фикс кнопок "Закрыть" и "Отмена"
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("cancel-btn") || event.target.classList.contains("modal-overlay")) {
            closeModal();
        }
    });

    // ✅ Открытие модалки для создания заметки
    document.addEventListener("click", function (event) {
        if (!event.target.classList.contains("viewNotes")) return;
        event.preventDefault();

        const fightUUID = event.target.dataset.id;
        const roundNumber = event.target.dataset.round;
        const fightElement = document.querySelector(`.fight[data-fight-id="${fightUUID}"]`);
        const fightNumber = fightElement ? fightElement.querySelector(".fight-number").textContent : "Неизвестно";
        const redFighter = fightElement.querySelector(".fighter-1").textContent;
        const blueFighter = fightElement.querySelector(".fighter-2").textContent;

        const content = `
            <h2>СУДЕЙСКАЯ ЗАПИСКА</h2>
        
            <div class="judge-info">
                <span>Дата: ${new Date().toISOString().split("T")[0]}</span>
                <span>Бой: ${fightNumber}</span>
                <span>Судья: ${document.querySelector(".user").textContent.trim()}</span>
            </div>
        
            <div class="divider"></div>
        
            <div class="fighter-info">
                <span class="red-fighter">${redFighter}</span>
                <span class="blue-fighter">${blueFighter}</span>
            </div>
        
            <div class="remarks-container">
                <input type="text" id="note-red-remark" placeholder="заметки">
                <span class="round-display">Раунд: ${roundNumber}</span>
                <input type="text" id="note-blue-remark" placeholder="заметки">
            </div>
        
            <div class="winner-selection">
                <select id="note-winner">
                    <option value="" selected disabled>-- Выбери победителя --</option>
                    <option value="red">КРАСНЫЙ</option>
                    <option value="blue">СИНИЙ</option>
                </select>
            </div>
        
            <div class="button-container">
                <button class="save-btn" id="save-note">Сохранить</button>
                <button class="cancel-btn">Отмена</button>
            </div>
        `;

        openModal(content);

        document.getElementById("save-note").addEventListener("click", function () {
            const winner = document.getElementById("note-winner").value;
            if (!winner) {
                alert("Выбери победителя перед сохранением!");
                return;
            }

            const data = {
                fight_id: fightUUID,
                round: roundNumber,
                judge: document.querySelector(".user").textContent.trim(),
                red_fighter: redFighter,
                blue_fighter: blueFighter,
                red_remark: document.getElementById("note-red-remark").value,
                blue_remark: document.getElementById("note-blue-remark").value,
                winner: winner,
            };

            fetch("/create_note/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
                body: JSON.stringify(data),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        closeModal();
                        updateFightList();
                    } else {
                        alert("Ошибка сохранения");
                    }
                });
        });
    });

    document.addEventListener("click", function (event) {
        if (!event.target.classList.contains("viewFightNotes")) return;
        event.preventDefault();

        const fightUUID = event.target.dataset.id;
        const fightElement = document.querySelector(`.fight[data-fight-id="${fightUUID}"]`);
        const fightNumber = fightElement ? fightElement.querySelector(".fight-number").textContent : "Неизвестно";

        const content = `
            <div id="round-links" class="button-container">
                <button class="round-btn" data-round="1">РАУНД №1</button>
                <button class="round-btn" data-round="2">РАУНД №2</button>
                <button class="round-btn" data-round="3">РАУНД №3</button>
            </div>
            <div id="notes-content-wrapper">
                <div id="notes-content"></div>
            </div>
            <div class="button-container">
                <button class="cancel-btn">Закрыть</button>
            </div>
        `;

        openModal(content);

        document.querySelectorAll(".round-btn").forEach(button => {
            button.addEventListener("click", function () {
                const roundNumber = this.dataset.round;

                fetch(`/notes/${fightUUID}/${roundNumber}/`)
                    .then(response => response.json())
                    .then(data => {
                        const notesContent = document.getElementById("notes-content");
                        notesContent.innerHTML = `<h3>РАУНД №${roundNumber}</h3>`;

                        if (data.success) {
                            data.notes.forEach(note => {
                                notesContent.innerHTML += `
                                    <div class="judge-note-display">
                                        <h2>СУДЕЙСКАЯ ЗАПИСКА</h2>

                                        <div class="judge-info">
                                            <span>Дата: ${note.date || new Date().toISOString().split("T")[0]}</span>
                                            <span>Бой: ${note.fight_number || fightNumber}</span>
                                            <span>Судья: ${note.judge}</span>
                                        </div>

                                        <div class="divider"></div>

                                        <div class="fighter-info">
                                            <span class="red-fighter">${note.red_fighter}</span>
                                            <span class="blue-fighter">${note.blue_fighter}</span>
                                        </div>

                                        <div class="remarks-container">
                                            <span class="remark">${note.red_remark || "—"}</span>
                                            <span class="round-display">Раунд: ${roundNumber}</span>
                                            <span class="remark">${note.blue_remark || "—"}</span>
                                        </div>

                                        <div class="winner-selection">
                                            <strong>Победитель:</strong>
                                            <span class="winner ${note.winner === 'red' ? 'red-text' : 'blue-text'}">
                                                ${note.winner === "red" ? "КРАСНЫЙ" : "СИНИЙ"}
                                            </span>
                                        </div>
                                    </div>
                                `;
                            });
                        } else {
                            notesContent.innerHTML += "<p>Нет записок для этого раунда.</p>";
                        }
                    });
            });
        });

        updateFightList();
    });
});
