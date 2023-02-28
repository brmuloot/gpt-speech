// Récupère le bouton qui permet de basculer entre les modes clair et sombre
const darkModeBtn = document.getElementById('dark-mode-btn');

// Récupère l'élément body de la page
const body = document.body;

// Ajoute un événement de clic sur le bouton
darkModeBtn.addEventListener('click', () => {
  // Ajoute ou supprime la classe "dark-mode" à l'élément body, selon que le mode sombre est actuellement activé ou non
  body.classList.toggle('dark-mode');
  
  // Change le texte du bouton en fonction du mode actuel (sombre ou clair)
  if (body.classList.contains('dark-mode')) {
    darkModeBtn.innerText = 'Light Mode';
  } else {
    darkModeBtn.innerText = 'Dark Mode';
  }
});