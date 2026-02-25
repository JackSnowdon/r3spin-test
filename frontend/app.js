const API_BASE = "http://localhost:8000";

const input = document.getElementById("item-input");
const addBtn = document.getElementById("add-btn");
const list = document.getElementById("items-list");
const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

function setStatus(text, kind = "default") {
    statusDot.classList.remove("ok", "error");
    if (kind === "ok") statusDot.classList.add("ok");
    if (kind === "error") statusDot.classList.add("error");
    statusText.textContent = text;
}

function renderItems(items) {
    list.innerHTML = "";
    if (!items || !Array.isArray(items) || items.length === 0) {
        const empty = document.createElement("li");
        empty.className = "item";
        empty.textContent = "No items yet — add one above.";
        list.appendChild(empty);
        return;
    }

    for (const item of items) {
        const li = document.createElement("li");
        li.className = "item";

        const label = document.createElement("span");
        label.textContent = item.name ?? "(no name)";

        const del = document.createElement("button");
        del.textContent = "Remove";
        del.addEventListener("click", () => deleteItem(item.id));

        li.appendChild(label);
        li.appendChild(del);
        list.appendChild(li);
    }
}

async function fetchItems() {
    try {
        setStatus("Loading items…");
        const res = await fetch(`${API_BASE}/api/items`);
        if (!res.ok) {
            throw new Error(`GET /api/items failed: ${res.status}`);
        }
        const data = await res.json();
        renderItems(data);
        setStatus("Connected to backend", "ok");
    } catch (err) {
        console.error(err);
        setStatus("Cannot reach backend — check your API", "error");
    }
}

async function createItem(name) {
    try {
        const res = await fetch(`${API_BASE}/api/items`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name }),
        });
        if (!res.ok) {
            throw new Error(`POST /api/items failed: ${res.status}`);
        }
        await fetchItems();
    } catch (err) {
        console.error(err);
        setStatus("Failed to create item", "error");
    }
}

async function deleteItem(id) {
    try {
        const res = await fetch(`${API_BASE}/api/items/${id}`, {
            method: "DELETE",
        });
        if (!res.ok) {
            throw new Error(`DELETE /api/items/${id} failed: ${res.status}`);
        }
        await fetchItems();
    } catch (err) {
        console.error(err);
        setStatus("Failed to delete item", "error");
    }
}

addBtn.addEventListener("click", () => {
    const value = input.value.trim();
    if (!value) return;
    createItem(value);
    input.value = "";
    input.focus();
});

input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        addBtn.click();
    }
});

fetchItems();

