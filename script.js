document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded successfully!");

    // ======================= Dark Mode Toggle =======================
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';

    document.body.classList.toggle('dark-mode', currentTheme === 'dark');
    themeToggle.classList.toggle('fa-sun', currentTheme === 'light');
    themeToggle.classList.toggle('fa-moon', currentTheme === 'dark');

    themeToggle.addEventListener('click', () => {
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        themeToggle.classList.toggle('fa-sun', !isDark); // Show sun in light mode
        themeToggle.classList.toggle('fa-moon', isDark); // Show moon in dark mode
    });
});

    

    // ======================= Profile Picture Upload =======================
    const profilePicInput = document.getElementById("uploadProfilePic");
    const profilePic = document.querySelector(".profile-pic");
    const savedPic = localStorage.getItem("profilePic");
    if (savedPic && profilePic) profilePic.src = savedPic;
    if (profilePicInput) {
        profilePicInput.addEventListener("change", (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    profilePic.src = e.target.result;
                    localStorage.setItem("profilePic", e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    }
    const removeBtn = document.getElementById("removeProfilePic");
    if (removeBtn) {
        removeBtn.addEventListener("click", () => {
            profilePic.src = "img/default-avatar.png";
            localStorage.removeItem("profilePic");
        });
    }

    // ======================= Profile Edit / Save =======================
    const profileName = document.getElementById("profileName");
    const profileEmail = document.getElementById("profileEmail");
    const profileUsername = document.getElementById("profileUsername");
    const profilePassword = document.getElementById("profilePassword");
    const editProfileBtn = document.getElementById("editProfile");
    const saveProfileBtn = document.getElementById("saveProfile");
    const cancelEditBtn = document.getElementById("cancelEdit");
    let originalProfile = {};

    function loadProfileData() {
        const userData = JSON.parse(localStorage.getItem("userData"));
        if (userData) {
            profileName.value = userData.name || "";
            profileEmail.value = userData.email || "";
            profileUsername.value = userData.username || "";
            profilePassword.value = userData.password || "";
            originalProfile = { ...userData };
        }
    }

    loadProfileData();

    if (editProfileBtn && saveProfileBtn && cancelEditBtn) {
        saveProfileBtn.style.display = "inline-block";
        cancelEditBtn.style.display = "inline-block";

        editProfileBtn.addEventListener("click", () => {
            document.querySelectorAll(".editable-field").forEach(field => field.removeAttribute("disabled"));
        });

        saveProfileBtn.addEventListener("click", () => {
            const updatedProfile = {
                name: profileName.value.trim(),
                email: profileEmail.value.trim(),
                username: profileUsername.value.trim(),
                password: profilePassword.value.trim()
            };
            localStorage.setItem("userData", JSON.stringify(updatedProfile));
            alert("Profile updated successfully!");
            document.querySelectorAll(".editable-field").forEach(field => field.setAttribute("disabled", true));
        });

        cancelEditBtn.addEventListener("click", () => {
            profileName.value = originalProfile.name;
            profileEmail.value = originalProfile.email;
            profileUsername.value = originalProfile.username;
            profilePassword.value = originalProfile.password;
            document.querySelectorAll(".editable-field").forEach(field => field.setAttribute("disabled", true));
        });
    }

    // ======================= Logout =======================
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("userData");
            localStorage.removeItem("profilePic");
            window.location.href = "index.html";
        });
    }

    // ======================= Domain Button Animation =======================
    const domainButtons = document.querySelectorAll(".domain-btn");
    domainButtons.forEach((btn, index) => {
        btn.style.animationDelay = `${index * 0.1}s`;
        btn.addEventListener("mouseenter", () => {
            btn.style.transform = "scale(1.2) rotate(-2deg)";
            btn.style.boxShadow = "0 15px 40px rgba(0, 0, 0, 0.6)";
        });
        btn.addEventListener("mouseleave", () => {
            btn.style.transform = "scale(1)";
            btn.style.boxShadow = "0 5px 15px rgba(0, 0, 0, 0.3)";
        });
    });

    // ======================= Auto Logout After Inactivity =======================
    let logoutTimer;
    function resetLogoutTimer() {
        clearTimeout(logoutTimer);
        logoutTimer = setTimeout(() => {
            alert("Session expired! Logging out...");
            window.location.href = "index.html";
        }, 10 * 60 * 1000); // 10 minutes
    }
    document.addEventListener("mousemove", resetLogoutTimer);
    document.addEventListener("keypress", resetLogoutTimer);
    resetLogoutTimer();

    // ======================= Section Navigation =======================
    const sections = document.querySelectorAll(".section");
    const menuLinks = document.querySelectorAll(".menu-link");

    function showSection(target) {
        sections.forEach(section => {
            section.classList.remove("active");
            section.style.display = "none";
        });
        const targetSection = document.getElementById(target);
        if (targetSection) {
            targetSection.classList.add("active");
            targetSection.style.display = "block";
        }
    }

    menuLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const target = this.getAttribute("data-target");
            showSection(target);
        });
    });

    if (sections.length > 0) {
        sections[0].classList.add("active");
        sections[0].style.display = "block";
    }

    // ======================= Login Functionality =======================
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const email = document.getElementById("loginEmail").value;
            const password = document.getElementById("loginPassword").value;

            if (email && password) {
                localStorage.setItem("userData", JSON.stringify({
                    name: "User",
                    email: email,
                    username: "User123",
                    password: password
                }));
                window.location.href = "dashboard.html";
            } else {
                alert("Invalid email or password.");
            }
        });
    }

    // ======================= Signup Functionality with Progress =======================
    const signupForm = document.getElementById("signupForm");
    const progressBar = document.getElementById("signupProgressBar");
    const nameInput = document.getElementById('signupName');
    const emailInput = document.getElementById('signupEmail');
    const usernameInput = document.getElementById('signupUsername');
    const passwordInput = document.getElementById('signupPassword');
    const confirmPasswordInput = document.getElementById('signupConfirmPassword');
    const termsCheckbox = document.getElementById('termsCheckbox');

    const fieldStatus = {
        fullName: false,
        email: false,
        username: false,
        password: false,
        confirmPassword: false,
        terms: false
    };

    function updateProgress() {
        const total = Object.keys(fieldStatus).length;
        const filled = Object.values(fieldStatus).filter(status => status).length;
        const percent = (filled / total) * 100;
        if (progressBar) {
            progressBar.style.width = percent + '%';
            progressBar.innerText = Math.round(percent) + '%';
        }
    }

    function validateEmail() {
        const email = emailInput?.value.trim();
        fieldStatus.email = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
        updateProgress();
    }

    function validateUsername() {
        const username = usernameInput?.value.trim();
        fieldStatus.username = username.length >= 3;
        updateProgress();
    }

    function validatePassword() {
        const pass = passwordInput?.value.trim();
        const confirm = confirmPasswordInput?.value.trim();
        const valid = pass.length >= 6 && pass === confirm;
        fieldStatus.password = valid;
        fieldStatus.confirmPassword = valid;
        updateProgress();
    }

    if (termsCheckbox) {
        termsCheckbox.addEventListener('change', (e) => {
            fieldStatus.terms = e.target.checked;
            updateProgress();
        });
    }

    nameInput?.addEventListener('input', () => {
        fieldStatus.fullName = nameInput.value.trim().length > 0;
        updateProgress();
    });

    emailInput?.addEventListener('input', validateEmail);
    usernameInput?.addEventListener('input', validateUsername);
    passwordInput?.addEventListener('input', validatePassword);
    confirmPasswordInput?.addEventListener('input', validatePassword);

    if (signupForm) {
        signupForm.addEventListener("submit", function (e) {
            e.preventDefault();
            if (Object.values(fieldStatus).every(status => status === true)) {
                localStorage.setItem("userData", JSON.stringify({
                    name: nameInput.value.trim(),
                    email: emailInput.value.trim(),
                    username: usernameInput.value.trim(),
                    password: passwordInput.value.trim()
                }));
                window.location.href = "dashboard.html";
            } else {
                alert("Please fill out the form correctly.");
            }
        });
    }
});
