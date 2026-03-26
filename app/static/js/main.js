function atualizarRelogio() {
  const el = document.getElementById("clock");
  if (!el) return;

  const agora = new Date();
  el.textContent = agora.toLocaleTimeString("pt-BR", { hour12: false });
}

setInterval(atualizarRelogio, 1000);
atualizarRelogio();

// Countdown
const INTERVALO = 15;
let segundosRestantes = INTERVALO;

const nextUpdateEl = document.getElementById("countdown");

function atualizarCountdown() {
  if (!nextUpdateEl) return;

  segundosRestantes--;

  if (segundosRestantes <= 0) {
    location.reload();
    return;
  }

  nextUpdateEl.innerHTML = `${segundosRestantes}s`;
}

setInterval(atualizarCountdown, 1000);

document.addEventListener("DOMContentLoaded", () => {
  const primeiraLinha = document.querySelector(".row-new");
  if (primeiraLinha) {
    primeiraLinha.style.borderLeft = "2px solid var(--accent)";
  }
});