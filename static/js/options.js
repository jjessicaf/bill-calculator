document.addEventListener('DOMContentLoaded', (event) => {

  let isActive = undefined;
  let assignment = {};

  function selectPerson(e) {
    if (isActive) {
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
    if (!(isActive.innerHTML in assignment)) {
      assignment[isActive.innerHTML] = [];
    }
    else {
      items.forEach(function (item) {
        if (assignment[isActive.innerHTML].includes(item.innerHTML)) {
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
    let input1 = item.querySelector('input');
    let id = isActive.getAttribute('name').substring(6);
    console.log(id);
    let elementToUpdate = document.getElementById(id);

    // check if already assigned that item, this indicates a remove
    if (assignment[isActive.innerHTML].includes(input1.name)) {
      //remove from assignment
      let index = assignment[isActive.innerHTML].indexOf(input1.name);
      if (index > -1) assignment[isActive.innerHTML].splice(index, 1);

      // remove from value of isActive
      let substring = ", " + input1.name;
      elementToUpdate.value = elementToUpdate.value.replace(substring, '');

      //remove active
      item.classList.remove('active');
    }
    else { // add item
      elementToUpdate.value += ", " + input1.name;
      assignment[isActive.innerHTML].push(input1.name);
      item.classList.add('active');
      // console.log(isActive.innerHTML + ", " + input1.name);
    }
  }

  let names = document.querySelectorAll('.name');
  names.forEach(function (name) {
    name.addEventListener('click', selectPerson);
  });

  let items = document.querySelectorAll('.item');
  items.forEach(function (item) {
    item.addEventListener('click', updateItem);
  });
});
