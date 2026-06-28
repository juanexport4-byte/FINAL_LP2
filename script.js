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