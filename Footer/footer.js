fetch('../Footer/footer.html')
.then(res => res.text())
.then(text => {
    let oldelem = document.querySelector("script#replace_with_footer");
    let newelem = document.createElement("footer");
    newelem.innerHTML = text;       
    oldelem.parentNode.replaceChild(newelem,oldelem);
    const Name = "#WebName#";
    let index = 0;
    let isTyping = false;

    function type() {
        document.getElementById("WebName").innerHTML += Name.charAt(index);
        index++;
        if (index >= Name.length) {
            clearInterval(interval);
        }
    }

    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && !isTyping) {
            isTyping = true;
            const interval = setInterval(type, 100);
            document.getElementById("WebName").style.opacity = 1;
        }
    });

    observer.observe(document.getElementById("WebName"));
    console.log(document.getElementById("WebName"));
})


