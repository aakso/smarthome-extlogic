# smarthome-extlogic
Extended logic support for Smarthome.py

## WTF?
When I wrote this smarthome.py just used `exec()` to execute users logic code. This caused some issues if you wanted to define functions and/or classes to organize your logics. Thus I created this plugin to handle logics
in more controlled manner.

This plugin is very specific for my needs and if you find any use for it I would like to hear about it :)

## Example
See `logics.py` for my house's air heat pump control.

## Configuration (plugin.conf)
Example:
```
[extlogic]
    class_name = ExtLogicPlugin
    class_path = plugins.extlogic
    logic_classes = plugins.extlogic.logics:AutumnLogic | plugins.extlogic.logics:WinterLogic | plugins.extlogic.logics:SummerLogic
```

## Toggle item support
You can use following syntax in item configuration to make a toggle item for a logic class
```
[autumn_logic_toggle]
name = Autumn logic
extlogic_class = AutumnLogic
type = bool
```

