# -*- coding: utf-8 -*-
"""
Generador del Tablero Scrumban Integral v5.0 de HealthDesk Quantux
- Soporte Multi-tipo: Épicas, UHs, Tareas Técnicas, Issues/Bugs, Gaps, Mejoras, Oportunidades
- 4 Vistas Integradas:
  1. Tablero Scrumban (Kanban por columnas con WIP limits)
  2. Roadmap & Timeline Interactivo (Gantt visual, Épicas, Sprints y Milestones)
  3. Métricas, Burndown & Capacidad (Velocity, distribución y calidad)
  4. Backlog Jerárquico (Árbol colapsable Épica -> UHs -> Tareas/Issues)
- Agrupación Histórica de Sprints 1 a 5 desarrollados + Programación del Sprint 6 (Actual)
- Inclusión del ISSUE-04 de Alta Prioridad (P1) en el Sprint Backlog
"""
import json

print("Iniciando generación del Tablero Scrumban Integral...")
