# CSRA - Módulo para Signal Desktop

import appModuleHandler

class AppModule(appModuleHandler.AppModule):
	# Basado en el fix de WhatsApp para WebView2/Electron
	# Evita errores de puntero NULL COM en interfaces Chrome_RenderWidgetHostHWND
	disableBrowseModeByDefault: bool = True
