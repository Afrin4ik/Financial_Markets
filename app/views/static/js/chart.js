const chartNode = document.getElementById("chart");
const statusNode = document.getElementById("status");
const titleNode = document.getElementById("chart-title");
const detailsNode = document.getElementById("chart-details");
const backBtn = document.getElementById("back-btn");

const CHART_LAYOUT = {
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
};

const CHART_CONFIG = {
    responsive: true,
    displaylogo: false,
    modeBarButtonsToRemove: ["select2d", "lasso2d"],
};

const ICHIMOKU_LINES = [
    { key: "tenkan", name: "Tenkan", color: "#0088cc", width: 1.5 },
    { key: "kijun", name: "Kijun", color: "#ea8f00", width: 1.5 },
    { key: "chikou", name: "Chikou", color: "#5b2a86", width: 1.2 },
    { key: "senkou_a", name: "Senkou A", color: "#1f9d55", width: 1.2 },
    { key: "senkou_b", name: "Senkou B", color: "#b01e44", width: 1.2 },
];


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


function buildCloudTraces(x, cloudBands) {
    const traces = new Array(cloudBands.length * 2);

    for (let idx = 0; idx < cloudBands.length; idx += 1) {
        const band = cloudBands[idx];
        const [startTrace, fillTrace] = buildCloudTrace(
            `Cloud-${idx}`,
            x,
            band.y1,
            band.y2,
            band.color,
        );
        const traceOffset = idx * 2;
        traces[traceOffset] = startTrace;
        traces[traceOffset + 1] = fillTrace;
    }

    return traces;
}


function buildIchimokuTraces(x, ichimoku) {
    return ICHIMOKU_LINES.map((line) => ({
        type: "scatter",
        mode: "lines",
        x,
        y: ichimoku[line.key],
        name: line.name,
        line: { color: line.color, width: line.width },
    }));
}


function renderChart(payload) {
    const candlesLength = payload.candles.length;
    const x = new Array(candlesLength);
    const open = new Array(candlesLength);
    const high = new Array(candlesLength);
    const low = new Array(candlesLength);
    const close = new Array(candlesLength);

    for (let idx = 0; idx < candlesLength; idx += 1) {
        const candle = payload.candles[idx];
        x[idx] = candle.time;
        open[idx] = candle.open;
        high[idx] = candle.high;
        low[idx] = candle.low;
        close[idx] = candle.close;
    }

    const cloudTraces = buildCloudTraces(x, payload.cloud || []);
    const ichimokuTraces = buildIchimokuTraces(x, payload.ichimoku);

    const traces = new Array(cloudTraces.length + 1 + ichimokuTraces.length);
    let traceIndex = 0;

    for (let idx = 0; idx < cloudTraces.length; idx += 1) {
        traces[traceIndex] = cloudTraces[idx];
        traceIndex += 1;
    }

    traces[traceIndex] = {
        type: "candlestick",
        x,
        open,
        high,
        low,
        close,
        name: "Свечи",
        increasing: { line: { color: "#0f8b71" } },
        decreasing: { line: { color: "#d1495b" } },
    };
    traceIndex += 1;

    for (let idx = 0; idx < ichimokuTraces.length; idx += 1) {
        traces[traceIndex] = ichimokuTraces[idx];
        traceIndex += 1;
    }

    Plotly.react(
        chartNode,
        traces,
        CHART_LAYOUT,
        CHART_CONFIG,
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