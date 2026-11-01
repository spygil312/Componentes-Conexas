import math
import random
import numpy as np
import tkinter as tk

# Paleta de colores
BG          = "#faf6ff"
BARRA       = "#f1e9fc"   
CARD        = "#ffffff"   
BORDE       = "#e9defa"
TEXTO       = "#3b2a5e"
TENUE       = "#9c8fc0"
BLOQUEADO   = "#e7e0f5"

LAVANDA     = "#d9c9fb"
CIELO       = "#bfe1ff"
MENTA       = "#bdeeda"
MELOCOTON   = "#ffdfb8"
ROSITA      = "#ffcfe0"

V_MORADO    = "#9b6bff"
V_AZUL      = "#4da3ff"
V_MENTA     = "#33c98f"
V_CORAL     = "#ff8f6b"
V_ROSA      = "#ff6fa0"

OK          = "#2fbf87"
ERROR       = "#ff5c7c"
PALETA_COMP = [V_MORADO, V_AZUL, V_MENTA, V_CORAL, V_ROSA, "#f5b942",
               "#2cc4d6", "#b565e0", "#8bc34a", "#e05252", "#5c6bc0", "#8d6e63"]

# Fuentes
FUENTE      = ("Segoe UI", 10)
FUENTE_BOLD = ("Segoe UI", 10, "bold")
FUENTE_MONO = ("Consolas", 11)
FUENTE_TIT  = ("Segoe UI", 19, "bold")
FUENTE_SUB  = ("Segoe UI", 10)

PASOS = [
    ("nodos",     "Número de nodos",      V_MORADO, "①"),
    ("tipo",      "Tipo de grafo",        V_AZUL,   "②"),
    ("generar",   "Generar grafo",        V_MENTA,  "③"),
    ("matriz",    "Matriz y grafo",       V_CORAL,  "④"),
    ("conexas",   "Componentes conexas",  V_ROSA,   "⑤"),
    ("resultado", "Resultado final",      V_MORADO, "⑥"),
]

# Funciones lógicas
def matriz_vacia(num_nodos):
    matriz = []
    for i in range(num_nodos):
        fila = []
        for j in range(num_nodos):
            fila.append(0)
        matriz.append(fila)
    return matriz

def grafo_aleatorio(num_nodos):
    contador = 0
    matriz = matriz_vacia(num_nodos)
    conexiones_al = random.randint(num_nodos, int(num_nodos * 1.5))

    while contador < conexiones_al:
        inicio = random.randint(1, num_nodos)
        final = random.randint(1, num_nodos)
        if matriz[inicio - 1][final - 1] == 0:
            matriz[inicio - 1][final - 1] = 1
            contador += 1
    return matriz, conexiones_al

def matriz_a_texto(matriz):
    matriz = np.array(matriz)
    return str(matriz)

def color_texto_para(fondo):
    r = int(fondo[1:3], 16); g = int(fondo[3:5], 16); b = int(fondo[5:7], 16)
    luz = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return TEXTO if luz > 0.72 else "#ffffff"
 
def texto_componente(idx, miembros):
    return f"V{idx + 1} = {{" + ", ".join(str(j + 1) for j in miembros) + "}"
 
