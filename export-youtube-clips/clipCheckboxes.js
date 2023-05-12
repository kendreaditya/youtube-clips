let lastCheckedCheckbox = null;
let shiftKeyActive = false;

function addCheckMarks() {
  console.log('Adding check marks to thumbnails');
  const thumbnails = document.querySelectorAll('a#thumbnail');

  thumbnails.forEach((thumbnail) => {
    const overlaysDiv = thumbnail.querySelector('div#overlays');

    // Create the checkbox element
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'check-mark';

    // Apply CSS to position the checkmark at the top right corner
    checkbox.style.position = 'absolute';
    checkbox.style.top = '5px';
    checkbox.style.right = '5px';
    checkbox.style.transform = 'scale(1.5)';

    // Add the checkbox to the overlaysDiv
    overlaysDiv.appendChild(checkbox);

    // Add event listener to prevent click propagation
    overlaysDiv.addEventListener('click', (event) => {
      if (event.target === checkbox) {
        event.stopPropagation();

        // Check if shift key is pressed
        if (event.shiftKey) {
          handleShiftClick(checkbox);
        } else {
          lastCheckedCheckbox = checkbox;
        }
      }
    });
  });
}

function handleShiftClick(checkbox) {
  if (!lastCheckedCheckbox) {
    lastCheckedCheckbox = checkbox;
    return;
  }

  const checkboxes = Array.from(document.querySelectorAll('input.check-mark'));
  const startIndex = checkboxes.indexOf(checkbox);
  const endIndex = checkboxes.indexOf(lastCheckedCheckbox);

  const [start, end] = startIndex < endIndex ? [startIndex, endIndex] : [endIndex, startIndex];

  checkboxes.slice(start, end + 1).forEach((chk) => {
    chk.checked = checkbox.checked;
  });
}

// Event listener to track the state of the shift key
document.addEventListener('keydown', (event) => {
  if (event.key === 'Shift') {
    shiftKeyActive = true;
  }
});

document.addEventListener('keyup', (event) => {
  if (event.key === 'Shift') {
    shiftKeyActive = false;
    lastCheckedCheckbox = null;
  }
});

// Wait for the page to fully load before adding the check marks
window.addEventListener("load", () => {
    setTimeout(function() {
        addCheckMarks();
    }, 2000)
});
