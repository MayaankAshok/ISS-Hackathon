fetch('/Navbar/navbar.html')
.then(res => res.text())
.then(text => {
    let oldelem = document.querySelector("script#replace_with_navbar");
    var pageName = oldelem.dataset.page;
    let newelem = document.createElement("div");
    newelem.innerHTML = text;
    var items = newelem.getElementsByClassName('navbar')[0].getElementsByClassName('menu-item');
    for (var i = 0 ; i < items.length; i++ ){
        items[i].addEventListener('mouseover', (e)=>{
            e.currentTarget.style.color = 'rgb(234, 122, 11)';
            e.currentTarget.style.backgroundImage  = 'radial-gradient(ellipse at 50% 50%, rgba(236, 231, 185, 0.308), rgba(200, 186, 31, 0) 75%)';
        });
        items[i].addEventListener('mouseout', (e)=>{
            e.currentTarget.style.color = 'var(--main-color)';
            e.currentTarget.style.backgroundImage  = '';
        });
    }
    oldelem.parentNode.replaceChild(newelem,oldelem);
})