def calcular_conexas(matriz):
    n = len(matriz)
    pasos = []
    
    # Etapa 1: Copia de la matriz original y lo completa con 1 en la diagonal principal
    diag = [fila[:] for fila in matriz]
    agregados = {}

    for i in range(n):
        if diag[i][i] == 0:
            diag[i][i] = 1
            agregados[(i, i)] = V_CORAL

    pasos.append({
        "titulo": "Paso 1: agregar 1 en la diagonal",
        "texto": ("Se hace una copia de la matriz y se coloca 1 en su diagonal "
                "(celdas coral) para que cada nodo se alcance a sí mismo. "
                "La matriz original del grafo no se modifica."),
        "matriz": [f[:] for f in diag], "filas": list(range(n)),
        "cols": list(range(n)), "resaltes": agregados, "bloques": [], "log_matriz": True,
    })
    
    # Etapa 2: Calcula la matriz de caminos
    caminos = [f[:] for f in diag]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if (
                    caminos[i][j] == 0
                    and caminos[i][k] == 1
                    and caminos[k][j] == 1
                ):
                    caminos[i][j] = 1

    pasos.append({
        "titulo": "Paso 2: matriz de caminos",
        "texto": (
            "Se calcula la matriz de caminos considerando todas las posibles "
            "conexiones entre los nodos. Se muestra directamente el resultado "
            "final de la matriz."
        ),
        "matriz": [f[:] for f in caminos], "filas": list(range(n)), "cols": list(range(n)),
        "resaltes": {}, "bloques": [], "log_matriz": True,
    })
        
    # Orden filas: Más 1's primero; empate -> el 1 más cercano a la primera
    # Orden columnas: mismo orden que para las filas
    cuentas = [sum(f) for f in caminos]
    orden = sorted(range(n), key=lambda i: (-cuentas[i], caminos[i].index(1),
                                            tuple(caminos[i])))
    cuentas_txt = ", ".join(f"nodo {i + 1}: {cuentas[i]}" for i in range(n))
    pasos.append({
        "titulo": "Paso 3: ordenar las filas",
        "texto": (f"Cantidad de 1 por fila → {cuentas_txt}. Se ordenan de mayor a "
                  f"menor; si empatan, va primero la fila cuyo primer 1 está más a "
                  f"la izquierda. Orden de filas: "
                  f"{', '.join(str(i + 1) for i in orden)}."),
        "matriz": [caminos[i][:] for i in orden], "filas": orden,
        "cols": list(range(n)), "resaltes": {}, "bloques": [], "log_matriz": True,
    })
 
    # Componentes: i y j están en la misma si cada uno alcanza al otro
    comp_de = [-1] * n
    componentes = []
    for i in orden:
        if comp_de[i] == -1:
            miembros = [j for j in range(n) if caminos[i][j] == 1 and caminos[j][i] == 1]
            for j in miembros:
                comp_de[j] = len(componentes)
            componentes.append(miembros)

    bloques = []
    for idx, miembros in enumerate(componentes):
        pos = [orden.index(j) for j in miembros]
        bloques.append((min(pos), max(pos), PALETA_COMP[idx % len(PALETA_COMP)]))
 
    lista_comp = "; ".join(texto_componente(i, m) for i, m in enumerate(componentes))
    pasos.append({
        "titulo": "Paso 4: ordenar las columnas y hallar los bloques",
        "texto": ("Se reordenan las columnas con el mismo orden de las filas. "
                  "Los bloques cuadrados diagonales de unos (cuadros de color) "
                  f"son las componentes conexas: {lista_comp}."),
        "matriz": [[caminos[i][j] for j in orden] for i in orden],
        "filas": orden, "cols": orden, "resaltes": {}, "bloques": bloques, "log_matriz": True,
    })
 
    return {
        "pasos": pasos,
        "componentes": componentes,
        "caminos": caminos,
        "orden": orden,
        "color_nodo": [PALETA_COMP[comp_de[i] % len(PALETA_COMP)] for i in range(n)],
    }
                                                                    
# Funciones visuales
def rounded_rect(cnv, x1, y1, x2, y2, radio=14, **kw):
    puntos = [
        x1 + radio, y1, x2 - radio, y1, x2, y1, x2, y1 + radio,
        x2, y2 - radio, x2, y2, x2 - radio, y2, x1 + radio, y2,
        x1, y2, x1, y2 - radio, x1, y1 + radio, x1, y1,
    ]
    return cnv.create_polygon(puntos, smooth=True, **kw)

def tarjeta(padre, **pack_kw):
    marco = tk.Frame(padre, bg=BORDE)
    marco.pack(**pack_kw)
    interior = tk.Frame(marco, bg=CARD)
    interior.pack(fill="both", expand=True, padx=1, pady=1)
    return interior

def campo(padre, etiqueta, ancho=8):
    caja = tk.Frame(padre, bg=CARD)
    caja.pack(side="left", padx=(0, 14))
    tk.Label(caja, text=etiqueta, bg=CARD, fg=TENUE, font=FUENTE).pack(anchor="w")
    entrada = tk.Entry(
        caja, width=ancho, font=("Segoe UI", 12), bg=BG, fg=TEXTO,
        insertbackground=V_MORADO, relief="flat", justify="center",
        highlightthickness=2, highlightbackground=BORDE, highlightcolor=V_MORADO,
    )
    entrada.pack(ipady=6, pady=(4, 0))
    return entrada

