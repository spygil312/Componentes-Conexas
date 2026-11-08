const PASOS = [["nodos", "Número de nodos", "var(--mor)"],
["tipo", "Tipo de grafo", "var(--azu)"],
["generar", "Generar grafo", "var(--men)"],
["matriz", "Matriz y grafo", "var(--cor)"],
["conexas", "Componentes conexas", "var(--ros)"],
["resultado", "Resultado final", "var(--mor)"]];

const PAL = ["#9b6bff",
  "#4da3ff",
  "#33c98f",
  "#ff8f6b",
  "#ff6fa0",
  "#f5b942",
  "#2cc4d6",
  "#b565e0",
  "#8bc34a",
  "#e05252",
  "#5c6bc0",
  "#8d6e63"];

let S = { n: null, tipo: null, M: null, paso: "nodos", res: null, sub: 0, pos: null };
const $ = id => document.getElementById(id);
const rnd = (a, b) => a + Math.floor(Math.random() * (b - a + 1));

function initTheme() {
  const root = document.documentElement, button = $("themeToggle");
  let theme = "light";
  try {
    const savedTheme = localStorage.getItem("componentes-conexas-theme");
    if (savedTheme === "light" || savedTheme === "dark") theme = savedTheme;
  } catch (error) {
    console.warn("No se pudo leer la preferencia de tema guardada.", error);
  }
  const applyTheme = () => {
    const nextTheme = theme === "light" ? "oscuro" : "claro";
    root.dataset.theme = theme;
    button.setAttribute("aria-label", `Cambiar a modo ${nextTheme}`);
    button.title = `Cambiar a modo ${nextTheme}`;
    button.setAttribute("aria-pressed", String(theme === "dark"));
  };
  applyTheme();
  button.addEventListener("click", () => {
    theme = theme === "light" ? "dark" : "light";
    applyTheme();
    try {
      localStorage.setItem("componentes-conexas-theme", theme);
    } catch (error) {
      console.warn("No se pudo guardar la preferencia de tema.", error);
    }
  });
}

/* ---------- logica ---------- */
const vacia = n => Array.from({ length: n }, () => Array(n).fill(0));
function aleatorio(n) {
  const M = vacia(n), k = rnd(n, Math.floor(n * 1.5)); let c = 0;
  while (c < k) { const i = rnd(0, n - 1), j = rnd(0, n - 1); if (!M[i][j]) { M[i][j] = 1; c++ } } return [M, k]
}

function posAleatorias(n, T = 320, margen = 46, distMin = 60) {
  const pos = []; let intentos = 0;
  while (pos.length < n) {
    const x = margen + Math.random() * (T - 2 * margen);
    const y = margen + Math.random() * (T - 2 * margen);
    const minima = intentos < 500 ? distMin : intentos < 1500 ? distMin * 0.6 : 34;
    if (pos.every(([px, py]) => Math.hypot(x - px, y - py) >= minima)) { pos.push([x, y]); intentos = 0 }
    else intentos++;
  }
  return pos;
}

const mtxt = m => "[" + m.map(r => "[" + r.join(" ") + "]").join("\n ") + "]";
const tcomp = (i, m) => `V${i + 1} = {${m.map(j => j + 1).join(", ")}}`;

function calc(M) {
  const n = M.length, ids = [...Array(n).keys()], P = [];
  const d = M.map(r => [...r]), hl = {};
  for (let i = 0; i < n; i++)if (!d[i][i]) { d[i][i] = 1; hl[i + "," + i] = "var(--cor)" }
  P.push({ t: "Paso 1: agregar 1 en la diagonal", x: "Se hace una copia de la matriz y se coloca 1 en su diagonal (celdas coral) para que cada nodo se alcance a sí mismo. La matriz original del grafo no se modifica.", m: d.map(r => [...r]), f: ids, c: ids, hl, bl: [] });
  const w = d.map(r => [...r]);
  for (let k = 0; k < n; k++)for (let i = 0; i < n; i++)for (let j = 0; j < n; j++)if (!w[i][j] && w[i][k] && w[k][j]) w[i][j] = 1;
  P.push({ t: "Paso 2: matriz de caminos", x: "Se calcula la matriz de caminos considerando todas las posibles conexiones entre los nodos. Se muestra directamente el resultado final de la matriz.", m: w.map(r => [...r]), f: ids, c: ids, hl: {}, bl: [] });
  const cu = w.map(r => r.reduce((a, b) => a + b, 0));
  const cmp = (a, b) => { for (let k = 0; k < n; k++)if (w[a][k] !== w[b][k]) return w[a][k] - w[b][k]; return 0 };
  const o = [...ids].sort((a, b) => cu[b] - cu[a] || w[a].indexOf(1) - w[b].indexOf(1) || cmp(a, b));
  P.push({ t: "Paso 3: ordenar las filas", x: `Cantidad de 1 por fila → ${ids.map(i => `nodo ${i + 1}: ${cu[i]}`).join(", ")}. Se ordenan de mayor a menor; si empatan, va primero la fila cuyo primer 1 está más a la izquierda. Orden de filas: ${o.map(i => i + 1).join(", ")}.`, m: o.map(i => [...w[i]]), f: o, c: ids, hl: {}, bl: [] });
  const cd = Array(n).fill(-1), comps = [];
  for (const i of o) if (cd[i] < 0) { const m = ids.filter(j => w[i][j] && w[j][i]); m.forEach(j => cd[j] = comps.length); comps.push(m) }
  const bl = comps.map((m, k) => { const p = m.map(j => o.indexOf(j)); return [Math.min(...p), Math.max(...p), PAL[k % PAL.length]] });
  P.push({
    t: "Paso 4: ordenar las columnas y hallar los bloques",
    x: `Se reordenan las columnas con el mismo orden de las filas. Los bloques cuadrados diagonales de unos (cuadros de color) son las componentes conexas: ${comps.map((m, i) => tcomp(i, m)).join("; ")}.`, m: o.map(i => o.map(j => w[i][j])), f: o, c: o, hl: {}, bl
  });
  return { P, comps, col: ids.map(i => PAL[cd[i] % PAL.length]) };
}

