function showToast(message)
{
    const toast =
    document.createElement("div");

    toast.className = "toast";

    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() =>
    {
        toast.remove();
    },3000);
}

/* ==========================
   Dashboard
========================== */

async function loadDashboard()
{
    const response =
    await fetch("/api/dashboard");

    const data =
    await response.json();

    const badge =
    document.getElementById("statusBadge");

    if(badge)
    {
        if(data.running)
        {
            badge.innerHTML =
            "🟢 Running";

            badge.className =
            "badge success-badge";
        }
        else
        {
            badge.innerHTML =
            "🔴 Stopped";

            badge.className =
            "badge danger-badge";
        }
    }

    const mode =
    document.getElementById("modeCard");

    if(mode)
    {
        mode.innerText =
        data.mode.toUpperCase();
    }

    const count =
    document.getElementById("ruleCount");

    if(count)
    {
        count.innerText =
        data.total_rules;
    }
}

/* ==========================
   Firewall Controls
========================== */

async function startFirewall()
{
    const response =
    await fetch("/api/start_firewall");

    const data =
    await response.json();

    showToast(data.message);

    loadDashboard();
}

async function stopFirewall()
{
    const response =
    await fetch("/api/stop_firewall");

    const data =
    await response.json();

    showToast(data.message);

    loadDashboard();
}

/* ==========================
   Rules
========================== */

async function loadRules()
{
    const response =
    await fetch("/api/rules");

    const data =
    await response.json();

    const table =
    document.getElementById("rulesTable");

    if(table)
    {
        table.innerHTML = "";

        data.ips.forEach(
        (ip,index)=>
        {
            table.innerHTML += `
            <tr>
                <td>${index+1}</td>
                <td>${ip}</td>
            </tr>
            `;
        });
    }

    const mode =
    document.getElementById("modeSelect");

    if(mode)
    {
        mode.value =
        data.mode;
    }
}

async function addIP()
{
    const ip =
    document.getElementById("ipInput").value;

    if(!ip)
    {
        showToast("Enter IP Address");
        return;
    }

    const response =
    await fetch("/api/add_ip",
    {
        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },

        body:JSON.stringify({ip})
    });

    const data =
    await response.json();

    showToast(data.message);

    loadRules();

    document.getElementById(
        "ipInput"
    ).value = "";
}

async function removeIP()
{
    const ip =
    document.getElementById("ipInput").value;

    if(!ip)
    {
        showToast("Enter IP Address");
        return;
    }

    const response =
    await fetch("/api/remove_ip",
    {
        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },

        body:JSON.stringify({ip})
    });

    const data =
    await response.json();

    showToast(data.message);

    loadRules();

    document.getElementById(
        "ipInput"
    ).value = "";
}

async function changeMode()
{
    const mode =
    document.getElementById("modeSelect").value;

    const response =
    await fetch("/api/set_mode",
    {
        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },

        body:JSON.stringify({mode})
    });

    const data =
    await response.json();

    showToast(data.message);
}

/* ==========================
   Logs
========================== */

async function loadLogs()
{
    const response =
    await fetch("/api/logs");

    const data =
    await response.json();

    const logs =
    document.getElementById(
        "logsContainer"
    );

    if(logs)
    {
        logs.textContent =
        data.logs;

        logs.scrollTop =
        logs.scrollHeight;
    }
}

function downloadLogs()
{
    window.location.href =
    "/download_logs";
}

/* ==========================
   Auto Load
========================== */

document.addEventListener(
    "DOMContentLoaded",
    () =>
    {
        loadDashboard();
    }
);