document.addEventListener("DOMContentLoaded", function() {
          document.querySelectorAll(".contact-form").forEach(function(form) {
              const nameInput = form.querySelector('input[name="name"]');
              const phoneInput = form.querySelector('input[name="phone"]');

              if (nameInput) {
                  function validateName() {
                      const isValid = /^[A-Za-zА-Яа-яЁё -]{2,}$/.test(nameInput.value.trim());
                      nameInput.setCustomValidity(isValid ? "" : "Введите имя буквами, без цифр");
                  }

                  nameInput.addEventListener("input", function() {
                      nameInput.value = nameInput.value.replace(/[^A-Za-zА-Яа-яЁё -]/g, "");
                      validateName();
                  });

                  nameInput.addEventListener("blur", validateName);
              }

              if (!phoneInput) {
                  return;
              }

              function getPhoneDigits(value) {
                  const digits = value.replace(/\D/g, "");

                  if (!digits) {
                      return "";
                  }

                  if (digits.startsWith("8")) {
                      return "7" + digits.slice(1, 11);
                  }

                  if (digits.startsWith("7")) {
                      return digits.slice(0, 11);
                  }

                  return "7" + digits.slice(0, 10);
              }

              function formatPhone(value) {
                  const digits = getPhoneDigits(value);

                  if (!digits) {
                      return "";
                  }

                  const number = digits.slice(1, 11);
                  const parts = [
                      number.slice(0, 3),
                      number.slice(3, 6),
                      number.slice(6, 8),
                      number.slice(8, 10),
                  ];

                  let formatted = "+7";

                  if (parts[0]) {
                      formatted += " (" + parts[0];
                  }

                  if (parts[0].length === 3) {
                      formatted += ")";
                  }

                  if (parts[1]) {
                      formatted += " " + parts[1];
                  }

                  if (parts[2]) {
                      formatted += "-" + parts[2];
                  }

                  if (parts[3]) {
                      formatted += "-" + parts[3];
                  }

                  return formatted;
              }

              function validatePhone() {
                  const isComplete = phoneInput.value.replace(/\D/g, "").length === 11;
                  phoneInput.setCustomValidity(isComplete ? "" : "Введите телефон в формате +7 (999) 999-99-99");
              }

              phoneInput.addEventListener("input", function() {
                  phoneInput.value = formatPhone(phoneInput.value);
                  validatePhone();
              });

              phoneInput.addEventListener("blur", validatePhone);

              form.addEventListener("submit", function() {
                  phoneInput.value = formatPhone(phoneInput.value);
                  validatePhone();
              });
          });
      });