/* ---------- Dibujo ---------- */
function mx(m, f, c, hl = {}, bl = []) {
  const n = m.length, s = n > 8 ? 22 : 28;
  let h = `<div class="mxw" style="--c:${s}px"><div class="mx" style="grid-template-columns:repeat(${n + 1},var(--c))"><i></i>`;
  c.forEach(x => h += `<i class="h">${x + 1}</i>`);
  m.forEach((r, i) => {
    h += `<i class="h">${f[i] + 1}</i>`;
    r.forEach((v, j) => {
      let col = hl[i + "," + j];
      if (!col && v) { const b = bl.find(b => i >= b[0] && i <= b[1] && j >= b[0] && j <= b[1]); col = b ? b[2] : "" }
      h += `<i class="c${v ? " on" : ""}"${col ? ` style="background:${col}"` : ""}>${v}</i>`
    })
  });
  h += "</div>";
  bl.forEach(b => { const k = b[1] - b[0] + 1; h += `<div class="blk" style="left:calc(var(--c)*${b[0] + 1});top:calc(var(--c)*${b[0] + 1});width:calc(var(--c)*${k});height:calc(var(--c)*${k});border-color:${b[2]}"></div>` });
  return h + "</div>";
}
function grafo(M, col, tit = "Representación gráfica") {
  const n = M.length, T = 320, P = [];
  const cl = col || PAL;
  if (!S.pos || S.pos.length !== n) S.pos = posAleatorias(n, T);
  P.push(...S.pos);
  let s = `<div><div class="cap">${tit}</div><svg class="g" viewBox="0 0 ${T} ${T}" role="img" aria-label="${tit}"><defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0L9,4.5L0,9z" fill="var(--lav)"/></marker></defs>`;
  for (let i = 0; i < n; i++)for (let j = 0; j < n; j++)if (M[i][j]) {
    const [x, y] = P[i];
    if (i == j) { s += `<path d="M${x - 8},${y - 14} C${x - 28},${y - 46} ${x + 28},${y - 46} ${x + 8},${y - 14}" fill="none" stroke="var(--azu)" stroke-width="2" marker-end="url(#ar)"/>`; continue }
    const [x2, y2] = P[j], dx = x2 - x, dy = y2 - y, d = Math.hypot(dx, dy), ux = dx / d, uy = dy / d;
    let a = x + ux * 17, b = y + uy * 17, c = x2 - ux * 19, e = y2 - uy * 19;
    if (M[j][i]) { const nx = -uy * 6, ny = ux * 6; a += nx; b += ny; c += nx; e += ny }
    s += `<line x1="${a}" y1="${b}" x2="${c}" y2="${e}" stroke="var(--lav)" stroke-width="2" marker-end="url(#ar)"/>`
  }
  P.forEach(([x, y], i) => s += `<circle cx="${x}" cy="${y}" r="16" fill="${cl[i % cl.length]}"/><text x="${x}" y="${y + 4.5}" text-anchor="middle" fill="#fff">${i + 1}</text>`);
  return s + "</svg></div>";
}

/* ---------- Consola ---------- */
function log(msg, c = "t") { const L = $("log"), d = document.createElement("div"); d.className = c; d.textContent = msg; L.appendChild(d); L.scrollTop = L.scrollHeight }
const titulo = t => log("\n" + t, "ti");

