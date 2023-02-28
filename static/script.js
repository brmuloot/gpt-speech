const darkModeBtn = document.getElementById('dark-mode-btn');
const body = document.body;

darkModeBtn.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
  if (body.classList.contains('dark-mode')) {
    darkModeBtn.innerText = 'Light Mode';
  } else {
    darkModeBtn.innerText = 'Dark Mode';
  }
});

