# Operational Instructions for GUI Refactor Project: TalkingtoDragons_TINS_Edition

## Branch Policy
- Always commit to the branch named `new_GUI` after each milestone (see milestones in GUI_progress.md).

## Repository Structure
- The root folder contains the main source code in `Talking_to_Dragonsv5.py`:
- The TINS_Edition folder contains supporting files for GUI design, TINS methodology, and modernization:
  - `best_gui.py`, `GUI_progress.md`, `PySide6modern.md`, `scuffedepoch-sysp.md`, `scuffedepoch-tins.md`

## Behavioral Rules
1. Do NOT rely solely on documentation, verify all logic and functionality via the actual Python source files in `Talking_to_Dragonsv5.py`.
2. Treat the source code `Talking_to_Dragonsv5.py` as the source of truth for application logic and GUI mapping.
3. Use files in TINS_Edition as reference for GUI modernization and TINS principles.

## Development Tasks

1. Understand what TINS is by reading `scuffedepoch-tins.md` files.
2. Analyze all source code in `Talking_to_Dragonsv5.py` for functionality and UI-related logic.
3. Plan the GUI replacement using PySide6 idioms, mapping CLI and report logic to GUI widgets. Document this plan as a checkbox list by updating the current template `TINS_Edition/GUI_progress.md`, the template already has relevent info.
4. Commit to `new_GUI` branch, Description: "Planned PySide6 GUI architecture and widget mapping."
5. Update the TINS `TINS_Edition/README.md` summarizing project relationships, design, and implementation details based on the source code.
6. Commit to `new_GUI` branch, Description: "Drafted TINS_Edition/README.md with project relationships and design rationale."
7. Study PySide6 idioms in `TINS_Edition/PySide6modern.md` and layout samples in `TINS_Edition/best_gui.py`. Refactor the TINS `TINS_Edition/README.md` to describe how the GUI will be reconstructed using PySide6 version 6.9.1 architecture (signals, slots, widget hierarchies).
8. Commit to `new_GUI` branch, Description: "Updated root README.md with PySide6 architecture and integration details."
9. Review if `Talking_to_Dragonsv5.py` needs to encapsulate the data model and business logic derived from earlier analysis.
10. Implement `main.py` to handle PySide6 view/controller logic using appropriate design patterns (e.g., MVC or MVVM), connecting widgets to model logic.
11. Create/update `requirements.txt` in the root folder, including `PySide6==6.9.1` and any other necessary dependencies. (Use only the modern PySide6 6.9.1.)
12. Commit to `new_GUI` branch, Description: "Implemented core data model, view/controller logic."
13. Update the root `README.md` with standard GitHub install/run instructions, ensuring that usage aligns with TINS principles.
15. Perform a final integration review of GUI elements, verifying layout accuracy, event propagation, and modular consistency taking into account `TINS_Edition/PySide6modern.md`.
16. Commit to `new_GUI` branch, Description: "Final integration review of GUI elements and architecture."

**Note:** Only update and mark progress in `TINS_Edition/GUI_progress.md` after completing a milestone (not every sub-step). The checkbox list should be maintained exclusively in `TINS_Edition/GUI_progress.md`.

## Task Checklist to update and mark progress:
`TINS_Edition/GUI_progress.md`