/* ---------- Stepper ---------- */
function estado(p) {
  if (p == "nodos") return S.n !== null ? "ok" : "on";
  if (p == "tipo") return S.n === null ? "lock" : S.tipo !== null ? "ok" : "on";
  if (p == "generar") return S.tipo === null ? "lock" : S.M ? "ok" : "on";
  return S.M ? "on" : "lock";
}
function stepper() {
  $("stp").innerHTML = PASOS.map(([id, t, c], i) => {
    const e = estado(id);
    return `<button class="st ${e == "lock" ? "lock" : ""} ${id == S.paso && e != "lock" ? "cur" : ""}" style="color:${c}" ${e == "lock" ? "disabled" : ""} onclick="go('${id}')"><b${e != "lock" ? ` style="background:${c}"` : ""}>${e == "lock" ? "🔒" : e == "ok" ? "✓" : i + 1}</b><span style="color:var(--tx)">${t}</span></button>`
  }).join("");
}
function go(p) { S.paso = p; ({ nodos: vNodos, tipo: vTipo, generar: vGenerar, matriz: vMatriz, conexas: vConexas, resultado: vResultado })[p](); stepper() }
const W = (t, s) => { $("work").innerHTML = `<h2>${t}</h2><p class="s">${s || ""}</p>`; return $("work") };
const add = h => $("work").insertAdjacentHTML("beforeend", h);

