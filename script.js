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

// ── Estado global ─────────────────────────────
let datos          = null
let filasTabla     = []
let plataformaActual = 'bluesky'
let miGrafico      = null   // se crea una sola vez
let graficoPlatforma = null
let filasMostradas = 10     // paginación tabla

// ── Cargar datos.json ─────────────────────────
fetch('datos.json')
  .then(res => res.json())
  .then(json => {
    datos      = json
    filasTabla = json.tabla || []
    renderTabla()
    // El gráfico general se construye cuando #seccion-grafico
    // se hace visible (~2.8s de delay en la animación CSS)
    setTimeout(construirGraficoGeneral, 2900)
  })
  .catch(() => {
    document.getElementById('cuerpo-tabla').innerHTML =
      `<tr><td colspan="4" style="color:#ffb4ab;padding:20px">
        ⚠ No se pudo cargar datos.json. Usá Live Server o python -m http.server.
      </td></tr>`
  })

// ── Gráfico general (se crea UNA sola vez) ────
function construirGraficoGeneral() {
  const todasEtiquetas = [...new Set([
    ...datos.bluesky.etiquetas,
    ...datos.fuente2.etiquetas
  ])]

  const valoresCombinados = todasEtiquetas.map(etiqueta => {
    const iBsky    = datos.bluesky.etiquetas.indexOf(etiqueta)
    const iFuente2 = datos.fuente2.etiquetas.indexOf(etiqueta)
    return (iBsky    !== -1 ? datos.bluesky.valores[iBsky]    : 0)
         + (iFuente2 !== -1 ? datos.fuente2.valores[iFuente2] : 0)
  })

  const ctx = document.getElementById('mi-grafico').getContext('2d')

  miGrafico = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: todasEtiquetas,
      datasets: [{
        label: 'Total de posts',
        data: valoresCombinados,
        backgroundColor: 'rgba(208,188,255,0.75)',
        borderColor: '#d0bcff',
        borderWidth: 1,
        borderRadius: 10,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: 'rgba(73,69,79,0.3)' } },
        x: { grid: { display: false } }
      },
      ...animacionModerna
    }
  })
}