"""
app.py
Frontend del carrusel de productos (Python + Streamlit).
Usa la Lista Circular Doblemente Enlazada de lista_circular.py.

Ejecutar:  streamlit run app.py
"""

import html
from dataclasses import dataclass
from urllib.parse import quote

import streamlit as st

from lista_circular import CircularDoublyLinkedList

st.set_page_config(page_title="Carrusel de Productos", layout="wide")

# ======================================================================
# 1. CSS PERSONALIZADO (Tonos Pastel: Crema, Durazno y Beige)
# ======================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700&display=swap');

:root {
    --bg: #fdfbf7;
    --surface: #ffffff;
    --card: #f9f6f0;
    --line: rgba(212, 163, 115, 0.3);
    --gold: #d4a373;
    --gold-soft: #e6b8a2;
    --text: #4a4a4a;
    --muted: #8a8a8a;
}

/* Fondo general */
.stApp {
    background: radial-gradient(1100px 560px at 50% -8%, #f4ece3 0%, var(--bg) 62%);
    color: var(--text);
    font-family: 'Manrope', sans-serif;
}
.stApp p, .stApp label { color: var(--text); }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.2rem; max-width: 1250px; }

/* Encabezado */
.hero { text-align: center; margin-bottom: 1.6rem; }
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem; font-weight: 700; line-height: 1.1;
    color: var(--text); letter-spacing: 0.01em;
}
.hero-sub { color: var(--muted); font-size: 1rem; margin-top: .4rem; }

/* Tarjeta del producto destacado */
.featured {
    position: relative; text-align: center;
    background: var(--surface);
    border: 1px solid var(--line); border-radius: 30px;
    padding: 1.6rem 1.8rem 1.9rem;
    box-shadow: 0 15px 35px -15px rgba(0, 0, 0, .1),
                0 0 0 1px rgba(255, 255, 255, .5) inset;
}
.badge {
    position: absolute; top: 1.2rem; left: 1.2rem;
    background: rgba(212, 163, 115, .15); color: var(--gold);
    border: 1px solid rgba(212, 163, 115, .5); border-radius: 999px;
    padding: .28rem .85rem; font-size: .72rem; font-weight: 700; letter-spacing: .08em;
}
.feat-img {
    height: 270px; display: flex; align-items: center; justify-content: center;
    background: radial-gradient(circle at 50% 58%, rgba(230, 184, 162, .3), transparent 64%);
}
.feat-img img {
    height: 235px; max-width: 100%; object-fit: contain;
    filter: drop-shadow(0 15px 15px rgba(0, 0, 0, .1));
}
.feat-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem; font-weight: 700; color: var(--text); margin-top: .5rem;
}
.feat-desc {
    color: var(--muted); font-size: .98rem; line-height: 1.55;
    max-width: 46ch; margin: .3rem auto 0;
}
.feat-rating { margin-top: .9rem; color: var(--muted); font-size: .9rem; }
.star { color: #dcdcdc; font-size: 1.05rem; }
.star.on { color: var(--gold); }
.feat-price {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.3rem; font-weight: 700; color: var(--gold); margin-top: .3rem;
}

/* Tarjetas laterales (anterior / siguiente) */
.mini {
    text-align: center; opacity: .7; transform: scale(.94);
    background: var(--surface); border: 1px solid var(--line);
    border-radius: 24px; padding: 1.1rem .8rem 1.2rem;
}
.mini img { height: 96px; max-width: 100%; object-fit: contain; }
.mini-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.25rem; font-weight: 700; margin-top: .5rem; color: var(--text);
}
.mini-price { color: var(--gold); font-weight: 600; font-size: .95rem; }

/* Puntos indicadores */
.dots { text-align: center; margin: 1.1rem 0 .6rem; }
.dot {
    display: inline-block; width: 8px; height: 8px; margin: 0 4px;
    border-radius: 50%; background: #e0d8c8;
}
.dot.on { background: var(--gold); width: 22px; border-radius: 6px; }

