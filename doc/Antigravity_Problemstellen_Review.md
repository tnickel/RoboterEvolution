# Antigravity Review-Auftrag: RoboterEvolution Problemstellen

## Ziel

Bitte schaue gezielt auf die unten genannten Problemstellen im Projekt `RoboterEvolution`.
Es geht zuerst um Analyse und konkrete Handlungsempfehlungen, nicht um einen grossen Umbau.

Wichtig: Bitte bestehende Aenderungen im Worktree respektieren und nichts unrelated zuruecksetzen.

## Kontext

Das Projekt ist eine Pygame/NEAT-Co-Evolution:

- `main.py` startet Config-Menue, Hall of Fame und Training.
- `ai/neat_ai.py` enthaelt den zentralen Co-Evolution-Loop.
- `core/entities.py` enthaelt Roboter, Batterien, Bewegung und Kollision.
- `core/sensors.py` enthaelt Numba-Raycasts und Batch-Sensoren.
- `core/spatial_grid.py` enthaelt den raeumlichen Index.
- `core/fast_net.py` ist neu und ersetzt `neat-python`-Aktivierung teilweise durch Numba.
- `config/config_manager.py` enthaelt Defaults und Config-Menue.
- `ai/hall_of_fame.py` speichert Genome per Pickle.

Aktueller Stand laut Analyse:

- Syntaxcheck laeuft durch.
- `python test_fast_net.py` bestaetigt gleiche Outputs zwischen `neat-python` und `FastNetwork`.
- Gemessener Speedup war ca. `2.7x`, nicht `10-20x`.
- Der Git-Worktree ist bereits veraendert. Bitte nicht blind formatieren oder refactoren.

## Bitte pruefen

### 1. Config-Defaults vs. UI-Grenzen

Datei: `config/config_manager.py`

Pruefen:

- `collector_sensor_fov` Default ist `240.0`, aber der Slider erlaubt nur `30.0` bis `180.0`.
- `fitness_eaten_penalty` Default ist `-10000.0`, aber der Slider erlaubt nur `-5000.0` bis `0.0`.

Aufgabe:

- Einschaetzen, ob die Defaults oder die UI-Grenzen angepasst werden sollen.
- Bitte konkrete Empfehlung geben.
- Wenn gefixt wird: kleine, gezielte Aenderung.

### 2. SpatialGrid-Zeitpunkt im Simulationsloop

Datei: `ai/neat_ai.py`

Beobachtung:

- Das Grid wird am Anfang jedes Simulationsschritts aufgebaut.
- Danach bewegen sich Sammler und Jaeger.
- Spaeter werden auf Basis des alten Grids unter anderem Naehe, Batterien und Fang-Kollisionen abgefragt.

Pruefen:

- Kann das zu veralteten Treffer-/Fang-Abfragen fuehren?
- Ist das bei aktuellen Geschwindigkeiten relevant?
- Sollte das Grid nach Bewegungen neu aufgebaut werden, oder sollten Fang-Kollisionen direkt gegen aktuelle Positionen geprueft werden?

Aufgabe:

- Bitte eine risikoarme Loesung vorschlagen.
- Performance beachten, weil der Loop ein Hotspot ist.

### 3. Hall-of-Fame-Gaeste verfälschen Statistik

Datei: `ai/neat_ai.py`

Beobachtung:

- Hall-of-Fame-Gaeste werden zu `collectors` und `collector_genome_list` hinzugefuegt.
- Die Hall-of-Fame-Aufnahme schliesst Gaeste aus.
- Aber Best-/Average-Fitness und Graphdaten koennen Gaeste weiterhin enthalten.

Pruefen:

- Werden `best_collector_fitness`, `avg_collector_fitness`, Graphdaten oder Fitness-Breakdowns durch Gaeste verzerrt?
- Sollten Gaeste aus Statistik und Evolution getrennt werden?

Aufgabe:

- Bitte konkret sagen, welche Metriken trainierende Population zeigen sollen und welche inklusive Gaeste sinnvoll sind.
- Falls Fix: moeglichst klar getrennte Listen/Filter statt grossem Umbau.

### 4. Pickle-Sicherheit und Kompatibilitaet

Dateien:

- `ai/hall_of_fame.py`
- `ui/brain_viewer.py`
- `ai/neat_ai.py`

Beobachtung:

- `hall_of_fame.pkl` wird mit `pickle.load` geladen.
- Genome werden mit `pickle.loads` rekonstruiert.
- `config_hash` existiert als Feld, wird aber offenbar nicht ernsthaft genutzt.

Pruefen:

- Reicht fuer dieses lokale Projekt ein Hinweis, dass fremde Pickles nicht geladen werden sollen?
- Sollte vor dem Injizieren/Anzeigen eine bessere Kompatibilitaetspruefung stattfinden?
- Kann `config_hash` sinnvoll genutzt werden, um Sensor-/Output-Topologie abzusichern?

Aufgabe:

- Bitte pragmatische Empfehlung geben.
- Kein Security-Grossumbau, ausser es ist wirklich noetig.

### 5. Encoding/Mojibake

Dateien:

- `README.md`
- mehrere Python-Dateien mit Kommentaren/UI-Texten

Beobachtung:

- Umlaute und Emojis erscheinen kaputt, z.B. `ðŸ`, `Ã¼`.

Pruefen:

- Ist das nur Anzeige/Encoding im Terminal oder tatsaechlich im Dateiinhalt?
- Welche Dateien sollten zuerst bereinigt werden?

Aufgabe:

- Bitte vorsichtig pruefen.
- Nicht automatisch alle Dateien massenhaft umcodieren.
- Empfehlung fuer sauberes UTF-8-Vorgehen geben.

### 6. FastNetwork-Kommentar und Tests

Dateien:

- `core/fast_net.py`
- `test_fast_net.py`
- `ai/neat_ai.py`

Beobachtung:

- Der Code-Kommentar spricht von `10-20x` Speedup.
- Der lokale Benchmark zeigte ca. `2.7x`.

Pruefen:

- Ist der Benchmark ausreichend?
- Sollte der Kommentar realistischer formuliert werden?
- Sollte `test_fast_net.py` in eine echte Teststruktur ueberfuehrt werden?

Aufgabe:

- Bitte kleine Empfehlung geben.
- Keine grosse Testinfrastruktur erzwingen, wenn nicht noetig.

## Erwartetes Ergebnis

Bitte liefere zuerst einen kurzen Review-Bericht mit:

1. Befund pro Problemstelle.
2. Risiko/Prioritaet.
3. Konkreter Fix-Vorschlag.
4. Welche Dateien du anfassen wuerdest.

Wenn du direkt Code aenderst, dann bitte nur kleine, klar begrenzte Fixes und danach:

- `python -m py_compile main.py ai\neat_ai.py ai\hall_of_fame.py config\config_manager.py core\world.py core\entities.py core\sensors.py core\spatial_grid.py core\fast_net.py ui\brain_viewer.py ui\commentary.py ui\hall_of_fame_window.py ui\stats_graph.py`
- `python test_fast_net.py`

Bitte keine grossen Refactorings, kein automatisches Formatieren des ganzen Projekts und kein Zuruecksetzen vorhandener Aenderungen.
