// ── Tema global Chart.js ──────────────────────
Chart.defaults.color       = '#948f9a'
Chart.defaults.borderColor = 'rgba(73,69,79,0.35)'
Chart.defaults.font.family = "'Be Vietnam Pro', sans-serif"
Chart.defaults.font.size   = 13

// ── Animación moderna para barras ─────────────
// Crecen desde el centro hacia afuera con delay escalonado
const animacionModerna = {
  animation: {
    duration: 900,
    easing: 'easeOutQuart',
    delay: (ctx) => {
      if (ctx.type !== 'data' || ctx.mode !== 'default') return 0
      return ctx.dataIndex * 80
    }
  },
  transitions: {
    active: { animation: { duration: 200 } }
  }
}

// ── Typewriter ────────────────────────────────
const TITULO = 'Monitor de Desinformación'

function typewriter(texto, elemento, velocidad = 55) {
  let i = 0
  elemento.textContent = ''
  const intervalo = setInterval(() => {
    elemento.textContent += texto[i]
    i++
    if (i >= texto.length) clearInterval(intervalo)
  }, velocidad)
}

// ── Control de animaciones de entrada ────────
const ELEMENTOS_ANIMADOS = [
  '#encabezado p',
  '.contenedor-botones',
  '#seccion-grafico',
  '#seccion-tabla'
]

function activarAnimaciones() {
  ELEMENTOS_ANIMADOS.forEach(sel => {
    const el = document.querySelector(sel)
    if (!el) return
    // Reiniciar: quitar clase, forzar reflow, volver a poner
    el.classList.remove('animar-entrada')
    void el.offsetWidth   // fuerza reflow del navegador
    el.classList.add('animar-entrada')
  })
}

document.addEventListener('DOMContentLoaded', () => {
  const span = document.getElementById('texto-titulo')
  if (span) typewriter(TITULO, span, 55)
  activarAnimaciones()
})