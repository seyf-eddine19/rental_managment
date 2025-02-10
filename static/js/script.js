document.getElementById("sidebarToggle").addEventListener("click", function () {
    const sidebar = document.querySelector(".sidebar");
    const mainContent = document.querySelector(".main");

    if (sidebar.style.right == 0) {
        sidebar.style.right = "-230px";
        mainContent.style.marginRight = 0;
    } else {
        sidebar.style.right = 0;
        mainContent.style.marginRight = "230px";
    }
});