/* Botones de Streamlit */
.stButton > button {
    border-radius: 999px; font-family: 'Manrope', sans-serif; font-weight: 600;
    transition: background .2s, border-color .2s;
}
.st-key-btn_prev button, .st-key-btn_next button {
    background: transparent; color: var(--gold);
    border: 1px solid rgba(212, 163, 115, .6); padding: .55rem 1rem;
}
.st-key-btn_prev button:hover, .st-key-btn_next button:hover {
    background: rgba(212, 163, 115, .15); border-color: var(--gold); color: var(--gold);
}
.st-key-btn_add button, [data-testid="stFormSubmitButton"] button {
    background: var(--gold); color: #ffffff; border: 1px solid var(--gold);
}
.st-key-btn_add button:hover, [data-testid="stFormSubmitButton"] button:hover {
    background: var(--gold-soft); border-color: var(--gold-soft); color: #ffffff;
}
.st-key-btn_del button {
    background: transparent; color: var(--muted); border: 1px solid rgba(138, 138, 138, .4);
}
.st-key-btn_del button:hover { color: #d9534f; border-color: #d9534f; background: transparent; }
.stButton > button:focus-visible { outline: 2px solid var(--gold-soft); outline-offset: 2px; }

/* Barra lateral y Expanders */
[data-testid="stSidebar"] {
    background: var(--surface); border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] h3 {
    font-family: 'Cormorant Garamond', serif; font-size: 1.7rem; color: var(--text);
}
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="base-input"],
[data-testid="stSidebar"] [data-baseweb="textarea"],
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #fdfbf7 !important; border-color: rgba(212, 163, 115, .4) !important;
}
[data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
    color: var(--text) !important; -webkit-text-fill-color: var(--text);
}
[data-testid="stForm"] { border: 1px solid var(--line); border-radius: 18px; }

/* Estilo de Pestañas (Tabs) */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px; justify-content: center; margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    height: 50px; background-color: transparent;
    border-radius: 8px 8px 0px 0px; color: var(--muted);
    font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-weight: 600;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important; border-bottom: 2px solid var(--gold) !important;
}

/* En pantallas pequeñas se ocultan las tarjetas laterales */
@media (max-width: 900px) { .mini { display: none; } .hero-title { font-size: 2.4rem; } }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ======================================================================
# 2. MODELO DE DATOS Y UTILIDADES
# ======================================================================
@dataclass(eq=False)
class Product:
    name: str
    price: float
    description: str
    image_url: str
    category: str
    rating: float = 4.5
    reviews: int = 0

    def __str__(self) -> str:
        return self.name


def placeholder(emoji: str = "🛍️") -> str:
    """Genera una imagen SVG con el emoji para usarla como imagen del producto."""
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'>"
        f"<text x='100' y='108' font-size='120' text-anchor='middle' "
        f"dominant-baseline='middle'>{emoji}</text></svg>"
    )
    return "data:image/svg+xml;utf8," + quote(svg)


def safe_image(url: str) -> str:
    url = (url or "").strip()
    if url.startswith(("http://", "https://", "data:image/")):
        return html.escape(url, quote=True)
    return html.escape(placeholder(), quote=True)


def fmt_price(value: float) -> str:
    return f"${value:,.0f}".replace(",", ".")


def stars_html(rating: float) -> str:
    full = int(round(rating))
    return "".join(
        f'<span class="star{" on" if i < full else ""}">★</span>' for i in range(5)
    )


def featured_html(p: Product) -> str:
    reviews = f" ({p.reviews})" if p.reviews else ""
    return (
        '<div class="featured">'
        f'<div class="badge">{html.escape(p.category)}</div>'
        f'<div class="feat-img"><img src="{safe_image(p.image_url)}" alt="{html.escape(p.name, quote=True)}"/></div>'
        f'<div class="feat-title">{html.escape(p.name)}</div>'
        f'<div class="feat-desc">{html.escape(p.description)}</div>'
        f'<div class="feat-rating">{stars_html(p.rating)} {p.rating:.1f}{reviews}</div>'
        f'<div class="feat-price">{fmt_price(p.price)}</div>'
        "</div>"
    )


def mini_html(p: Product) -> str:
    return (
        '<div class="mini">'
        f'<img src="{safe_image(p.image_url)}" alt=""/>'
        f'<div class="mini-name">{html.escape(p.name)}</div>'
        f'<div class="mini-price">{fmt_price(p.price)}</div>'
        "</div>"
    )


def cart_card_html(p: Product) -> str:
    """Tarjeta para mostrar en el carrito con imagen real."""
    return (
        '<div style="background: #ffffff; border: 1px solid rgba(212, 163, 115, 0.3); '
        'border-radius: 15px; padding: 1rem; text-align: center; height: 100%;">'
        f'<img src="{safe_image(p.image_url)}" style="height: 120px; object-fit: contain; margin-bottom: 0.5rem;"/>'
        f'<div style="font-family: \'Cormorant Garamond\', serif; font-size: 1.2rem; font-weight: 700; color: #4a4a4a;">{html.escape(p.name)}</div>'
        f'<div style="color: #d4a373; font-weight: 600; font-size: 1.1rem;">{fmt_price(p.price)}</div>'
        '</div>'
    )


