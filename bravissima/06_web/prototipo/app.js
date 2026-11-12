/* bravissima — interacciones del prototipo (sin dependencias) */
(function () {
  // menú mobile
  var menu = document.querySelector(".menu-mobile");
  var abrir = document.querySelector(".menu-btn");
  var cerrar = document.querySelector(".menu-mobile .cerrar");
  function setMenu(abierto) {
    if (!menu) return;
    menu.classList.toggle("abierto", abierto);
    menu.setAttribute("aria-hidden", abierto ? "false" : "true");
    if (abrir) abrir.setAttribute("aria-expanded", abierto ? "true" : "false");
    document.body.style.overflow = abierto ? "hidden" : "";
  }
  if (abrir) abrir.addEventListener("click", function () { setMenu(true); });
  if (cerrar) cerrar.addEventListener("click", function () { setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });

  // cuenta regresiva al lanzamiento: 3 de diciembre de 2026, 00:00 hora de Córdoba (UTC−3)
  var LANZAMIENTO = new Date("2026-12-03T00:00:00-03:00").getTime();
  var nodos = document.querySelectorAll("[data-cuenta]");
  var barra = document.querySelector("[data-dias]");
  function dos(n) { return n < 10 ? "0" + n : "" + n; }
  function tic() {
    var resto = Math.max(0, LANZAMIENTO - Date.now());
    var d = Math.floor(resto / 864e5), h = Math.floor(resto / 36e5) % 24, m = Math.floor(resto / 6e4) % 60, s = Math.floor(resto / 1e3) % 60;
    nodos.forEach(function (n) {
      var v = { dias: d, horas: h, minutos: m, segundos: s }[n.getAttribute("data-cuenta")];
      n.textContent = dos(v);
    });
    if (barra) barra.textContent = resto > 0 ? (d === 1 ? "falta 1 día" : "faltan " + d + " días") : "ya llegó";
  }
  if (nodos.length || barra) { tic(); setInterval(tic, 1000); }

  // filtros de colecciones
  var filtros = document.querySelectorAll(".filtros button");
  filtros.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.getAttribute("data-filtro");
      filtros.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      document.querySelectorAll("[data-coleccion]").forEach(function (p) {
        p.hidden = !(f === "todas" || p.getAttribute("data-coleccion") === f);
      });
    });
  });
  var hash = location.hash.replace("#", "");
  if (hash) { var b = document.querySelector('.filtros button[data-filtro="' + hash + '"]'); if (b) b.click(); }

  // galería de la ficha
  var principal = document.querySelector(".galeria .principal span");
  document.querySelectorAll(".galeria .miniaturas button").forEach(function (b, i, todos) {
    b.addEventListener("click", function () {
      todos.forEach(function (x) { x.setAttribute("aria-current", x === b ? "true" : "false"); });
      if (principal) principal.textContent = "foto " + (i + 1) + " de la pieza";
    });
  });

  // cantidad
  var out = document.querySelector(".cantidad output");
  document.querySelectorAll(".cantidad button").forEach(function (b) {
    b.addEventListener("click", function () {
      var n = parseInt(out.textContent, 10) + (b.getAttribute("data-paso") === "+" ? 1 : -1);
      out.textContent = Math.max(1, n);
    });
  });

  // agregar al carrito (simulado)
  var cuenta = document.querySelector(".carrito .cuenta");
  var agregar = document.querySelector("[data-agregar]");
  if (agregar) agregar.addEventListener("click", function () {
    var n = parseInt(cuenta.textContent || "0", 10) + parseInt(out ? out.textContent : "1", 10);
    cuenta.textContent = n; cuenta.hidden = false;
    agregar.textContent = "agregado ✓";
    setTimeout(function () { agregar.textContent = "agregar al carrito"; }, 1800);
  });

  // formulario (prototipo: no envía)
  var form = document.querySelector("form.form");
  if (form) form.addEventListener("submit", function (e) {
    e.preventDefault();
    form.innerHTML = '<p class="titulo t-m">gracias, brava.</p><p class="bajada">Te respondemos en breve.</p><p class="nota">(Prototipo: el formulario todavía no envía mensajes.)</p>';
  });
})();
