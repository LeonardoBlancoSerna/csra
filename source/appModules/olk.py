# CSRA - AppModule for Modern Outlook (Open Source)
# Optimized for the WebView2/Chromium interface (olk.exe)
# Based on the streamlined architecture by Joseph Lee

import appModuleHandler

class AppModule(appModuleHandler.AppModule):
    """
    AppModule for the modern Microsoft Outlook.
    Automatically disables browse mode to prevent COM pointer errors
    and eliminate interface freezes.
    """
    disableBrowseModeByDefault: bool = True