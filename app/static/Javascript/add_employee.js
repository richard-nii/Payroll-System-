
document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  form.addEventListener('submit', (e) => {
    const accountNumber = form.bank_account_number.value.trim();
    if (!/^[0-9]{8,20}$/.test(accountNumber)) {
      alert("Please enter a valid bank account number.");
      e.preventDefault();
    }
  });
});
