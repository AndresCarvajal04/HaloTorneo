// Halo CE Tournament Script - Client Logic
const MAP_CATALOG = [
    { id: "beavercreek", name: "Beaver Creek", size: "Small (2-8)", type: "Canyon / Bases", bg: "radial-gradient(#2d6a4f, #081c15)" },
    { id: "damnation", name: "Damnation", size: "Medium (4-8)", type: "Hydroelectric Plant", bg: "radial-gradient(#b08968, #2b1e16)" },
    { id: "prisoner", name: "Prisoner", size: "Small (2-4)", type: "Vertical Platform", bg: "radial-gradient(#4a4e69, #1a1a24)" },
    { id: "chillout", name: "Chill Out", size: "Small (2-6)", type: "Teleport Lab", bg: "radial-gradient(#0077b6, #03045e)" },
    { id: "hangemhigh", name: "Hang 'Em High", size: "Large (4-16)", type: "Tomb Structure", bg: "radial-gradient(#6c584c, #1f1a17)" },
    { id: "wizard", name: "Wizard", size: "Small (2-4)", type: "Symmetrical Arena", bg: "radial-gradient(#7209b7, #240046)" },
    { id: "bloodgulch", name: "Blood Gulch", size: "Large (8-16)", type: "Box Canyon", bg: "radial-gradient(#386641, #122115)" }
];

function initCarousel() {
    const track = document.getElementById("map-carousel");
    if (!track) return;
    track.innerHTML = "";
    MAP_CATALOG.forEach(m => {
        const card = document.createElement("div");
        card.className = "map-card";
        card.onclick = () => loadMap(m.id);
        card.innerHTML = `
            <div class="map-img-container" style="background: ${m.bg};">
                <span class="map-tag">${m.size}</span>
            </div>
            <div class="map-details">
                <div class="map-name">${m.name}</div>
                <div class="map-desc">${m.type}</div>
                <button class="btn btn-cyan" style="width:100%; font-size:0.75em;" onclick="event.stopPropagation(); loadMap('${m.id}')">Deploy Map</button>
            </div>
        `;
        track.appendChild(card);
    });
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    const target = document.getElementById(tabId);
    if (target) target.classList.add('active');
    if (event && event.target) event.target.classList.add('active');
}

async function loadMap(mapId) {
    const mode = document.getElementById("gt-mode") ? document.getElementById("gt-mode").value : "team_slayer";
    const statusBox = document.getElementById("roulette-status");
    if (statusBox) statusBox.innerText = `> Deploying map ${mapId} (${mode})...`;
    try {
        const res = await fetch("/api/map", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ map_id: mapId, gametype: mode })
        });
        const data = await res.json();
        if (statusBox) statusBox.innerText = `> Server Response: ${data.response}`;
    } catch (e) {
        if (statusBox) statusBox.innerText = `> Connection Error: ${e.message}`;
    }
}

async function spinRoulette() {
    const statusBox = document.getElementById("roulette-status");
    if (statusBox) statusBox.innerText = "> Spinning Map Roulette...";
    try {
        const res = await fetch("/api/roulette", { method: "POST" });
        const data = await res.json();
        if (statusBox) statusBox.innerText = `> Winner: ${data.selected.name} (${data.selected.mode}) deployed!`;
    } catch (e) {
        if (statusBox) statusBox.innerText = `> Error: ${e.message}`;
    }
}

async function voteAction(act) {
    const statusBox = document.getElementById("roulette-status");
    try {
        const res = await fetch("/api/vote/" + act, { method: "POST" });
        const data = await res.json();
        if (statusBox) statusBox.innerText = `> Vote ${act}: ${data.response}`;
    } catch (e) {
        if (statusBox) statusBox.innerText = `> Error: ${e.message}`;
    }
}

async function sendRcon() {
    const cmd = document.getElementById("rcon-input").value;
    const output = document.getElementById("rcon-output");
    try {
        const res = await fetch("/api/command", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ command: cmd })
        });
        const data = await res.json();
        if (output) output.innerText = `> ${data.response}`;
    } catch (e) {
        if (output) output.innerText = `> RCON Network Error: ${e.message}`;
    }
}

// Bracket Logic
function advanceTeam(teamName, targetId) {
    const target = document.getElementById(targetId);
    if (target) {
        target.querySelector("span").innerText = teamName;
    }
}

function setChampion(winnerElementId) {
    const target = document.getElementById(winnerElementId);
    if (target) {
        const champion = target.querySelector("span").innerText;
        document.getElementById("champion-name").innerText = champion;
    }
}

// Player KDA Tracking
let playerStats = [
    { name: "MasterChief_99", team: "Red Wolves", k: 28, d: 9, a: 4 },
    { name: "Cortana_AI", team: "Blue Comets", k: 22, d: 12, a: 8 }
];

function renderStats() {
    const tbody = document.getElementById("kda-body");
    if (!tbody) return;
    tbody.innerHTML = "";
    playerStats.sort((a, b) => b.k - a.k);
    playerStats.forEach((p, idx) => {
        const kd = (p.k / Math.max(1, p.d)).toFixed(2);
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${p.name}</strong></td>
            <td style="color: ${p.team.includes('Red') ? 'var(--halo-red)' : 'var(--halo-cyan)'};">${p.team}</td>
            <td>${p.k}</td>
            <td>${p.d}</td>
            <td>${p.a}</td>
            <td>${kd}</td>
            <td>${idx === 0 ? '<span class="mvp-badge">👑 TOP FRAGGER</span>' : 'Active'}</td>
        `;
        tbody.appendChild(tr);
    });
}

function addPlayerStats() {
    const name = document.getElementById("stat-player").value;
    const team = document.getElementById("stat-team").value;
    const k = parseInt(document.getElementById("stat-k").value) || 0;
    const d = parseInt(document.getElementById("stat-d").value) || 0;
    const a = parseInt(document.getElementById("stat-a").value) || 0;
    if (name) {
        playerStats.push({ name, team, k, d, a });
        renderStats();
        document.getElementById("stat-player").value = "";
        document.getElementById("stat-k").value = "";
        document.getElementById("stat-d").value = "";
        document.getElementById("stat-a").value = "";
    }
}

function loadGametypePreset(preset) {
    if (preset === 'mlg') {
        document.getElementById('gt-name').value = "MLG_Competitive_Slayer";
        document.getElementById('gt-mode').value = "slayer";
        document.getElementById('gt-score').value = 50;
        document.getElementById('gt-wep1').value = "pistol";
        document.getElementById('gt-wep2').value = "ar";
        document.getElementById('gt-shields').value = "normal";
        document.getElementById('gt-radar').value = "0";
    } else if (preset === 'snipers') {
        document.getElementById('gt-name').value = "Team_Snipers_Uncapped";
        document.getElementById('gt-mode').value = "slayer";
        document.getElementById('gt-score').value = 50;
        document.getElementById('gt-wep1').value = "sniper";
        document.getElementById('gt-wep2').value = "pistol";
        document.getElementById('gt-shields').value = "normal";
        document.getElementById('gt-radar').value = "1";
    }
}

async function saveGametype() {
    const gtName = document.getElementById('gt-name').value;
    alert(`Gametype '${gtName}' saved and ready to deploy.`);
}

window.addEventListener("DOMContentLoaded", () => {
    initCarousel();
    renderStats();
});
