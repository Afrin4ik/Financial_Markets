const chartNode = document.getElementById("chart");
const statusNode = document.getElementById("status");
const titleNode = document.getElementById("chart-title");
const detailsNode = document.getElementById("chart-details");
const backBtn = document.getElementById("back-btn");


function setStatus(message, type = "") {
    statusNode.textContent = message;
    statusNode.className = `status ${type}`.trim();
}


function parseQuery() {
    const params = new URLSearchParams(window.location.search);
    return {
        ticker: params.get("ticker") || "",
        timeframe: params.get("timeframe") || "",
        days_count: params.get("days_count") || "",
    };
}


function buildCloudTrace(name, x, y1, y2, color) {
    return [
        {
            type: "scatter",
            mode: "lines",
            x,
            y: y1,
            line: { width: 0 },
            hoverinfo: "skip",
            showlegend: false,
            name: `${name}-start`,
        },
        {
            type: "scatter",
            mode: "lines",
            x,
            y: y2,
            line: { width: 0 },
            fill: "tonexty",
            fillcolor: color,
            hoverinfo: "skip",
            showlegend: false,
            name,
        },
    ];
}


function renderChart(payload) {
    const x = payload.candles.map((candle) => candle.time);
    const open = payload.candles.map((candle) => candle.open);
    const high = payload.candles.map((candle) => candle.high);
    const low = payload.candles.map((candle) => candle.low);
    const close = payload.candles.map((candle) => candle.close);

    const traces = [
        {
            type: "candlestick",
            x,
            open,
            high,
            low,
            close,
            name: "Свечи",
            increasing: { line: { color: "#0f8b71" } },
            decreasing: { line: { color: "#d1495b" } },
        },
        {
            type: "scatter",
            mode: "lines",
            x,
            y: payload.ichimoku.tenkan,
            name: "Tenkan",
            line: { color: "#0088cc", width: 1.5 },
        },
        {
            type: "scatter",
            mode: "lines",
            x,
            y: payload.ichimoku.kijun,
            name: "Kijun",
            line: { color: "#ea8f00", width: 1.5 },
        },
        {
            type: "scatter",
            mode: "lines",
            x,
            y: payload.ichimoku.chikou,
            name: "Chikou",
            line: { color: "#5b2a86", width: 1.2 },
        },
        {
            type: "scatter",
            mode: "lines",
            x,
            y: payload.ichimoku.senkou_a,
            name: "Senkou A",
            line: { color: "#1f9d55", width: 1.2 },
        },
        {
            type: "scatter",
            mode: "lines",
            x,
            y: payload.ichimoku.senkou_b,
            name: "Senkou B",
            line: { color: "#b01e44", width: 1.2 },
        },
    ];

    payload.cloud.forEach((band, idx) => {
        const [startTrace, fillTrace] = buildCloudTrace(
            `Cloud-${idx}`,
            x,
            band.y1,
            band.y2,
            band.color,
        );
        traces.push(startTrace, fillTrace);
    });

    Plotly.newPlot(
        chartNode,
        traces,
        {
            margin: { l: 50, r: 16, t: 10, b: 40 },
            dragmode: "zoom",
            xaxis: {
                rangeslider: { visible: false },
                showgrid: true,
                gridcolor: "rgba(66, 87, 128, 0.1)",
            },
            yaxis: {
                fixedrange: false,
                showgrid: true,
                gridcolor: "rgba(66, 87, 128, 0.1)",
            },
            legend: {
                orientation: "h",
                y: -0.2,
            },
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "#ffffff",
        },
        {
            responsive: true,
            displaylogo: false,
            modeBarButtonsToRemove: ["select2d", "lasso2d"],
        },
    );
}


async function init() {
    const params = parseQuery();
    if (!params.ticker || !params.timeframe || !params.days_count) {
        setStatus("Не переданы параметры графика. Вернитесь назад и выберите их.", "error");
        return;
    }

    titleNode.textContent = `${params.ticker.toUpperCase()} · ${params.timeframe}`;
    detailsNode.textContent = `Период: ${params.days_count} дней`;
    setStatus("Загрузка свечей и индикаторов...", "");

    try {
        const response = await fetch(`/market-data/chart?${new URLSearchParams(params).toString()}`);
        const payload = await response.json();
        if (!response.ok) {
            throw new Error(payload.detail?.message || payload.detail || "Ошибка запроса");
        }

        renderChart(payload);
        setStatus("Данные получены", "ok");
    } catch (error) {
        setStatus(`Ошибка: ${error.message}`, "error");
    }
}


backBtn.addEventListener("click", () => {
    window.location.assign("/");
});


init();