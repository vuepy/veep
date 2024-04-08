# coding: utf-8
import json
from pathlib import Path

import ipywidgets as widgets
from IPython.core.magic import register_line_magic

from ipywui import wui
from vuepy import create_app
from vuepy import get_script_src_from_sfc
from vuepy import import_sfc as _import_sfc


@register_line_magic
def vuepy_import(vue_sfc):
    """
    import vue sfc file

    ```python
    from ipywui import wui

    app=%vue_import test.vue
    app.use(wui)
    app.mount()
    ```

    :param vue_sfc:
    :return: App
    """
    return _import_sfc(vue_sfc)


@register_line_magic
def vuepy_demo(vue_sfc):
    """
    %vuepy_demo test.vue

    :param vue_sfc:
    :return:
    """
    sfc_file = vue_sfc.strip()
    sfc_file = Path(sfc_file)
    with open(sfc_file) as f:
        sfc_content = f.read()

    script_content = 0
    script_src = get_script_src_from_sfc(sfc_file)
    if script_src:
        script_file = sfc_file.parent.joinpath(script_src)
        with open(script_file) as f:
            script_content = f.read()

    print(json.dumps({
        'vue': sfc_content,
        'setup': script_content,
    }))

    App = _import_sfc(sfc_file)
    app = create_app(App).use(wui)
    return app.mount(widgets.Output())