def dibujar_matriz_generica(padre, matriz, filas, cols, titulo, resaltes=None, bloques=None):
    n = len(matriz)
    resaltes = resaltes or {}
    bloques = bloques or []
    celda = 28 if n <= 8 else 22
    margen = 34
    tam = margen + celda * n + 10
    fuente_c = ("Segoe UI", 9 if celda >= 28 else 8)
 
    marco = tk.Frame(padre, bg=CARD)
    marco.pack(side="left", padx=(0, 24), anchor="n")
    tk.Label(marco, text=titulo, bg=CARD, fg=TENUE,
             font=FUENTE_BOLD).pack(anchor="center", pady=(0, 6))
    cnv = tk.Canvas(marco, width=tam, height=tam, bg=CARD, highlightthickness=0)
    cnv.pack()
 
    for p in range(n):
        cnv.create_text(margen + celda * p + celda / 2, margen / 2,
                        text=str(cols[p] + 1), fill=TENUE, font=("Segoe UI", 8))
        cnv.create_text(margen / 2, margen + celda * p + celda / 2,
                        text=str(filas[p] + 1), fill=TENUE, font=("Segoe UI", 8))
 
    def color_bloque(i, j):
        for a, b, color in bloques:
            if a <= i <= b and a <= j <= b:
                return color
        return None

    for i in range(n):
        for j in range(n):
            valor = matriz[i][j]
            fondo = V_MORADO if valor == 1 else BG
            if (i, j) in resaltes:
                fondo = resaltes[(i, j)]
            elif valor == 1 and color_bloque(i, j):
                fondo = color_bloque(i, j)
            x1 = margen + celda * j
            y1 = margen + celda * i
            cnv.create_rectangle(x1, y1, x1 + celda, y1 + celda,
                                 fill=fondo, outline=BORDE)
            fg = TENUE if fondo == BG else color_texto_para(fondo)
            cnv.create_text(x1 + celda / 2, y1 + celda / 2, text=str(valor),
                            fill=fg, font=fuente_c)
 
    for a, b, color in bloques:
        cnv.create_rectangle(margen + celda * a, margen + celda * a,
                             margen + celda * (b + 1), margen + celda * (b + 1),
                            outline=color, width=3)


