(() => {
  const friendsDialog = document.querySelector('#friends-dialog');
  document.querySelectorAll('[data-open-friends]').forEach((slot) => {
    slot.addEventListener('click', () => friendsDialog?.showModal());
  });
  document.querySelectorAll('[data-close-friends]').forEach((button) => {
    button.addEventListener('click', () => friendsDialog?.close());
  });
  friendsDialog?.addEventListener('click', (event) => {
    if (event.target === friendsDialog) friendsDialog.close();
  });
})();
