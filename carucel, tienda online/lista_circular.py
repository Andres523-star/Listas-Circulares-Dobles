"""
lista_circular.py
Lógica de la Lista Circular Doblemente Enlazada (Estructuras de Datos).

Idea clave: el último nodo apunta al primero (next) y el primero apunta
al último (prev). Por eso el carrusel nunca "se acaba": después del último
producto vuelve el primero, y antes del primero aparece el último.
"""

from typing import Any, List, Optional


class Node:
    """Nodo de la lista: guarda un dato y los enlaces a sus dos vecinos."""

    def __init__(self, data: Any):
        self.data = data
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class CircularDoublyLinkedList:
    """
    Lista circular doble.
    - head:    primer nodo de la lista.
    - current: nodo que se está mostrando en el carrusel.
    - size:    cantidad de nodos.
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self.current: Optional[Node] = None
        self.size: int = 0

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------
    def is_empty(self) -> bool:
        return self.head is None

    def _iter_nodes(self):
        """Recorre los nodos una sola vuelta, empezando en head."""
        node = self.head
        for _ in range(self.size):
            yield node
            node = node.next

    def _find(self, data: Any) -> Optional[Node]:
        """Busca el nodo que contiene 'data' (una sola vuelta)."""
        for node in self._iter_nodes():
            if node.data == data:
                return node
        return None

    # ------------------------------------------------------------------
    # Métodos obligatorios
    # ------------------------------------------------------------------
    def insert_at_beginning(self, data: Any) -> None:
        """Inserta un nodo nuevo antes de head y lo convierte en el nuevo head."""
        new_node = Node(data)

        if self.head is None:
            # Lista vacía: el nodo se apunta a sí mismo en ambas direcciones.
            new_node.next = new_node
            new_node.prev = new_node
            self.head = new_node
            self.current = new_node
        else:
            tail = self.head.prev          # el último nodo
            new_node.next = self.head
            new_node.prev = tail
            tail.next = new_node
            self.head.prev = new_node
            self.head = new_node           # el nuevo nodo pasa a ser el primero

        self.size += 1

    def insert_at_end(self, data: Any) -> None:
        """Inserta un nodo nuevo después del último (head no cambia)."""
        new_node = Node(data)

        if self.head is None:
            new_node.next = new_node
            new_node.prev = new_node
            self.head = new_node
            self.current = new_node
        else:
            tail = self.head.prev
            new_node.next = self.head
            new_node.prev = tail
            tail.next = new_node
            self.head.prev = new_node

        self.size += 1

    def delete(self, data: Any) -> bool:
        """
        Elimina el nodo que contiene 'data'. Devuelve True si lo eliminó.
        Mantiene la lista consistente:
        - Si borra el único nodo, la lista queda vacía.
        - Si borra head, head pasa al siguiente.
        - Si borra current (el producto que se está viendo), current pasa
          al siguiente, así el carrusel nunca queda apuntando a un nodo borrado.
        """
        node = self._find(data)
        if node is None:
            return False

        if self.size == 1:
            self.head = None
            self.current = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if node is self.head:
                self.head = node.next
            if node is self.current:
                self.current = node.next

        # Soltamos los enlaces del nodo eliminado
        node.next = None
        node.prev = None
        self.size -= 1
        return True

    def print_list(self) -> str:
        """
        Imprime la lista en consola y también devuelve el texto
        (para mostrarlo en la interfaz).
        Ejemplo: A ⇄ B ⇄ C ⇄ (vuelve a A)
        """
        if self.is_empty():
            texto = "(lista vacía)"
        else:
            nombres = [str(node.data) for node in self._iter_nodes()]
            texto = " ⇄ ".join(nombres) + f" ⇄ (vuelve a {nombres[0]})"
        print(texto)
        return texto

    # ------------------------------------------------------------------
    # Navegación del carrusel
    # ------------------------------------------------------------------
    def next_node(self) -> Optional[Any]:
        """Avanza al siguiente producto (después del último vuelve al primero)."""
        if self.current is None:
            return None
        self.current = self.current.next
        return self.current.data

    def prev_node(self) -> Optional[Any]:
        """Retrocede al producto anterior (antes del primero va al último)."""
        if self.current is None:
            return None
        self.current = self.current.prev
        return self.current.data

    # ------------------------------------------------------------------
    # Ayudas para el frontend
    # ------------------------------------------------------------------
    def get_current(self) -> Optional[Any]:
        return self.current.data if self.current else None

    def peek_next(self) -> Optional[Any]:
        """Dato del siguiente nodo, sin mover el carrusel."""
        return self.current.next.data if self.current else None

    def peek_prev(self) -> Optional[Any]:
        """Dato del nodo anterior, sin mover el carrusel."""
        return self.current.prev.data if self.current else None

    def set_current(self, data: Any) -> bool:
        """Deja 'data' como producto actual (si existe en la lista)."""
        node = self._find(data)
        if node is None:
            return False
        self.current = node
        return True

    def current_index(self) -> int:
        """Posición (0, 1, 2...) del producto actual contando desde head."""
        for i, node in enumerate(self._iter_nodes()):
            if node is self.current:
                return i
        return -1

    def to_list(self) -> List[Any]:
        return [node.data for node in self._iter_nodes()]
