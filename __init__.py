from aqt.qt import *
from anki.hooks import addHook
from aqt import mw

config = mw.addonManager.getConfig(__name__)


def _enter_character(char):
    config["last_used"] = char
    mw.web.eval('$("#typeans").val($("#typeans").val().slice(0, $("#typeans")[0].selectionStart) + "'
                + char + '" + $("#typeans").val().slice($("#typeans")[0].selectionStart))')


def _symbol_factory(symbol):
    return lambda _: _enter_character(symbol)


def _reviewerContextMenu(view, menu):
    if mw.state != "review":
        return

    main = QMenu(mw)

    last = main.addAction("Last Used: %s" % config["last_used"])
    last.triggered.connect(_symbol_factory(config["last_used"]))

    faves = QMenu("Favourites", mw)
    main.addMenu(faves)

    faves_list = list(config['favourites'])
    char_sets = config["char_sets"]

    for char in faves_list:
        a = faves.addAction(char)
        a.triggered.connect(_symbol_factory(char))

    for k, v in char_sets.items():
        tmp_menu = QMenu(k, mw)
        main.addMenu(tmp_menu)

        chars = list(v)

        for char in chars:
            a = tmp_menu.addAction(char)
            a.triggered.connect(_symbol_factory(char))

    main.exec_(QCursor.pos())


addHook('AnkiWebView.contextMenuEvent', _reviewerContextMenu)
