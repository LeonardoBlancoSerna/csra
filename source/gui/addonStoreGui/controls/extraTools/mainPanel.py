# -*- coding: utf-8 -*-
# Copyright (C) 2022-2025 Héctor J. Benítez Corredera, CSRA
# This file is covered by the GNU General Public License.

import wx
import addonHandler
import globalVars
from gui import guiHelper
from gui.nvdaControls import CustomCheckListBox
from utils.addonUtils import utilidades, ajustes
import gui

class ExtraToolsPanel(wx.Panel):
	def __init__(self, parent):
		super(ExtraToolsPanel, self).__init__(parent)
		
		self.listAddons = list(addonHandler.getAvailableAddons())
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		self.notebook = wx.Notebook(self)
		mainSizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
		
		# Pestaña Empaquetador
		self.packagerPanel = wx.Panel(self.notebook)
		self._setupPackager(self.packagerPanel)
		self.notebook.AddPage(self.packagerPanel, _("Empaquetador"))
		
		# Pestaña Instalador Múltiple
		self.multiInstallPanel = wx.Panel(self.notebook)
		self._setupMultiInstaller(self.multiInstallPanel)
		self.notebook.AddPage(self.multiInstallPanel, _("Instalador Múltiple"))
		
		# Pestaña Backup
		self.backupPanel = wx.Panel(self.notebook)
		self._setupBackup(self.backupPanel)
		self.notebook.AddPage(self.backupPanel, _("Copias de Seguridad"))
		
		# Estado y Progreso común
		statusSizer = wx.StaticBoxSizer(wx.VERTICAL, self, _("Estado del proceso"))
		self.textEstado = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
		statusSizer.Add(self.textEstado, 1, wx.EXPAND | wx.ALL, 5)
		
		self.progreso = wx.Gauge(self, wx.ID_ANY, 100)
		statusSizer.Add(self.progreso, 0, wx.EXPAND | wx.ALL, 5)
		
		mainSizer.Add(statusSizer, 0, wx.EXPAND | wx.ALL, 5)
		
		self.SetSizer(mainSizer)
		self.Layout()

	def _setupPackager(self, panel):
		sizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(panel, -1, _("Seleccione complementos para empaquetar:"))
		sizer.Add(label, 0, wx.ALL, 5)
		
		self.listbox_empaquetador = CustomCheckListBox(panel, -1)
		for addon in self.listAddons:
			self.listbox_empaquetador.Append(addon.manifest["summary"])
		sizer.Add(self.listbox_empaquetador, 1, wx.EXPAND | wx.ALL, 5)
		
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.genBtn = wx.Button(panel, -1, _("Generar .nvda-addon"))
		self.genBtn.Bind(wx.EVT_BUTTON, self.onGenerate)
		btnSizer.Add(self.genBtn, 0, wx.ALL, 5)
		
		sizer.Add(btnSizer, 0, wx.CENTER)
		panel.SetSizer(sizer)

	def _setupMultiInstaller(self, panel):
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.selectDirBtn = wx.Button(panel, -1, _("Seleccionar carpeta de complementos..."))
		self.selectDirBtn.Bind(wx.EVT_BUTTON, self.onSelectInstallDir)
		sizer.Add(self.selectDirBtn, 0, wx.EXPAND | wx.ALL, 5)
		
		self.listbox_instalador = CustomCheckListBox(panel, -1)
		sizer.Add(self.listbox_instalador, 1, wx.EXPAND | wx.ALL, 5)
		
		self.installBtn = wx.Button(panel, -1, _("Instalar seleccionados"))
		self.installBtn.Bind(wx.EVT_BUTTON, self.onMultiInstall)
		sizer.Add(self.installBtn, 0, wx.CENTER | wx.ALL, 5)
		
		panel.SetSizer(sizer)

	def _setupBackup(self, panel):
		sizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(panel, -1, _("Elementos para copia de seguridad:"))
		sizer.Add(label, 0, wx.ALL, 5)
		
		self.listbox_backup = CustomCheckListBox(panel, -1)
		# Lógica de carga de backups omitida para brevedad, se integrará de ajustes.py
		sizer.Add(self.listbox_backup, 1, wx.EXPAND | wx.ALL, 5)
		
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.backupBtn = wx.Button(panel, -1, _("Crear Copia"))
		btnSizer.Add(self.backupBtn, 0, wx.ALL, 5)
		self.restoreBtn = wx.Button(panel, -1, _("Restaurar Copia"))
		btnSizer.Add(self.restoreBtn, 0, wx.ALL, 5)
		
		sizer.Add(btnSizer, 0, wx.CENTER)
		panel.SetSizer(sizer)

	# Métodos de puente para utilidades.py
	def onTextoEstado(self, texto):
		self.textEstado.AppendText(texto + "\n")
		
	def onProgreso(self, valor):
		self.progreso.SetValue(valor)
		
	def onCorrecto(self, msg):
		gui.messageBox(msg, _("Éxito"), wx.OK | wx.ICON_INFORMATION)
		
	def onError(self, msg):
		gui.messageBox(msg, _("Error"), wx.OK | wx.ICON_ERROR)

	def onGenerate(self, evt):
		selection = [i for i in range(self.listbox_empaquetador.GetCount()) if self.listbox_empaquetador.IsChecked(i)]
		if not selection:
			return
		dlg = wx.DirDialog(self, _("Seleccione dónde guardar los complementos:"), style=wx.DD_DEFAULT_STYLE)
		if dlg.ShowModal() == wx.ID_OK:
			utilidades.EmpaquetaComplementosIndividuales(self, selection, dlg.GetPath())
		dlg.Destroy()

	def onSelectInstallDir(self, evt):
		dlg = wx.DirDialog(self, _("Seleccione la carpeta con los .nvda-addon:"), style=wx.DD_DEFAULT_STYLE)
		if dlg.ShowModal() == wx.ID_OK:
			# Lógica de escaneo de carpeta
			pass
		dlg.Destroy()

	def onMultiInstall(self, evt):
		pass
