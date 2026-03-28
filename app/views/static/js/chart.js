const form = document.getElementById("market-form");
const tickerSelect = document.getElementById("ticker");
const timeframeSelect = document.getElementById("timeframe");
const daysInput = document.getElementById("days-count");
const statusNode = document.getElementById("status");
const previewNode = document.getElementById("request-preview");
const submitBtn = document.getElementById("submit-btn");


function setStatus(message, type = "") {
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
    setStatus("Загрузка доступных активов и таймфреймов...");
    try {
        const [assetsResp, timeframesResp] = await Promise.all([
            fetch("/market/assets"),
            fetch("/market/timeframes"),
        ]);

        if (!assetsResp.ok || !timeframesResp.ok) {
            throw new Error("Не удалось получить справочные данные");
        }

        const assetsData = await assetsResp.json();
        const timeframesData = await timeframesResp.json();

        fillSelect(tickerSelect, assetsData.supported_assets || [], "Нет доступных активов");
        fillSelect(timeframeSelect, timeframesData.supported_timeframes || [], "Нет доступных таймфреймов");

        setStatus("Параметры загружены. Можно отправлять запрос.", "ok");
    } catch (error) {
        setStatus(`Ошибка: ${error.message}`, "error");
    }
}


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const ticker = tickerSelect.value;
    const timeframe = timeframeSelect.value;
    const daysCount = Number(daysInput.value);

    if (!ticker || !timeframe || !daysCount) {
        setStatus("Заполни все поля формы", "error");
        return;
    }

    submitBtn.disabled = true;
    setStatus("Отправление запроса за данными...", "");

    const query = new URLSearchParams({
        ticker,
        timeframe,
        days_count: String(daysCount),
    });

    try {
        const response = await fetch(`/market/chart?${query.toString()}`);
        const payload = await response.json();

        if (!response.ok) {
            throw new Error(payload.detail?.message || payload.detail || "Ошибка запроса");
        }

        previewNode.hidden = false;
        previewNode.textContent = JSON.stringify({
                ticker: payload.ticker,
                timeframe: payload.timeframe,
                days_count: payload.days_count,
                candles_count: payload.candles?.length || 0,
            },
            null,
            2,
        );
        setStatus("Данные получены", "ok");
    } catch (error) {
        previewNode.hidden = true;
        setStatus(`Ошибка: ${error.message}`, "error");
    } finally {
        submitBtn.disabled = false;
    }
});


loadReferenceData();