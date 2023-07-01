function selectText(element) {
    let target = element.querySelector('h3');
    let copiedText = target.textContent;
    navigator.clipboard.writeText(copiedText);

    let tooltip = element.querySelector('.tooltiptext');
    tooltip.innerHTML = "copied!";
    element.style.backgroundColor = '#fff6e4';
}

function resetTooltip(element) {
    let tooltip = element.querySelector('.tooltiptext');
    tooltip.innerHTML = "copy total";
    element.style.backgroundColor = '#f5f6f8';
}

/*
returns result page but without the buttons
 */
function copyPage() {
    let currentUrl = window.location.href;
    /* TO-DO: remove the buttons in the page rendered */
    let to_remove = ['removable'];
    let modifiedUrl = currentUrl;
    console.log(modifiedUrl);
    to_remove.forEach(function(item) {
        let regex = new RegExp(item + '=\\d', 'g');
        modifiedUrl = modifiedUrl.replace(item, '');
        console.log(item + " " + modifiedUrl);
    });
    let temp = document.createElement('input');
    temp.id = 'tempInput';
    temp.value = modifiedUrl;
    document.body.appendChild(temp);
    temp.select();
    document.execCommand('copy');
    document.body.removeChild(temp);
}

function animateRipple(e) {
    const button = e.target;
    const rect = button.getBoundingClientRect();

    button.textContent = "copied!";

    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    let buttonCenterX = rect.left + rect.width / 2;
    let buttonCenterY = rect.top + rect.height / 2;

    ripple.style.top = `${buttonCenterY - 1.07*rect.top}px`;
    ripple.style.left = `${buttonCenterX - 1.13*rect.left}px`;

    const ripple_container = document.createElement('span');
    ripple_container.className = 'ripple_container';
    ripple_container.appendChild(ripple);

    button.appendChild(ripple_container);
    button.classList.add('ripple_action');

    setTimeout(() => {
        button.textContent = "share";
        ripple_container.remove();
        button.classList.remove('ripple_action');
    }, 600);
}

document.addEventListener('DOMContentLoaded', (event) => {
    let button = document.getElementById('share');
    button.addEventListener('click', animateRipple);
});