/* ---------- Vistas ---------- */
function vNodos() {
  W("① Número de nodos", "Elige un valor entre 4 y 12.");
  add(`<div class="row" style="align-items:flex-end"><div><label for="nn">Nodos</label><input id="nn" type="number" min="4" max="12" value="${S.n ?? ""}"></div><button class="chip" style="background:var(--mor)" onclick="regNodos()">Registrar →</button></div>`);
  $("nn").addEventListener("keydown", e => { if (e.key == "Enter") regNodos() });
}
function regNodos() {
  const v = $("nn").value.trim(), n = Number(v);
  if (v === "" || !Number.isInteger(n)) { log("Error: Tipo de dato incorrecto", "e"); return }
  if (n < 4 || n > 12) { log("Error: El número de nodos debe de estar entre [4, 12]", "e"); return }
  /* >>> Reiniciar posiciones al cambiar el número de nodos <<< */
  S.n = n; S.M = null; S.res = null; S.pos = null; log("Cantidad de nodos registrados correctamente: " + n, "ok"); go("tipo");
}
function vTipo() {
  if (S.n === null) { log("Error: Tienes que seleccionar un número de nodos primero", "e"); return go("nodos") }
  W("② Tipo de grafo", "¿Cómo quieres construir las conexiones?");
  add(`<div class="acts"><button class="chip" style="background:var(--azu)" onclick="elegir('manual')">✎ Manual</button><button class="chip" style="background:var(--men)" onclick="elegir('aleatorio')">🎲 Aleatorio</button></div>`);
}
function elegir(t) {
  /* >>> Reiniciar posiciones al elegir el tipo de grafo <<< */
  S.tipo = t; S.res = null; S.pos = null; log("Tipo de grafo seleccionado: " + t, "ok");
  if (t == "aleatorio") { genAl(); go("matriz") } else { S.M = vacia(S.n); go("generar") }
}
function genAl() {
  /* >>> Reiniciar posiciones cada vez que se genera un grafo aleatorio nuevo <<< */
  const [M, k] = aleatorio(S.n); S.M = M; S.res = null; S.pos = null;
  titulo("GRAFO ALEATORIO"); log(`Nodos disponibles del [1 - ${S.n}]`, "m"); log(k + " conexiones registradas correctamente", "ok");
}
function vGenerar() {
  if (S.n === null) { log("Error: Tienes que seleccionar un número de nodos primero", "e"); return go("nodos") }
  if (S.tipo === null) { log("Error: Tienes que seleccionar un tipo de grafo primero", "e"); return go("tipo") }
  if (S.tipo == "aleatorio") {
    W("③ Grafo aleatorio", "Ya hay un grafo generado. Puedes crear otro o seguir.");
    add(`<div class="acts"><button class="chip" style="background:var(--men)" onclick="genAl();go('matriz')">🎲 Generar otro</button><button class="chip sec" onclick="go('matriz')">Ver matriz →</button></div>`); return
  }
  if (!S.M) S.M = vacia(S.n);
  titulo("GRAFO MANUAL INTERACTIVO"); log("Haz clic en cualquier celda para activar/desactivar conexiones (Origen → Destino).", "m");
  W("③ Conexiones del grafo", "Fila = nodo origen · Columna = nodo destino. Haz clic en una celda para cambiarla.");
  const n = S.n, s = n > 8 ? 24 : 30;
  let h = `<div class="graph-editor"><div class="scroll graph-matrix"><div class="cap">Matriz interactiva</div><div class="mx" style="--c:${s}px;grid-template-columns:repeat(${n + 1},var(--c))"><i class="h">O\\D</i>`;
  for (let j = 0; j < n; j++)h += `<i class="h">${j + 1}</i>`;
  for (let i = 0; i < n; i++) { h += `<i class="h">${i + 1}</i>`; for (let j = 0; j < n; j++)h += `<button class="cell${i == j ? " d" : ""}${S.M[i][j] ? " on" : ""}" id="b${i}_${j}" aria-label="${i + 1} a ${j + 1}" onclick="tog(${i},${j})">${S.M[i][j]}</button>` }
  h += `</div></div><div id="gv">${grafo(S.M, null, "Grafo en tiempo real")}</div></div><div class="acts right graph-confirm"><button class="chip" style="background:var(--ros)" onclick="fin()">✓ Confirmar grafo</button></div>`;
  add(h);
}
function tog(r, c) {
  const v = S.M[r][c] ? 0 : 1; S.M[r][c] = v; S.res = null;
  const b = $(`b${r}_${c}`); b.textContent = v; b.classList.toggle("on", !!v);
  if (r == c && v) log("Bucle activado en nodo " + (r + 1), "d");
  else if (v) log(`Conexión agregada: ${r + 1} → ${c + 1}`, "d"); else log(`Conexión removida: ${r + 1} → ${c + 1}`, "m");
  $("gv").innerHTML = grafo(S.M, null, "Grafo en tiempo real");
}
function fin() { log(`Grafo configurado con ${S.M.flat().reduce((a, b) => a + b, 0)} conexión(es) en total.`, "ok"); go("matriz") }
function vMatriz() {
  if (!S.M) { log("Error: Tienes que generar el grafo primero", "e"); return go(S.tipo ? "generar" : "tipo") }
  titulo("MATRIZ DE ADYACENCIA"); log(mtxt(S.M));
  const ids = [...Array(S.n).keys()];
  W("④ Matriz y representación gráfica", "");
  add(`<div class="row"><div class="scroll"><div class="cap">Matriz de adyacencia</div>${mx(S.M, ids, ids)}</div>${grafo(S.M)}</div><div class="acts right"><button class="chip" style="background:var(--ros)" onclick="go('conexas')">Buscar componentes →</button></div>`);
}
function vConexas() {
  if (!S.M) { log("Error: Tienes que generar el grafo primero", "e"); return go("generar") }
  S.res = calc(S.M); S.sub = 0; titulo("COMPONENTES CONEXAS"); log("Usa «Siguiente» para avanzar etapa por etapa.", "m"); etapa(true);
}
function mover(d) { S.sub += d; etapa(d > 0) }
function etapa(reg) {
  const P = S.res.P, p = P[S.sub], t = P.length;
  W(`⑤ Componentes conexas · etapa ${S.sub + 1} de ${t}`, p.t);
  add(`<div class="row"><div class="scroll">${mx(p.m, p.f, p.c, p.hl, p.bl)}</div><div class="txt"><p style="margin:0">${p.x}</p><div class="acts">${S.sub > 0 ? `<button class="chip sec" onclick="mover(-1)">← Anterior</button>` : ""}${S.sub < t - 1 ? `<button class="chip" style="background:var(--ros)" onclick="mover(1)">Siguiente →</button>` : `<button class="chip" style="background:var(--men)" onclick="go('resultado')">✓ Resultado</button>`}</div></div></div>`);
  if (reg) { log(`Etapa ${S.sub + 1}/${t} — ${p.t}`, "d"); log(p.x); log(mtxt(p.m)) }
}
function vResultado() {
  if (!S.M) { log("Error: Tienes que generar el grafo primero", "e"); return go("generar") }
  if (!S.res) S.res = calc(S.M);
  const r = S.res;
  W("⑥ Resumen de componentes conexas", "Resultado final del algoritmo");
  add(`<div class="row">${grafo(S.M, r.col, "Grafo por componentes")}<div style="flex:1;min-width:230px"><div class="big">Total de componentes conexas: ${r.comps.length}</div>${r.comps.map((m, i) => `<div class="comp"><b style="color:${PAL[i % PAL.length]}">Componente ${i + 1}:</b><span>${tcomp(i, m)}</span></div>`).join("")}</div></div>`);
  titulo("⑥ RESULTADO FINAL"); log(`Proceso finalizado. Se encontraron ${r.comps.length} componente(s) conexa(s).`, "ok");
}

initTheme();
go("nodos"); log("Bienvenido. Empieza eligiendo el número de nodos.", "m");
