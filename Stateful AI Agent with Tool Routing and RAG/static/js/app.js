document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("[data-agent-form]");
  const input = document.querySelector("#message");
  const sendButton = document.querySelector("[data-send-button]");
  const workingMessage = document.querySelector("[data-working-message]");

  document.querySelectorAll("[data-prompt]").forEach((button) => {
    button.addEventListener("click", () => {
      if (!input) return;
      input.value = button.dataset.prompt || "";
      input.focus();
    });
  });

  form?.addEventListener("submit", () => {
    if (sendButton) {
      sendButton.disabled = true;
      sendButton.textContent = "Working…";
    }
    if (workingMessage) workingMessage.hidden = false;
  });
});