def dots_html(total: int, active: int) -> str:
    return '<div class="dots">' + "".join(
        f'<span class="dot{" on" if i == active else ""}"></span>' for i in range(total)
    ) + "</div>"


# ======================================================================
# 3. DATOS INICIALES
# ======================================================================
def cargar_datos_demo(lista: CircularDoublyLinkedList) -> None:
    # Usamos los emojis como imágenes para los productos de prueba
    demo = [
        Product("Reloj Inteligente", 249900, "Monitorea tu actividad, notificaciones y sueño todo el día.",
                placeholder("⌚"), "NUEVO", 4.6, 89),
        Product("Audífonos Inalámbricos", 189900, "Sonido de alta calidad con cancelación de ruido y 30 h de batería.",
                placeholder("🎧"), "BEST SELLER", 4.8, 120),
        Product("Mochila para Portátil", 139900, "Espaciosa, resistente al agua y con compartimento acolchado.",
                placeholder("🎒"), "POPULAR", 4.5, 75),
        Product("Teclado Mecánico", 229900, "Switches táctiles, retroiluminación y construcción en aluminio.",
                placeholder("⌨️"), "TRENDING", 4.7, 98),
    ]
    for producto in demo:
        lista.insert_at_end(producto)


if "lista" not in st.session_state:
    nueva_lista = CircularDoublyLinkedList()
    cargar_datos_demo(nueva_lista)
    st.session_state.lista = nueva_lista

if "carrito" not in st.session_state:
    st.session_state.carrito = CircularDoublyLinkedList()

lista: CircularDoublyLinkedList = st.session_state.lista
carrito: CircularDoublyLinkedList = st.session_state.carrito


# ======================================================================
# 4. CALLBACKS
# ======================================================================
def agregar_al_carrito():
    actual = lista.get_current()
    if actual is not None:
        carrito.insert_at_end(actual)
        st.toast(f"'{actual.name}' agregado al carrito")

def eliminar_del_carrito():
    actual_carrito = carrito.get_current()
    if actual_carrito is not None:
        carrito.delete(actual_carrito)
        st.toast(f"'{actual_carrito.name}' eliminado del carrito")

def vaciar_carrito():
    st.session_state.carrito = CircularDoublyLinkedList()
    st.toast("Carrito vaciado")


# ======================================================================
# 5. BARRA LATERAL
# ======================================================================
with st.sidebar:
    st.markdown("### Panel de Control")
    
    # Desplegable para Agregar Producto
    with st.expander("Agregar nuevo producto", expanded=False):
        with st.form("form_producto", clear_on_submit=True):
            nombre = st.text_input("Nombre")
            precio = st.number_input("Precio (COP)", min_value=0, step=1000, value=0)
            descripcion = st.text_area("Descripción", height=90)
            url_imagen = st.text_input("URL de la imagen", help="Si la dejas vacía se usa una imagen por defecto.")
            categoria = st.selectbox("Categoría", ["NUEVO", "BEST SELLER", "TRENDING", "POPULAR"])
            calificacion = st.slider("Calificación", 1.0, 5.0, 4.5, 0.1)
            posicion = st.radio("Insertar", ["Al final", "Al inicio"], horizontal=True)
            enviado = st.form_submit_button("Agregar al catálogo", use_container_width=True)

        if enviado:
            if not nombre.strip():
                st.error("Escribe el nombre del producto.")
            elif precio <= 0:
                st.error("El precio debe ser mayor que 0.")
            else:
                nuevo = Product(nombre.strip(), precio, descripcion.strip() or "Sin descripción.",
                                url_imagen.strip(), categoria, calificacion, 0)
                if posicion == "Al inicio":
                    lista.insert_at_beginning(nuevo)
                else:
                    lista.insert_at_end(nuevo)
                lista.set_current(nuevo)
                st.toast(f"'{nuevo.name}' agregado al catálogo")

    # Desplegable para explicar la Estructura
    with st.expander("Demostración del Enlace Circular", expanded=False):
        st.write("""
        **¿Qué es esto?** 
        Es la representación del catálogo actual. Como es una lista circular, el último producto 
        se conecta con el primero, permitiendo navegar infinitamente sin llegar a un final.
        """)
        st.caption(f"Total de productos en el catálogo: {lista.size}")
        # Aquí se muestra el texto generado por print_list(), que usa los nombres en vez de la palabra Nodo
        st.code(lista.print_list(), language=None)


