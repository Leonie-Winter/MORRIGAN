// Settings
const chartLabels = [
  "Temperature (°C)",
  "pH",
  "TDS (ppm)",
  "DO (mg/L)",
  "Turbidity (NTU)",
];
const chartXLabel = "Milliseconds";
const chartYLables = [
  "Celsius",
  "pondus Hydrogenii",
  "Parts per million",
  "Milligrams per liter",
  "Nephelometric Turbidity Unit",
];
const chartColors = [
  "rgba(255, 99, 132, 1)", // Temp
  "rgba(54, 162, 235, 1)", // pH
  "rgba(255, 206, 86, 1)", // TDS
  "rgba(75, 192, 192, 1)", // DO
  "rgba(153, 102, 255, 1)", // Turbidity
];
const chartXDisplayMaxAmount = 60; // * 1/60 sec = 1 sec
const pullRate = (10 / 60) * 1000; // in ms
const enableAnimations = true; // disable if too laggy
const dataFileLocation = "data.json";

// Vars
const chartIds = ["chartTemp", "chartPH", "chartTDS", "chartDO", "chartTurb"];
let charts = {}; // To store chart instances
let viewAllPoints = false;

function fetchData() {
  fetch(dataFileLocation)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch data.json");
      }
      return response.json();
    })
    .then((fetchedData) => {
      updateCharts(fetchedData); // Update all charts with new data
    })
    .catch((error) => console.error("Error fetching data:", error));
}

function createChart(ctx, label, color, yLabel) {
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [], // X-axis labels (e.g., timestamps)
      datasets: [
        {
          label: label,
          data: [], // Y-axis values
          borderColor: color,
          backgroundColor: color.replace("1)", "0.2)"),
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: label,
        },
      },
      scales: {
        y: {
          title: {
            display: true,
            text: yLabel,
          },
        },
        x: {
          min: 0,
          max: chartXDisplayMaxAmount,
          title: {
            display: true,
            text: chartXLabel,
          },
        },
      },
      maintainAspectRatio: false,
      animation: enableAnimations,
    },
  });
}

function updateCharts(data) {
  // Map sensor types to their respective chart IDs
  const sensorMapping = {
    temperature: "chartTemp",
    PH: "chartPH",
    TDS: "chartTDS",
    DO: "chartDO",
    turbidity: "chartTurb",
  };

  // Iterate over each sensor type in the mapping
  Object.entries(sensorMapping).forEach(([key, chartId], index) => {
    const sensorData = data.filter((item) => key in item); // Filter data for the specific sensor
    const ctx = document.getElementById(chartId).getContext("2d");

    if (!charts[chartId]) {
      // Create the chart if it doesn't exist
      charts[chartId] = createChart(
        ctx,
        chartLabels[index],
        chartColors[index],
        chartYLables[index]
      );
    }

    const chart = charts[chartId];
    let sensorDataX = sensorData.map((row) => row.milliseconds);
    let sensorDataY = sensorData.map((row) => row[key]);

    // Shift min max if needed
    if (viewAllPoints) {
      chart.options.scales.x.min = undefined;
      chart.options.scales.x.max = undefined;
    } else {
      let xAmount = sensorDataX.length;
      if (xAmount >= chartXDisplayMaxAmount) {
        chart.options.scales.x.max = xAmount;
        chart.options.scales.x.min = xAmount - chartXDisplayMaxAmount;
      }
    }

    // Update chart data
    chart.data.labels = sensorDataX; // Update X-axis labels
    chart.data.datasets[0].data = sensorDataY; // Update Y-axis values

    chart.update(); // Re-render the chart
  });
}

// Poll for updates in ms
setInterval(fetchData, pullRate);

// Initial data fetch
fetchData();

document
  .getElementById("viewAllPoints")
  .addEventListener("click", onClick_viewAllPoints);
document
  .getElementById("viewSection")
  .addEventListener("click", onClick_viewSection);

function onClick_viewAllPoints() {
  viewAllPoints = true;
  console.log("viewAllPoints");
  fetchData();
}

function onClick_viewSection() {
  viewAllPoints = false;
  console.log("viewSection");
  fetchData();
}