class Chip(tk.Canvas):
    def __init__(self, padre, texto, comando, color, color_texto="#ffffff",
                 icono="", ancho=170, alto=42, bg_fondo=CARD, fuente=FUENTE_BOLD):
        super().__init__(padre, width=ancho, height=alto, bg=bg_fondo,
                          highlightthickness=0, bd=0, cursor="hand2")
        self.comando = comando
        self.color = color
        self.color_hover = self._aclarar(color)
        self.color_texto = color_texto
        self.texto = f"{icono}  {texto}" if icono else texto
        self.ancho, self.alto, self.fuente = ancho, alto, fuente
        self._dibujar(self.color)
        self.bind("<Enter>", lambda _e: self._dibujar(self.color_hover))
        self.bind("<Leave>", lambda _e: self._dibujar(self.color))
        self.bind("<Button-1>", lambda _e: self.comando())

    def _aclarar(self, hexcolor, factor=0.18):
        r = int(hexcolor[1:3], 16); g = int(hexcolor[3:5], 16); b = int(hexcolor[5:7], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _dibujar(self, color):
        self.delete("all")
        rounded_rect(self, 1, 1, self.ancho - 1, self.alto - 1,
                    radio=self.alto / 2, fill=color, outline="")
        self.create_text(self.ancho / 2, self.alto / 2, text=self.texto,
                        fill=self.color_texto, font=self.fuente)


# Clase principal
class AppGrafos:
    def __init__(self, raiz, icono):
        self.icono = icono
        try:
            self.icono.iconbitmap("icon_graf.ico")
        except Exception:
            pass
        self.raiz = raiz
        self.matriz = None
        self.num_nodos = None
        self.tipo_grafo = None
        self.paso_actual = "nodos"
        self.res = None       
        self.sub_paso = 0

        raiz.title("Componentes Conexas")
        raiz.geometry("1080x700")
        raiz.minsize(960, 640)
        raiz.configure(bg=BG)

        self._construir_cabecera()

        cuerpo = tk.Frame(raiz, bg=BG)
        cuerpo.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self._construir_stepper(cuerpo)
        self._construir_area(cuerpo)

        self.op_nodos()
        self.escribir("Bienvenido. Empieza eligiendo el número de nodos.", TENUE)

    # Construir interfaz
    def _construir_cabecera(self):
        cab = tk.Frame(self.raiz, bg=BG)
        cab.pack(fill="x", padx=20, pady=(20, 12))

        tk.Label(cab, text="Componentes Conexas", bg=BG, fg=TEXTO,
                font=FUENTE_TIT).pack(anchor="w")
        
        tk.Label(cab, text="Construye tu grafo, observa su matriz y avanza paso a "
                        "paso hacia sus componentes conexas.",
                bg=BG, fg=TENUE, font=FUENTE_SUB).pack(anchor="w", pady=(2, 10))

        linea = tk.Canvas(cab, height=4, bg=BG, highlightthickness=0)
        linea.pack(fill="x")
        linea.bind("<Configure>", self._pintar_degradado)

    def _construir_stepper(self, padre):
        contenedor = tk.Frame(padre, bg=BARRA, width=260)
        contenedor.pack(side="left", fill="y")
        contenedor.pack_propagate(False)

        tk.Label(contenedor, text="Progreso", bg=BARRA, fg=TENUE,
                 font=FUENTE_BOLD).pack(anchor="w", padx=22, pady=(20, 6))

        self.stepper = tk.Canvas(contenedor, bg=BARRA, highlightthickness=0,
                                  width=260, height=len(PASOS) * 78 + 20)
        self.stepper.pack(fill="x")

        tk.Frame(contenedor, bg=BARRA).pack(fill="both", expand=True)
        Chip(contenedor, "Salir", self.raiz.destroy, "#d8cdf2", color_texto=TEXTO,
             icono="✕", ancho=210, alto=38, bg_fondo=BARRA).pack(pady=16)

        self._dibujar_stepper()

    def _construir_area(self, padre):
        area = tk.Frame(padre, bg=BG)
        area.pack(side="left", fill="both", expand=True, padx=(18, 0))

        self.trabajo = tarjeta(area, fill="both", pady=(0, 14))
        self._marco_trabajo = None
        self.limpiar_trabajo()

        tk.Label(area, text="Historial", bg=BG, fg=TENUE,
                 font=FUENTE_BOLD).pack(anchor="w", pady=(0, 6))
        contenedor_log = tarjeta(area, fill="both", expand=True)

        self.consola = tk.Text(
            contenedor_log, bg=CARD, fg=TEXTO, font=FUENTE_MONO, relief="flat",
            padx=16, pady=12, wrap="word", state="normal",
            insertbackground=V_MORADO, spacing1=1, spacing3=3,
        )
        self.consola.pack(side="left", fill="both", expand=True)

        barra = tk.Scrollbar(contenedor_log, command=self.consola.yview,
                              bg=CARD, troughcolor=CARD, relief="flat",
                              borderwidth=0, width=10)
        
        self.consola.config(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
                                
        for nombre, color in (("texto", TEXTO), ("tenue", TENUE),
                              ("ok", OK), ("error", ERROR),
                              ("titulo", V_ROSA), ("dato", V_AZUL)):
            self.consola.tag_config(nombre, foreground=color)

    # Dibujo de interfaz
    def _dibujar_stepper(self):
        cnv = self.stepper
        cnv.delete("all")
        cx = 40
        y0 = 24
        paso_alto = 78
        y_fin = y0 + paso_alto * (len(PASOS) - 1)
        cnv.create_line(cx, y0, cx, y_fin, fill=BLOQUEADO, width=3)

        for idx, (pid, titulo, color, _num) in enumerate(PASOS):
            cy = y0 + idx * paso_alto
            estado = self._estado_paso(pid)
            es_actual = (pid == self.paso_actual)

            if estado == "bloqueado":
                relleno, contenido, fg_txt = BLOQUEADO, "🔒", TENUE
            elif estado == "completado":
                relleno, contenido, fg_txt = color, "✓", TEXTO
            else:
                relleno, contenido, fg_txt = color, str(idx + 1), TEXTO

            if es_actual and estado != "bloqueado":
                cnv.create_oval(cx - 21, cy - 21, cx + 21, cy + 21,
                                 outline=color, width=2)

            oid = cnv.create_oval(cx - 16, cy - 16, cx + 16, cy + 16,
                                   fill=relleno if estado != "bloqueado" else BLOQUEADO,
                                   outline="")
            tid = cnv.create_text(cx, cy, text=contenido,
                                   fill="#ffffff" if estado != "bloqueado" else TENUE,
                                   font=FUENTE_BOLD)

            fuente = FUENTE_BOLD if es_actual else FUENTE
            ltid = cnv.create_text(cx + 30, cy, text=titulo, anchor="w",
                                    fill=fg_txt, font=fuente)

            if estado != "bloqueado":
                for item in (oid, tid, ltid):
                    cnv.tag_bind(item, "<Button-1>",
                                 lambda _e, p=pid: self._ir_a(p))
                    cnv.tag_bind(item, "<Enter>", lambda _e: cnv.config(cursor="hand2"))
                    cnv.tag_bind(item, "<Leave>", lambda _e: cnv.config(cursor="arrow"))
   
    def _dibujar_matriz(self, padre):
        n = self.num_nodos
        celda = 30 if n <= 8 else 24
        margen = 34
        tam = margen + celda * n + 10

        marco = tk.Frame(padre, bg=CARD)
        marco.pack(side="left", padx=(0, 24))
        tk.Label(marco, text="Matriz de adyacencia", bg=CARD, fg=TENUE,
                 font=FUENTE_BOLD, justify="center").pack(anchor="center", pady=(0, 6))

        cnv = tk.Canvas(marco, width=tam, height=tam, bg=CARD, highlightthickness=0)
        cnv.pack()

        for i in range(n):
            cnv.create_text(margen + celda * i + celda / 2, margen / 2,
                             text=str(i + 1), fill=TENUE, font=("Segoe UI", 8))
            cnv.create_text(margen / 2, margen + celda * i + celda / 2,
                             text=str(i + 1), fill=TENUE, font=("Segoe UI", 8))

        for i in range(n):
            for j in range(n):
                x1 = margen + celda * j
                y1 = margen + celda * i
                relleno = V_MORADO if self.matriz[i][j] == 1 else BG
                cnv.create_rectangle(x1, y1, x1 + celda, y1 + celda,
                                      fill=relleno, outline=BORDE)

    def _dibujar_grafo(self, padre, colores=None, titulo="Representación gráfica"):
        n = self.num_nodos
        tam = 320
        centro = tam / 2
        radio = tam / 2 - 40

        marco = tk.Frame(padre, bg=CARD)
        marco.pack(side="left")
        tk.Label(marco, text=titulo, bg=CARD, fg=TENUE,
                 font=FUENTE_BOLD, justify="center").pack(anchor="center", pady=(0, 6))

        cnv = tk.Canvas(marco, width=tam, height=tam, bg=CARD, highlightthickness=0)
        cnv.pack()

        colores_nodo = colores or [V_MORADO, V_AZUL, V_MENTA, V_CORAL, V_ROSA]
        posiciones = []

        for i in range(n):
            angulo = 2 * math.pi * i / n - math.pi / 2
            x = centro + radio * math.cos(angulo)
            y = centro + radio * math.sin(angulo)
            posiciones.append((x, y))

        for i in range(n):
            for j in range(n):
                if self.matriz[i][j] == 1:
                    x1, y1 = posiciones[i]
                    # bucle
                    if i == j:
                        cnv.create_line(x1 - 10, y1 - 13, x1 - 28, y1 - 42,
                                        x1 + 28, y1 - 42, x1 + 10, y1 - 13,
                                        smooth=True, fill=V_AZUL, width=2,
                                        arrow=tk.LAST, arrowshape=(10, 12, 5))
                        continue
                    #conexión entre diferentes nodos
                    x2, y2 = posiciones[j]
                    dx, dy = x2 - x1, y2 - y1
                    dist = math.hypot(dx, dy)

                    if dist > 0:
                        ux = dx / dist
                        uy = dy / dist
                        x1_adj = x1 + ux * 16
                        y1_adj = y1 + uy * 16
                        x2_adj = x2 - ux * 16
                        y2_adj = y2 - uy * 16

                        if self.matriz[j][i] == 1:
                            nx, ny = -uy * 6, ux * 6
                            x1_adj += nx
                            y1_adj += ny
                            x2_adj += nx
                            y2_adj += ny
                        cnv.create_line(x1_adj, y1_adj, x2_adj, y2_adj, fill=LAVANDA,
                                        width=2, arrow=tk.LAST, arrowshape=(10, 12, 5))

        for i, (x, y) in enumerate(posiciones):
            color = colores_nodo[i % len(colores_nodo)]
            cnv.create_oval(x - 16, y - 16, x + 16, y + 16, fill=color, outline="")
            cnv.create_text(x, y, text=str(i + 1), fill="#ffffff", font=FUENTE_BOLD)

    def _pintar_degradado(self, evento):
        lienzo = evento.widget
        lienzo.delete("all")
        ancho = max(evento.width, 1)
        colores = [(155, 107, 255), (77, 163, 255), (255, 111, 160)]
        for x in range(0, ancho, 2):
            t = x / ancho * (len(colores) - 1)
            i = min(int(t), len(colores) - 2)
            f = t - i
            c1, c2 = colores[i], colores[i + 1]
            r = int(c1[0] + (c2[0] - c1[0]) * f)
            g = int(c1[1] + (c2[1] - c1[1]) * f)
            b = int(c1[2] + (c2[2] - c1[2]) * f)
            lienzo.create_line(x, 0, x, 4, fill=f"#{r:02x}{g:02x}{b:02x}")

    # Consola
    def escribir(self, mensaje, color=TEXTO):
        etiqueta = {TEXTO: "texto", TENUE: "tenue", OK: "ok",
                    ERROR: "error", V_ROSA: "titulo", V_AZUL: "dato"}[color]
        self.consola.config(state="normal")
        self.consola.insert("end", mensaje + "\n", etiqueta)
        self.consola.see("end")
        self.consola.config(state="disabled") 

    def titulo(self, texto):
        self.escribir("\n" + texto, V_ROSA)

    def limpiar_trabajo(self, titulo=None, subtitulo=None):
        for hijo in self.trabajo.winfo_children():
            hijo.destroy()

        contenedor = tk.Frame(self.trabajo, bg=CARD)
        contenedor.pack(fill="both", expand=True, padx=22, pady=20)
        if titulo:
            tk.Label(contenedor, text=titulo, bg=CARD, fg=TEXTO,
                     font=("Segoe UI", 13, "bold")).pack(anchor="w")
        if subtitulo:
            tk.Label(contenedor, text=subtitulo, bg=CARD, fg=TENUE,
                     font=FUENTE).pack(anchor="w", pady=(2, 12))
        elif titulo:
            tk.Frame(contenedor, bg=CARD, height=12).pack()

        fila = tk.Frame(contenedor, bg=CARD)
        fila.pack(fill="x")
        return fila, contenedor

    def _refrescar(self):
        self._dibujar_stepper()

    def _estado_paso(self, pid):
        if pid == "nodos":
            return "completado" if self.num_nodos is not None else "disponible"
        if pid == "tipo":
            if self.num_nodos is None:
                return "bloqueado"
            return "completado" if self.tipo_grafo is not None else "disponible"
        if pid == "generar":
            if self.tipo_grafo is None:
                return "bloqueado"
            return "completado" if self.matriz is not None else "disponible"
        return "disponible" if self.matriz is not None else "bloqueado"

    def _ir_a(self, pid):
        self.paso_actual = pid
        {
            "nodos": self.op_nodos,
            "tipo": self.op_tipo,
            "generar": self.op_generar,
            "matriz": self.op_matriz,
            "conexas": self.op_conexas,
            "resultado": self.op_resultado,
        }[pid]()
        self._dibujar_stepper()

    # Vista de pasos
    def op_nodos(self):
        fila, _ = self.limpiar_trabajo("① Número de nodos",
                                        "Elige un valor entre 4 y 12.")
        entrada = campo(fila, "Nodos", 6)
        if self.num_nodos is not None:
            entrada.insert(0, str(self.num_nodos))
        entrada.focus()
        entrada.bind("<Return>", lambda _e: confirmar())

        def confirmar():
            try:
                nodo = int(entrada.get())
            except ValueError:
                self.escribir("Error: Tipo de dato incorrecto", ERROR)
                return
            if nodo >= 4 and nodo <= 12:
                self.num_nodos = nodo
                self.matriz = None
                self.escribir(f"Cantidad de nodos registrados correctamente: {nodo}", OK)
                self.paso_actual = "tipo"
                self._refrescar()
                self.op_tipo()
            else:
                self.escribir("Error: El número de nodos debe de estar entre [4, 12]", ERROR)

        Chip(fila, "Registrar", confirmar, V_MORADO, icono="→").pack(side="left", pady=(18, 0))

    def op_tipo(self):
        if self.num_nodos is None:
            self.escribir("Error: Tienes que seleccionar un número de nodos primero", ERROR)
            self.paso_actual = "nodos"
            self._refrescar()
            self.op_nodos()
            return
        fila, _ = self.limpiar_trabajo("② Tipo de grafo",
                                        "¿Cómo quieres construir las conexiones?")

        def elegir(tipo):
            self.tipo_grafo = tipo
            self.matriz = None
            self.escribir(f"Tipo de grafo seleccionado: {tipo}", OK)
            self.paso_actual = "generar"
            self._refrescar()
            self.op_generar()

        Chip(fila, "Manual", lambda: elegir("manual"), V_AZUL, icono="✎",
             ancho=150).pack(side="left", padx=(0, 12))
        Chip(fila, "Aleatorio", lambda: elegir("aleatorio"), V_MENTA, icono="🎲",
             ancho=150).pack(side="left")

    def op_generar(self):
        if self.num_nodos is None:
            self.escribir("Error: Tienes que seleccionar un número de nodos primero", ERROR)
            self.op_nodos()
            return
        if self.tipo_grafo is None:
            self.escribir("Error: Tienes que seleccionar un tipo de grafo primero", ERROR)
            self.op_tipo()
            return
        if self.tipo_grafo == "manual":
            self.grafo_manual()
        if self.tipo_grafo == "aleatorio":
            self.grafo_aleatorio()

    def grafo_manual(self):
        self.matriz = matriz_vacia(self.num_nodos)
        self.conexiones = 0

        self.titulo("GRAFO MANUAL INTERACTIVO")
        self.escribir(f"Haz clic en cualquier celda para activar/desactivar conexiones (Origen → Destino).", TENUE)

        _fila, contenedor = self.limpiar_trabajo("③ Conexiones del Grafo (Matriz Interactiva)", "Fila = Nodo Origen | Columna = Nodo Destino")
        
        panel_interactivo = tk.Frame(contenedor, bg=CARD) 
        panel_interactivo.pack(fill="both", expand=True, pady=(4, 0))

        marco_matriz = tk.Frame(panel_interactivo, bg=CARD) 
        marco_matriz.pack(side="left", padx=(0, 20), anchor="n")

        tk.Frame(panel_interactivo, width=50, bg=CARD).pack(side="left")
        tk.Label(marco_matriz, text="Haz clic para cambiar (0 / 1)", bg=CARD, fg=TENUE, 
                 font=FUENTE_BOLD).pack(pady=(0, 6))
        grid_frame = tk.Frame(marco_matriz, bg=CARD)
        grid_frame.pack()

        # Encabezado superior origen/destino
        tk.Label(grid_frame, text="O\\D", font=("Segoe UI", 8, "bold"), fg=V_MORADO, bg=CARD, 
                 width=3).grid(row=0, column=0, padx=1, pady=1)
        
        # Columnas (destino)
        for j in range(self.num_nodos):
            tk.Label(grid_frame, text=str(j + 1), font=FUENTE_BOLD, fg=V_MORADO, bg=CARD, 
                     width=3).grid(row=0, column=j+1, padx=1, pady=1)
        
        # Filas (origen) y botones interactivos
        self.botones_matriz = {} 
        for i in range(self.num_nodos):
            tk.Label(grid_frame, text=str(i + 1), font=FUENTE_BOLD, fg=V_MORADO, bg=CARD, 
                     width=3).grid(row=i+1, column=0, padx=1, pady=1)
        
            for j in range(self.num_nodos): 
                btn = tk.Button(grid_frame, text="0", font=FUENTE, bg=BG, fg=TEXTO, relief="flat", 
                                width=3, height=1, highlightthickness=1, highlightbackground=BORDE, 
                                command=lambda r=i, c=j: alternar_celda(r, c))
    
                btn.grid(row=i+1, column=j+1, padx=1, pady=1)
                self.botones_matriz[(i, j)] = btn 
        
        # Alternar el valor de la celda al interactuar (0/1)
        def alternar_celda(r, c): 
            nuevo_val = 1 if self.matriz[r][c] == 0 else 0
            self.matriz[r][c] = nuevo_val

            # Actualizar color del botón 
            es_diag = (r == c)
            color_fondo = V_MORADO if nuevo_val == 1 else (BG if not es_diag else BLOQUEADO)
            color_texto = "#ffffff" if nuevo_val == 1 else TEXTO
            self.botones_matriz[(r, c)].config(text=str(nuevo_val), bg=color_fondo, fg=color_texto) 

            # Registrar en la consola 
            if r == c and nuevo_val == 1: 
                self.escribir(f"Bucle activado en nodo {r + 1}", V_AZUL)
            elif nuevo_val == 1: 
                self.escribir(f"Conexión agregada: {r + 1} → {c + 1}", V_AZUL)
            else: 
                self.escribir(f"Conexión removida: {r + 1} → {c + 1}", TENUE)
            actualizar_grafo() 
        
        marco_grafo = tk.Frame(panel_interactivo, bg=CARD)
        marco_grafo.pack(side="left", fill="both", expand=True)
            
        def actualizar_grafo():
            for child in marco_grafo.winfo_children():
                child.destroy() 
            self._dibujar_grafo(marco_grafo, titulo="Grafo en tiempo real") 
        actualizar_grafo()

        # Botón para confirmar y avanzar al paso 4
        def terminar(): 
            total_conn = sum(sum(fila) for fila in self.matriz)
            self.escribir(f"Grafo configurado con {total_conn} conexión(es) en total.", OK)
            self.paso_actual = "matriz" 
            self._refrescar() 
            self.op_matriz()
        
        Chip(contenedor, "Confirmar Grafo", terminar, V_ROSA, icono="✓", ancho=200).pack(anchor="e", pady=(12, 0))

    def grafo_aleatorio(self):
        self.matriz, conexiones_al = grafo_aleatorio(self.num_nodos)

        self.titulo("GRAFO ALEATORIO")
        self.escribir(f"Nodos disponibles del [1 - {self.num_nodos}]", TENUE)
        self.escribir(f"{conexiones_al} conexiones registradas correctamente", OK)
        self.paso_actual = "matriz"
        self._refrescar()
        self.op_matriz()

    def op_matriz(self):
        if self.matriz is None:
            self.escribir("Error: Tienes que generar el grafo primero", ERROR)
            self.op_generar()
            return

        self.titulo("MATRIZ DE ADYACENCIA")
        self.escribir(matriz_a_texto(self.matriz), TEXTO)

        _fila, contenedor = self.limpiar_trabajo("④ Matriz y representación gráfica", " ")
        visual = tk.Frame(contenedor, bg=CARD)
        visual.pack(fill="both", expand=True, pady=(4, 0))

        self._dibujar_matriz(visual)
        self._dibujar_grafo(visual)
        Chip(contenedor, "Buscar componentes", lambda: self._ir_a("conexas"),
             V_ROSA, icono="→", ancho=210).pack(anchor="e", pady=(10, 0))

    def op_conexas(self):
        if self.matriz is None:
            self.escribir("Error: Tienes que generar el grafo primero", ERROR)
            self.op_generar()
            return

        self.res = calcular_conexas(self.matriz)
        self.sub_paso = 0
        self.titulo("COMPONENTES CONEXAS")
        self.escribir("Usa «Siguiente» para avanzar etapa por etapa.", TENUE)
        self._mostrar_sub_paso()
 
    def _cambiar_sub_paso(self, delta):
        self.sub_paso += delta
        self._mostrar_sub_paso(registrar=(delta > 0))
 
    def _mostrar_sub_paso(self, registrar=True):
        pasos = self.res["pasos"]
        paso = pasos[self.sub_paso]
        total = len(pasos)
 
        _fila, contenedor = self.limpiar_trabajo(
            f"⑤ Componentes conexas · etapa {self.sub_paso + 1} de {total}",
            paso["titulo"])
 
        cuerpo = tk.Frame(contenedor, bg=CARD)
        cuerpo.pack(fill="both", expand=True)
        dibujar_matriz_generica(cuerpo, paso["matriz"], paso["filas"], paso["cols"],
                                "Matriz", paso["resaltes"], paso["bloques"])
 
        lado = tk.Frame(cuerpo, bg=CARD)
        lado.pack(side="left", fill="both", expand=True)
        tk.Label(lado, text=paso["texto"], bg=CARD, fg=TEXTO, font=FUENTE,
                 wraplength=290, justify="left").pack(anchor="w")
 
        botones = tk.Frame(lado, bg=CARD)
        botones.pack(anchor="w", pady=(16, 0))

        if self.sub_paso > 0:
            Chip(botones, "Anterior", lambda: self._cambiar_sub_paso(-1), "#d8cdf2",
                 color_texto=TEXTO, icono="←", ancho=130).pack(side="left", padx=(0, 12))
        if self.sub_paso < total - 1:
            Chip(botones, "Siguiente", lambda: self._cambiar_sub_paso(1), V_ROSA,
                 icono="→", ancho=130).pack(side="left")
        else:
            Chip(botones, "Resultado", lambda: self._ir_a("resultado"), V_MENTA,
                 icono="✓", ancho=130).pack(side="left")
 
        if registrar:
            self.escribir(f"Etapa {self.sub_paso + 1}/{total} — {paso['titulo']}", V_AZUL)
            self.escribir(paso["texto"], TEXTO)
            if paso["log_matriz"]:
                self.escribir(matriz_a_texto(paso["matriz"]), TEXTO)

    def op_resultado(self):
        if self.matriz is None:
            self.escribir("Error: Tienes que generar el grafo primero", ERROR)
            self.op_generar()
            return

        if not hasattr(self, 'res') or self.res is None:
            self.res = calcular_conexas(self.matriz)

        self.titulo("⑥ RESULTADO FINAL")
        _fila, contenedor = self.limpiar_trabajo("⑥ Resumen de componentes conexas",
                                                 "Resultado final del algoritmo")

        visual = tk.Frame(contenedor, bg=CARD)
        visual.pack(fill="both", expand=True, pady=(4, 0))

        self._dibujar_grafo(visual, colores=self.res["color_nodo"], titulo="Grafo por componentes")

        lado = tk.Frame(visual, bg=CARD)
        lado.pack(side="left", fill="both", expand=True, padx=(20, 0))
        total_comp = len(self.res["componentes"])
        tk.Label(lado, text=f"Total de componentes conexas: {total_comp}", bg=CARD, fg=V_MORADO,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        for i, miembros in enumerate(self.res["componentes"]):
            txt_comp = texto_componente(i, miembros)
            color_comp = PALETA_COMP[i % len(PALETA_COMP)]

            tarjeta_c = tk.Frame(lado, bg=BORDE, pady=1, padx=1)
            tarjeta_c.pack(fill="x", expand=False, pady=4)

            int_c = tk.Frame(tarjeta_c, bg=CARD, padx=10, pady=8)
            int_c.pack(fill="both", expand=False)

            tk.Label(int_c, text=f"Componente {i + 1}:", font=FUENTE_BOLD, fg=color_comp, 
                     bg=CARD).pack(side="left")
            tk.Label(int_c, text=f"  {txt_comp}", font=FUENTE, fg=TEXTO, bg=CARD).pack(side="left")
        self.escribir(f"\nProceso finalizado. Se encontraron {total_comp} componente(s) conexa(s).", OK)


def main():
    raiz = tk.Tk()
    icono = "icon_graf.ico"
    AppGrafos(raiz, icono)
    raiz.mainloop()

main()
