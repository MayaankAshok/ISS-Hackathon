
fetch('/Navbar/navbar.html')
.then(res => res.text())
.then(text => {
    let oldelem = document.querySelector("script#replace_with_navbar");
    let newelem = document.createElement("div");
    newelem.innerHTML = `<link rel="stylesheet" href="/Navbar/navbar.css">
    <div class="navbar">
        <img src="/ImageResources/Logo.png" class="navbar-logo" alt="LOGO">
        <div class="navbar-items">
            <a class="menu-item" href="/DashboardPage/dashboard.html?id=`+ String(id) +`">DASHBOARD</a>
            <a class="menu-item" href="/ExpenseTrackingPage/expense.html?id=`+ String(id) +`">EXPENSE TRACKING</a>
            <a class="login-link" href="/LoginPage/login.html">LOGIN / SIGN UP</a>
        </div>
    </div>`;
    oldelem.parentNode.replaceChild(newelem,oldelem);
})