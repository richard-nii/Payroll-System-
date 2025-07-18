// admin.js

document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll(".view-link");

  links.forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const empId = this.getAttribute("data-empid");
      alert(`Payslip preview for Employee ID: ${empId} (feature coming soon)`);
      // In the future: window.location.href = `/admin/payslip/${empId}`;
    });
  });
});
