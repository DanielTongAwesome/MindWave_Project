"""
..module:: base_main_qt
  :platform: Windows, Linux(Raspbian-ARM)
  :synopsis: Defines the starting point of Qt Applications for both DTC and CAN signal
  visualizaion.

.. moduleauthor: Roger (Sichen) Luo <sichen.luo.external@autoliv.com>
"""
import sys

from PyQt4.QtGui import QApplication

def main(main_window):
    """
    Main Function of the module
    """

    app = QApplication(sys.argv)
    init_app(app)

    ui = main_window()
    ui.activateWindow()
    ui.show()

    sys.exit(app.exec_())


def init_app(app):
    """
    Initialize a Qt Application, by setting s style property
    (This will change when the setting menu is completed)
    """

    app.setStyle("plastique")
