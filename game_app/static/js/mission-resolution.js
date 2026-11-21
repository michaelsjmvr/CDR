(() => {
  const completionDialog = document.querySelector('#mission-completion-dialog');
  const continueButton = document.querySelector('#mission-completion-continue');
  if (completionDialog && typeof completionDialog.showModal === 'function' && !completionDialog.open) {
    completionDialog.showModal();
  }
  continueButton?.addEventListener('click', () => completionDialog?.close());

  const form = document.querySelector('#mission-loot-form');
  if (!form) return;
  const checkboxes = [...form.querySelectorAll('input[name="keep_item_ids"]')];
  const submit = document.querySelector('#mission-loot-submit');
  const feedback = document.querySelector('#capacity-feedback');
  const currentCount = Number(form.dataset.inventoryCount);
  const capacity = Number(form.dataset.inventoryCapacity);

  const updateCapacity = () => {
    const keptCount = checkboxes.filter((checkbox) => checkbox.checked).length;
    const projectedCount = currentCount + keptCount;
    const exceedsCapacity = projectedCount > capacity;
    submit.disabled = exceedsCapacity;
    feedback.textContent = exceedsCapacity
      ? `A seleção ocupa ${projectedCount} espaços. Libere ${projectedCount - capacity} espaço(s) ou desmarque espólios.`
      : `Após confirmar: ${projectedCount} / ${capacity} espaços ocupados.`;
  };
  checkboxes.forEach((checkbox) => checkbox.addEventListener('change', updateCapacity));
  updateCapacity();
})();
