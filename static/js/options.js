document.addEventListener('DOMContentLoaded', (event) => {

  let isActive = undefined;
  let assignment = {};

  function selectPerson(e) {
    if (isActive) { // previously selected a person, de-select
      isActive.classList.remove('active');
      items.forEach(function (item) {
        item.classList.remove('active');
      });
    }
    if (e.target == isActive) {
      isActive = undefined;
      return;
    }
    isActive = e.target;
    isActive.classList.add('active');
    if (!(isActive.innerHTML in assignment)) { // has not been assigned any items yet
      assignment[isActive.innerHTML] = [];
    }
    else { // already assigned other items
      items.forEach(function (item) {
        if (assignment[isActive.innerHTML].includes(item.dataset.elementName)) {
          item.classList.add('active');
        }
      });
    }
  }

  function updateItem(e) {
    if (isActive == undefined) return;
    // add that item to the person, then will return to flask as output
    if (!(isActive.innerHTML in assignment)) {
      assignment[isActive.innerHTML] = [];
    }

    let item = e.target;
    let elementToUpdate = document.getElementById(isActive.innerHTML);

    // check if already assigned that item, this indicates a remove
    if (assignment[isActive.innerHTML].includes(item.dataset.elementName)) {
      //remove from assignment
      let index = assignment[isActive.innerHTML].indexOf(item.dataset.elementName);
      if (index > -1) assignment[isActive.innerHTML].splice(index, 1);

      // remove from value of isActive
      let substring = ", " + item.dataset.elementName;
      elementToUpdate.value = elementToUpdate.value.replace(substring, '');

      //remove active
      item.classList.remove('active');
    }
    else { // add item
      elementToUpdate.value += ", " + item.dataset.elementName;
      assignment[isActive.innerHTML].push(item.dataset.elementName);
      item.classList.add('active');
    }
  }

  const names = document.querySelectorAll('.name');
  names.forEach(function (name) {
    name.addEventListener('click', selectPerson);
  });

  const items = document.querySelectorAll('.item');
  items.forEach(function (item) {
    item.addEventListener('click', updateItem);
  });
});