# ======================================================================
# 6. CUERPO PRINCIPAL (PESTAÑAS)
# ======================================================================
st.markdown(
    '<div class="hero"><div class="hero-title">Productos destacados</div>'
    '<div class="hero-sub">Tecnología y accesorios para tu día a día</div></div>',
    unsafe_allow_html=True,
)

tab_catalogo, tab_carrito = st.tabs(["Catálogo", "Tu Carrito"])

# --- PESTAÑA 1: CATÁLOGO ---
with tab_catalogo:
    if lista.is_empty():
        st.info("No hay productos. Agrega uno desde la barra lateral.")
    else:
        actual = lista.get_current()
        varios = lista.size > 1

        col_prev, col_izq, col_centro, col_der, col_next = st.columns(
            [0.9, 1, 2.3, 1, 0.9], vertical_alignment="center"
        )

        with col_prev:
            st.button("Anterior", key="btn_prev", on_click=lista.prev_node,
                      disabled=not varios, use_container_width=True)
        with col_next:
            st.button("Siguiente", key="btn_next", on_click=lista.next_node,
                      disabled=not varios, use_container_width=True)

        if varios:
            with col_izq:
                st.markdown(mini_html(lista.peek_prev()), unsafe_allow_html=True)
            with col_der:
                st.markdown(mini_html(lista.peek_next()), unsafe_allow_html=True)

        with col_centro:
            st.markdown(featured_html(actual), unsafe_allow_html=True)
            st.markdown(dots_html(lista.size, lista.current_index()), unsafe_allow_html=True)
            
            # Solo aparece el botón de agregar al carrito
            st.button("Agregar al carrito", key="btn_add", on_click=agregar_al_carrito, use_container_width=True)

# --- PESTAÑA 2: CARRITO ---
with tab_carrito:
    if carrito.is_empty():
        st.info("Tu carrito está vacío. Ve al catálogo y agrega algunos productos.")
    else:
        st.markdown("### Resumen de tu compra")
        
        actual_carrito = carrito.get_current()
        varios_carrito = carrito.size > 1

        # Controles del carrito (Navegación circular)
        col_prev_c, col_info, col_next_c = st.columns([1, 2, 1], vertical_alignment="center")
        
        with col_prev_c:
            st.button("Anterior", key="cart_prev", on_click=carrito.prev_node, 
                      disabled=not varios_carrito, use_container_width=True)
        with col_next_c:
            st.button("Siguiente", key="cart_next", on_click=carrito.next_node, 
                      disabled=not varios_carrito, use_container_width=True)

        with col_info:
            # Mostramos el producto actual del carrito con su imagen y diseño
            st.markdown(
                f"<div style='text-align:center; padding: 1.5rem; background: #ffffff; "
                f"border: 1px solid rgba(212, 163, 115, 0.3); border-radius: 15px;'>"
                f"<img src='{safe_image(actual_carrito.image_url)}' style='height: 150px; object-fit: contain; margin-bottom: 1rem;'/>"
                f"<h3 style='margin:0; color: #4a4a4a; font-family: Cormorant Garamond, serif;'>{html.escape(actual_carrito.name)}</h3>"
                f"<p style='margin:0; color: #8a8a8a;'>{html.escape(actual_carrito.description)}</p>"
                f"<h2 style='margin-top:1rem; color: #d4a373; font-weight: bold;'>{fmt_price(actual_carrito.price)}</h2>"
                f"</div>", 
                unsafe_allow_html=True
            )

        # Botones de acción del carrito
        col_del, col_clear = st.columns(2)
        with col_del:
            st.button("Eliminar este producto del carrito", key="btn_del_cart", 
                      on_click=eliminar_del_carrito, use_container_width=True)
        with col_clear:
            if st.button("Vaciar Carrito", key="btn_clear_cart", use_container_width=True):
                vaciar_carrito()
                st.rerun()

        # Lista completa de productos en el carrito (en cuadrícula con imágenes)
        st.markdown("---")
        st.markdown("#### Productos en el carrito:")
        productos_en_carrito = carrito.to_list()
        total = sum(p.price for p in productos_en_carrito)
        
        # Crear una cuadrícula de 4 columnas
        cols = st.columns(4)
        for i, prod in enumerate(productos_en_carrito):
            with cols[i % 4]:
                st.markdown(cart_card_html(prod), unsafe_allow_html=True)
            
        st.markdown(f"### **Total a pagar: {fmt_price(total)}**")