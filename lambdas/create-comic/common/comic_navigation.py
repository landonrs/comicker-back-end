def find_panel(panels, panel_id):
    """
    Find panel in comic. Returns none if panel id does not match.
    """
    for panel in panels:
        if panel["panelId"] == panel_id:
            return panel
        else:
            child_panels = panel["childPanels"]
            panel = find_panel(child_panels, panel_id)
            if panel:
                return panel

    return None
