document.addEventListener("DOMContentLoaded", function() {
    const tabs = Array.from(document.querySelectorAll(".nav.nav-tabs a"));
    let currentIndex = 0;

    // Create Next button
    const nextBtn = document.createElement("button");
    nextBtn.type = "button";
    nextBtn.innerHTML = 'Next <i class="fas fa-angle-double-right"></i>';
    nextBtn.className = "btn btn-outline-primary";
    // Style the button
    nextBtn.style.cssText = `
        float: right;
        margin: 10px;
        display: block;
    `;
    document.querySelector(".tab-content").appendChild(nextBtn);

    nextBtn.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % tabs.length;
        tabs[currentIndex].click();
    });


    const prevBtn = document.createElement("button");
    prevBtn.type = "button";
    prevBtn.innerHTML = '<i class="fas fa-angle-double-left"></i> Previous';
    prevBtn.className = "btn btn-outline-secondary";
    document.querySelector(".tab-content").appendChild(prevBtn);

    prevBtn.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + tabs.length) % tabs.length;
        tabs[currentIndex].click();
    });
});
