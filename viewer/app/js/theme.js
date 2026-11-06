// Aplica o tema escolhido antes da primeira pintura. A escolha fica só neste
// navegador (localStorage); sem ela, vale o tema do sistema.
(function () {
  var choice = null;
  try {
    choice = localStorage.getItem("viewer-theme");
  } catch (error) {
    choice = null;
  }
  if (choice === "light" || choice === "dark") document.documentElement.dataset.theme = choice;
})();
