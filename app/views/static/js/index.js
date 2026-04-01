const form = document.getElementById("market-form");
const tickerSelect = document.getElementById("ticker");
const timeframeSelect = document.getElementById("timeframe");
const daysInput = document.getElementById("days-count");
const statusNode = document.getElementById("status");
const submitBtn = document.getElementById("submit-btn");


function setStatus(message, type = "") {
    if (!statusNode) {
        return;
    }
    statusNode.textContent = message;
    statusNode.className = `status ${type}`.trim();
}


function fillSelect(selectNode, values, placeholderText) {
    selectNode.innerHTML = "";

    if (!values || values.length === 0) {
        const option = document.createElement("option");
        option.textContent = placeholderText;
        option.disabled = true;
        option.selected = true;
        selectNode.appendChild(option);
        return;
    }

    values.forEach((value, idx) => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        if (idx === 0) {
            option.selected = true;
        }
        selectNode.appendChild(option);
    });
}


async function loadReferenceData() {
    if (!tickerSelect || !timeframeSelect) {
        setStatus("Ошибка инициализации формы", "error");
        return;
    }

    setStatus("Загрузка доступных активов и таймфреймов...", "");

    try {
        const [assetsResp, timeframesResp] = await Promise.all([
            fetch("/market-data/assets"),
            fetch("/market-data/timeframes"),
        ]);

        if (!assetsResp.ok || !timeframesResp.ok) {
            throw new Error("Не удалось получить данные об активах или таймфреймах");
        }

        const assetsData = await assetsResp.json().catch(() => ({}));
        const timeframesData = await timeframesResp.json().catch(() => ({}));

        fillSelect(tickerSelect, assetsData.supported_assets || [], "Нет доступных активов");
        fillSelect(timeframeSelect, timeframesData.supported_timeframes || [], "Нет доступных таймфреймов");

        setStatus("Параметры загружены. Можно строить график.", "ok");
    } catch (error) {
        setStatus(`Ошибка: ${error?.message || "Неизвестная ошибка"}`, "error");
    }
}


if (!form || !submitBtn || !daysInput) {
    setStatus("Форма недоступна на странице", "error");
} else {
    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (!tickerSelect || !timeframeSelect) {
            setStatus("Ошибка: поля формы не найдены", "error");
            return;
        }

        const ticker = tickerSelect.value;
        const timeframe = timeframeSelect.value;
        const daysCount = Number(daysInput.value);

        if (!ticker || !timeframe || !daysCount) {
            setStatus("Заполните все поля формы", "error");
            return;
        }

        if (!Number.isInteger(daysCount) || daysCount < 1 || daysCount > 3650) {
            setStatus("Количество дней должно быть целым числом от 1 до 3650", "error");
            return;
        }

        submitBtn.disabled = true;

        const query = new URLSearchParams({
            ticker,
            timeframe,
            days_count: String(daysCount),
        });

        try {
            window.location.assign(`/chart?${query.toString()}`);
        } catch (error) {
            submitBtn.disabled = false;
            setStatus(`Ошибка перехода: ${error?.message || "Неизвестная ошибка"}`, "error");
        }
    });
}


loadReferenceData();
