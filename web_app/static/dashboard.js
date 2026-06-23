Chart.register(ChartDataLabels);

// =========================
// START / STOP SYSTEM
// =========================
async function startSystem() {
    await fetch("/start", { method: "POST" });
}

async function stopSystem() {
    await fetch("/stop", { method: "POST" });
}

// =========================
// EQUITY CURVE INIT
// =========================
const ctx = document.getElementById("equityChart").getContext("2d");

const equityChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Equity Curve",
            data: [],
            borderColor: "#00ffcc",
            backgroundColor: "rgba(0,255,204,0.1)",
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: { display: false },
            y: {
                ticks: { color: "#ffffff" }
            }
        },
        plugins: {
            datalabels: {
                display: false
            },
            legend: {
                 display: false
            }
        }
    }
});


// =========================
// PIE CHART (WIN / LOSS)
// =========================
const pieCanvas = document.getElementById("winLossChart");

if (!pieCanvas) {
    console.error("winLossChart canvas not found");
}

const winLossChart = new Chart(pieCanvas.getContext("2d"), {
    type: "pie",
    data: {
        labels: ["Wins", "Losses"],
        datasets: [{
            data: [1, 1],
            backgroundColor: ["#00ff66", "#ff4444"],
            borderColor: "#222",
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                labels: {
                    color: "#ffffff"
                }
            },

            // =========================
            // % LABELS ON PIE CHART
            // =========================
            datalabels: {
                color: "#ffffff",
                font: {
                    weight: "bold"
                },
                formatter: (value, context) => {

                    const data = context.chart.data.datasets[0].data;
                    const total = data.reduce((a, b) => a + b, 0);

                    if (total === 0) return "0%";

                    const percent = (value / total) * 100;

                    return percent.toFixed(0) + "%";
                }
            }
        }
    }
});


// =========================
// WEBSOCKET
// =========================
const ws = new WebSocket("ws://127.0.0.1:9000/ws");

ws.onmessage = function (event) {

    const data = JSON.parse(event.data);

    // =========================
    // STATUS
    // =========================
    document.getElementById("status").innerText =
        `STATUS: ${data.status}`;

    const statusEl = document.getElementById("status");

    statusEl.className = data.status === "RUNNING"
        ? "badge bg-success fs-6 px-3 py-2"
        : "badge bg-secondary fs-6 px-3 py-2";

    // =========================
    // RUNTIME
    // =========================
    const runtime = Math.floor(data.runtime_seconds);

    const hours = Math.floor(runtime / 3600);
    const minutes = Math.floor((runtime % 3600) / 60);
    const seconds = runtime % 60;

    document.getElementById("runtime").innerText =
        `${hours} : ${minutes} : ${seconds}`;

    // =========================
    // MARKET DATA
    // =========================
    document.getElementById("price").innerText =
        Number(data.price).toFixed(2);

    document.getElementById("cash").innerText =
        Number(data.cash).toFixed(2);

    document.getElementById("btc").innerText =
        Number(data.btc_holdings).toFixed(6);

    document.getElementById("trades").innerText =
        data.trades_count;

    // =========================
    // METRICS
    // =========================
    document.getElementById("candle_count").innerText =
        data.candle_count ?? 0;

    document.getElementById("portfolio_value").innerText =
        Number(data.portfolio_value ?? 0).toFixed(2);

    document.getElementById("wins").innerText =
        data.wins ?? 0;

    document.getElementById("losses").innerText =
        data.losses ?? 0;

    document.getElementById("sharpe_ratio").innerText =
        (data.sharpe_ratio ?? 0).toFixed?.(3) ?? 0;

    document.getElementById("max_dd").innerText =
        Number(data.max_dd ?? 0).toFixed(6);

    document.getElementById("profits").innerText =
        Number(data.profits ?? 0).toFixed(2);

    // DEBUGS
    const momentumEl = document.getElementById("dbg_momentum");

    momentumEl.innerText = data.momentum ?? "--";

    if (data.momentum === "BULLISH") {
        momentumEl.style.color = "#00ff66";
    }
    else if (data.momentum === "BEARISH") {
        momentumEl.style.color = "#ff4444";
    }
    else {
        momentumEl.style.color = "#ffffff";
    } 

    // SMA_PCA
    const smaEl = document.getElementById("dbg_sma");

    smaEl.innerText = data.sma_pct ?? "NEUTRAL";

    if (data.sma_pct === "BULLISH") {
        smaEl.style.color = "lime";
    }
    else if (data.sma_pct === "BEARISH") {
        smaEl.style.color = "red";
    }
    else {
        smaEl.style.color = "white";
    }

    // =========================
    // TRANSACTION TABLE
    // =========================
    const table = document.getElementById("tx_table");

    if (table) {
        table.innerHTML = "";

        (data.trades || []).slice().reverse().forEach(t => {

            const pnl = Number(t.pnl || 0);

            const row = `
                <tr>
                    <td style="color:${t.type === "BUY" ? "#00ff66" : "#ff4444"}">
                        ${t.type}
                    </td>

                    <td>${Number(t.price || 0).toFixed(2)}</td>

                    <td>${Number(t.qty || 0).toFixed(6)}</td>

                    <td style="color:${pnl === 0 ? "#aaaaaa" : (pnl > 0 ? "#00ff66" : "#ff4444")}; font-weight:bold;">
                        ${pnl === 0 ? "-" : pnl.toFixed(2)}
                    </td>

                    <td>${t.index ?? "-"}</td>
                </tr>
            `;

            table.innerHTML += row;
        });
    }

    // =========================
    // EQUITY CURVE UPDATE
    // =========================
    const curve = data.equity_curve;

    if (curve && curve.length > 0) {

        if (curve.length < equityChart.data.datasets[0].data.length) {
            equityChart.data.labels = [];
            equityChart.data.datasets[0].data = [];
        }

        const lastIndex = equityChart.data.datasets[0].data.length;

        if (curve.length > lastIndex) {

            for (let i = lastIndex; i < curve.length; i++) {
                equityChart.data.labels.push(i);
                equityChart.data.datasets[0].data.push(curve[i]);
            }

            equityChart.update();
        }
    }

    // =========================
    // PIE CHART UPDATE
    // =========================
    const wins = data.wins ?? 0;
    const losses = data.losses ?? 0;

    const total = wins + losses;

    if (total > 0) {
        winLossChart.data.datasets[0].data = [wins, losses];
    } else {
        winLossChart.data.datasets[0].data = [1, 1];
    }

    winLossChart.update();
};