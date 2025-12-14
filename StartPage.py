from nicegui import ui

@ui.page('/')
def start():
    with ui.column().classes('items-center justify-center h-screen'):
        ui.button('Attacker', on_click=lambda: ui.navigate.to('/attacker'))
        ui.button('Defender', on_click=lambda: ui.navigate.to('/Defender'))

@ui.page('/attacker')
def attacker():
   ui.button('click', on_click=lambda: ui.notify('Button clicked!'))
 
@ui.page('/Defender')
def Defender():
   ui.button('click', on_click=lambda: ui.notify('Button clicked!'))
 
ui.run()
