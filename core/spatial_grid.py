"""
spatial_grid.py – Grid-basierte Kollisionserkennung fuer das Neuro-Oekosystem.

Teilt die Welt in Zellen auf und ermoeglicht effiziente
Proximity-Abfragen. Raycasts und Kollisionschecks pruefen
nur Objekte in relevanten Zellen statt aller Objekte.
"""

import math


class SpatialGrid:
    """Grid-basierte Raum-Partitionierung fuer effiziente Proximity-Abfragen.

    Die Welt wird in quadratische Zellen unterteilt. Jede Entity wird
    in die Zelle eingefuegt, die ihren Mittelpunkt enthaelt.
    Abfragen liefern nur Entities aus relevanten Zellen.

    Attributes:
        cell_size: Groesse einer Zelle in Pixeln
        grid: Dictionary {(cell_x, cell_y): [entity_list]}
    """

    def __init__(self, cell_size: int = 100) -> None:
        self.cell_size = cell_size
        self.grid: dict[tuple[int, int], list] = {}

    def _cell_key(self, x: float, y: float) -> tuple[int, int]:
        """Berechnet den Zellen-Schluessel fuer eine Position."""
        return (int(x // self.cell_size), int(y // self.cell_size))

    def clear(self) -> None:
        """Leert das gesamte Grid. Muss jeden Frame aufgerufen werden."""
        self.grid.clear()

    def insert(self, entity) -> None:
        """Fuegt eine Entity in die passende Zelle ein.

        Args:
            entity: Objekt mit x, y Attributen.
        """
        key = self._cell_key(entity.x, entity.y)
        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append(entity)

    def insert_all(self, entities: list) -> None:
        """Fuegt mehrere Entities ein.

        Args:
            entities: Liste von Objekten mit x, y Attributen.
        """
        for entity in entities:
            self.insert(entity)

    def query_radius(self, x: float, y: float, radius: float) -> list:
        """Gibt alle Entities im Umkreis einer Position zurueck.

        Prueft alle Zellen, die vom Suchkreis ueberlappt werden.
        Fuehrt anschliessend eine exakte Distanzpruefung durch.

        Args:
            x, y: Suchposition
            radius: Suchradius

        Returns:
            Liste von Entities innerhalb des Radius.
        """
        results = []
        r_sq = radius * radius

        # Zellen-Bereich berechnen, der vom Suchkreis ueberlappt wird
        min_cx = int((x - radius) // self.cell_size)
        max_cx = int((x + radius) // self.cell_size)
        min_cy = int((y - radius) // self.cell_size)
        max_cy = int((y + radius) // self.cell_size)

        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                cell = self.grid.get((cx, cy))
                if cell is None:
                    continue
                for entity in cell:
                    dx = entity.x - x
                    dy = entity.y - y
                    if dx * dx + dy * dy <= r_sq:
                        results.append(entity)

        return results

    def get_nearby(self, entity, radius: float) -> list:
        """Gibt alle Nachbar-Entities einer Entity zurueck (exkl. sich selbst).

        Args:
            entity: Die Entity, deren Nachbarn gesucht werden.
            radius: Suchradius.

        Returns:
            Liste von Nachbar-Entities (ohne die Entity selbst).
        """
        nearby = self.query_radius(entity.x, entity.y, radius)
        return [e for e in nearby if e is not entity]

    def query_rect(self, x1: float, y1: float, x2: float, y2: float) -> list:
        """Gibt alle Entities in einem Rechteck zurueck.

        Args:
            x1, y1: Obere linke Ecke
            x2, y2: Untere rechte Ecke

        Returns:
            Liste von Entities im Rechteck.
        """
        results = []
        min_cx = int(x1 // self.cell_size)
        max_cx = int(x2 // self.cell_size)
        min_cy = int(y1 // self.cell_size)
        max_cy = int(y2 // self.cell_size)

        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                cell = self.grid.get((cx, cy))
                if cell is None:
                    continue
                for entity in cell:
                    if x1 <= entity.x <= x2 and y1 <= entity.y <= y2:
                        results.append(entity)

        return results
