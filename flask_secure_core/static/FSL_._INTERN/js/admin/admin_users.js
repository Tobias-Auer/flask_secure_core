let users = [];

fetch("/admin/api/users")
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
    users = data;
  })
  .then(() => renderUsers())
  .catch((error) => console.error("Error fetching user data:", error));

const tbody = document.querySelector("#userTable tbody");
const searchInput = document.getElementById("search");
const roleFilter = document.getElementById("roleFilter");
const statusFilter = document.getElementById("statusFilter");
const totalUsersEl = document.getElementById("totalUsers");
const activeUsersEl = document.getElementById("activeUsers");
const adminsEl = document.getElementById("admins");
const disabledEl = document.getElementById("disabled");

let currentPage = 1;
const rowsPerPage = 10;
let currentSort = { key: "", direction: "asc" };

function renderStats() {
  totalUsersEl.textContent = users.length;
  activeUsersEl.textContent = users.filter(
    (u) => u.status === "Enabled"
  ).length;
  adminsEl.textContent = users.filter((u) => u.role === "Administrator").length;
  disabledEl.textContent = users.filter((u) => u.status === "Disabled").length;
}

function getFilteredUsers() {
  const search = searchInput.value.toLowerCase();
  const role = roleFilter.value;
  const status = statusFilter.value;

  return users.filter(
    (u) =>
      (u.display_name.toLowerCase().includes(search) ||
        u.username.toLowerCase().includes(search) ||
        u.email.toLowerCase().includes(search)) &&
      (role === "" || u.role === role) &&
      (status === "" || u.status === status)
  );
}

function renderUsers() {
  const filtered = getFilteredUsers();
  const start = (currentPage - 1) * rowsPerPage;
  const end = start + rowsPerPage;
  const paginated = filtered.slice(start, end);

  tbody.innerHTML = paginated
    .map(
      (u, i) => `
    <tr>
      <td>${u.display_name}</td>
      <td>${u.username}</td>
      <td>${u.email}</td>
      <td><span class="role-badge role-${u.role}">${u.role}</span></td>
      <td class="${
        u.status === "Enabled" ? "status-enabled" : "status-disabled"
      }">${u.status}</td>
      <td>${u.lastLogin}</td>
      <td>${u.created}</td>
      <td>
        <span class="actions-btn" onclick="editUser(${start + i})">✏️</span>
        <span class="actions-btn" onclick="deleteUser(${start + i})">🗑️</span>
      </td>
    </tr>`
    )
    .join("");

  renderPagination(filtered.length);
  renderStats();
}

function renderPagination(totalItems) {
  const totalPages = Math.ceil(totalItems / rowsPerPage);
  document.getElementById(
    "pageInfo"
  ).textContent = `Page ${currentPage} of ${totalPages}`;
  document.getElementById("prevPage").disabled = currentPage === 1;
  document.getElementById("nextPage").disabled = currentPage === totalPages;
}

document.getElementById("prevPage").onclick = () => {
  currentPage--;
  renderUsers();
};

document.getElementById("nextPage").onclick = () => {
  currentPage++;
  renderUsers();
};

searchInput.addEventListener("input", () => {
  currentPage = 1;
  renderUsers();
});
roleFilter.addEventListener("change", () => {
  currentPage = 1;
  renderUsers();
});
statusFilter.addEventListener("change", () => {
  currentPage = 1;
  renderUsers();
});

function sortTable(key) {
  if (currentSort.key === key) {
    currentSort.direction = currentSort.direction === "asc" ? "desc" : "asc";
  } else {
    currentSort.key = key;
    currentSort.direction = "asc";
  }
  users.sort((a, b) => {
    const valA = a[key].toLowerCase ? a[key].toLowerCase() : a[key];
    const valB = b[key].toLowerCase ? b[key].toLowerCase() : b[key];
    if (valA < valB) return currentSort.direction === "asc" ? -1 : 1;
    if (valA > valB) return currentSort.direction === "asc" ? 1 : -1;
    return 0;
  });
  renderUsers();
}
document
  .querySelectorAll("th[data-sort]")
  .forEach((th) =>
    th.addEventListener("click", () => sortTable(th.dataset.sort))
  );

// Modal logic
const modal = document.getElementById("userModal");
const cancelBtn = document.getElementById("cancelBtn");
const addUserBtn = document.getElementById("addUserBtn");
const userForm = document.getElementById("userForm");
let editIndex = null;

addUserBtn.onclick = () => openModal(false);
cancelBtn.onclick = closeModal;

function openModal(edit, index) {
  modal.style.display = "flex";
  document.getElementById("modalTitle").textContent = edit
    ? "Edit User"
    : "Add User";
  if (edit) {
    const u = users[index];
    editIndex = index;
    fullName.value = u.display_name;
    username.value = u.username;
    email.value = u.email;
    permission.value = u.role;
    state.value = u.status;
  } else {
    editIndex = null;
    userForm.reset();
  }
}

function closeModal() {
  modal.style.display = "none";
}
window.onclick = (e) => {
  if (e.target === modal) closeModal();
};

userForm.onsubmit = (e) => {
  e.preventDefault();
  const newUser = {
    display_name: fullName.value,
    username: username.value,
    email: email.value,
    role: permission.value,
    status: state.value,
    password: pwd.value,
    lastLogin: null,
  };

  if (editIndex === null) {
    fetch("/admin/api/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newUser),
    })
      .then((response) => {
        if (!response.ok) alert("Error adding user:<br>" + response.error);
      })
      .then((data) => {
        users.push(newUser);
        closeModal();
        renderUsers();
      })
      .catch((error) => console.error("Error adding user:", error));
    return;
  } else {
    fetch(`/admin/api/users/${users[editIndex].username}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newUser),
    })
      .then((response) => {
        if (!response.ok)
          alert("Error updating user:<br>" + response.error);
        users[editIndex] = newUser;
        closeModal();
        renderUsers();
      })
      .catch((error) => console.error("Error updating user:", error));
  }
};

function editUser(index) {
  openModal(true, index);
}

function deleteUser(index) {
  if (confirm("Delete this user?")) {
    users.splice(index, 1);
    renderUsers();
  }
}

renderUsers();
