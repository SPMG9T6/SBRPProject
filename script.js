// Simulated data for open roles
const openRoles = [
    { title: 'Role 1', description: 'Description for Role 1' },
    { title: 'Role 2', description: 'Description for Role 2' },
    // Add more role data here
];

// Simulated data for staff applications
const staffApplications = [];

// Function to display open roles
function displayOpenRoles() {
    const roleList = document.getElementById('role-list');
    roleList.innerHTML = '';

    openRoles.forEach((role, index) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<strong>${role.title}</strong><p>${role.description}</p><button onclick="viewRoleDetails(${index})">View Details</button>`;
        roleList.appendChild(listItem);
    });
}

// Function to view role details
function viewRoleDetails(index) {
    const roleDescription = document.getElementById('role-description');
    roleDescription.innerHTML = `<strong>${openRoles[index].title}</strong><p>${openRoles[index].description}</p><button onclick="applyForRole(${index})">Apply</button>`;
}

// Function to simulate staff applying for a role
function applyForRole(index) {
    const appliedRole = openRoles[index];
    staffApplications.push(appliedRole);

    // Update the staff applications list
    const applicationList = document.getElementById('application-list');
    const listItem = document.createElement('li');
    listItem.innerHTML = `<strong>${appliedRole.title}</strong><p>${appliedRole.description}</p>`;
    applicationList.appendChild(listItem);
}

// Initialize the page
displayOpenRoles();
