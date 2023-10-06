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
        // listItem.innerHTML = `<strong>${role.title}</strong><p>${role.description}</p><button onclick="viewRoleDetails(${index})">View Details</button>`;
        listItem.innerHTML = 
        `
            <div class="card" id="role${index}" style="width: 18rem;">
                <div class="card-body">
                    <a href="javascript:viewRoleDetails(${index});" class="card-title fw-bold" style="color: black; text-decoration: none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'" onclick="toggleBorder(${index})">${role.title}</a>
                    <p class="card-text">${role.description}</p>
                </div>
            </div>
        `
        roleList.appendChild(listItem);
    });
}
// hello
// function for border
function toggleBorder(index) {
    // Get the element corresponding to the clicked card
    var card = document.getElementById('role' + index);

    // Get all card elements by class name
    var cards = document.getElementsByClassName('card');

    // Remove the border from all cards
    for (var i = 0; i < cards.length; i++) {
        cards[i].style.borderColor = '#BDBDBD';
    }

    // Add the border to the clicked card
    card.style.borderColor = '#FC6C85';
}

// Function to view role details
function viewRoleDetails(index) {
    const roleDescription = document.getElementById('role-description');
    // roleDescription.innerHTML = `<strong>${openRoles[index].title}</strong><p>${openRoles[index].description}</p><button onclick="applyForRole(${index})">Apply</button>`;
    roleDescription.innerHTML = 
    `
        <div class="card" style="width: 18rem; border-color: #FC6C85;">
            <div class="card-body">
                <strong class="card-title">${openRoles[index].title}</strong>
                <p class="card-text">${openRoles[index].description}</p>
                <button class="btn" style="background-color: #FC6C85; color: white" onclick="applyForRole(${index})">Apply</button>
            </div>
        </div>
    `
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
