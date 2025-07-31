const homeBtn = document.getElementById("homeBtn");
const membersBtn = document.getElementById("membersBtn");
const structureBtn = document.getElementById("structureBtn");

const mainContent = document.getElementById("mainContent");
const membersContent = document.getElementById("membersContent");
const structureContent = document.getElementById("structureContent");

homeBtn.addEventListener("click", () => {
  mainContent.classList.remove("hidden");
  membersContent.classList.add("hidden");
  structureContent.classList.add("hidden");
});

membersBtn.addEventListener("click", () => {
  mainContent.classList.add("hidden");
  membersContent.classList.remove("hidden");
  structureContent.classList.add("hidden");
});

structureBtn.addEventListener("click", () => {
  mainContent.classList.add("hidden");
  membersContent.classList.add("hidden");
  structureContent.classList.remove("hidden");
});
function updateLiveCount() {
  fetch("/api/live_count")
    .then((res) => res.json())
    .then((data) => {
      console.log("Received count:", data.count);
      const box = document.getElementById("liveCountBox");
      box.textContent = data.count;
    })
    .catch((err) => console.error("Fetch error:", err));
}

// Refresh every second
setInterval(updateLiveCount,1000);


// Handle Read Data button
document.getElementById("readDataBtn").addEventListener("click", () => {
  fetch("/api/over_threshold_records")
    .then((res) => res.json())
    .then((data) => {
      const tableBody = document.getElementById("tableBody");
      const tableContainer = document.getElementById("recordTable");
      tableBody.innerHTML = "";

      if (data.length > 0) {
        tableContainer.classList.remove("hidden");
        data.forEach((row) => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td class="border px-4 py-2">${row.sensor_value}</td>
            <td class="border px-4 py-2">${new Date(row.timestamp).toLocaleString()}</td>
          `;
          tableBody.appendChild(tr);
        });
      } else {
        tableBody.innerHTML =
          "<tr><td colspan='2' class='px-4 py-2'>No data found.</td></tr>";
        tableContainer.classList.remove("hidden");
      }
    })
    .catch((err) => console.error("Failed to fetch data", err));
});

fetch('/read-data')
  .then(response => response.json())
  .then(data => {
    const records = data.records;
    const overLimit = data.over_limit;

    const tableBody = document.getElementById("data-table-body");
    tableBody.innerHTML = '';

    records.forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="border px-4 py-2">${row.sensor_value}</td>
        <td class="border px-4 py-2">${new Date(row.timestamp).toLocaleString()}</td>
      `;
      tableBody.appendChild(tr);
    });

    // Show or hide alert based on current live value
    const alertBox = document.getElementById("alert-box");
    if (overLimit) {
      alertBox.textContent = "⚠️ Integration over limit occurred";
      alertBox.style.display = 'block';
    } else {
      alertBox.style.display = 'none';
    }
  });
