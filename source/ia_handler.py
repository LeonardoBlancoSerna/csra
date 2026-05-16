# A part of CSRA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import ctypes
import base64
import json
import requests
import threading
from io import BytesIO
import config
import speech
import ui
from logHandler import log
import winUser
import winGDI
import winBindings.gdi32
import winBindings.gdiplus as gdiplus
from screenBitmap import ScreenBitmap

class IAHandler:
	"""Manages AI-driven features for CSRA, including image description and text analysis."""

	def __init__(self):
		self._gdip_token = ctypes.c_ulong()
		self._init_gdiplus()

	def _init_gdiplus(self):
		startup_input = gdiplus.GdiplusStartupInput()
		startup_output = gdiplus.GdiplusStartupOutput()
		res = gdiplus.GdiplusStartup(ctypes.byref(self._gdip_token), ctypes.byref(startup_input), ctypes.byref(startup_output))
		if res != 0:
			log.error(f"Failed to initialize GDI+ for IAHandler: {res}")

	def __del__(self):
		if self._gdip_token:
			gdiplus.GdiplusShutdown(self._gdip_token)

	def analyze_screen(self, context="describe"):
		"""Captures the screen and sends it to the configured AI provider."""
		ui.message(_("Analizando pantalla con IA..."))
		
		# Run in a separate thread to avoid freezing the screen reader
		threading.Thread(target=self._run_analysis, args=(context,), daemon=True).start()

	def _run_analysis(self, context):
		try:
			image_data = self._capture_screen_to_base64()
			if not image_data:
				speech.speakMessage(_("Error al capturar la pantalla."))
				return

			provider = config.conf["IA"]["provider"]
			if provider == "local":
				result = self._send_to_local(image_data)
			elif provider == "gemini":
				result = self._send_to_gemini(image_data)
			else:
				speech.speakMessage(_("Proveedor de IA no configurado o no soportado."))
				return

			if result:
				speech.speakMessage(result)
			else:
				speech.speakMessage(_("No se pudo obtener una respuesta de la IA."))

		except Exception as e:
			log.exception("IAHandler error during analysis")
			speech.speakMessage(_("Ocurrió un error en el procesamiento de IA."))

	def _capture_screen_to_base64(self):
		"""Captures the primary monitor and returns a base64 encoded JPEG."""
		width = winUser.getSystemMetrics(winUser.SM_CXSCREEN)
		height = winUser.getSystemMetrics(winUser.SM_CYSCREEN)
		
		# Use existing ScreenBitmap to get screen pixels
		bitmap = ScreenBitmap(width, height)
		# Capture full screen (0,0 to width,height)
		pixels = bitmap.captureImage(0, 0, width, height)
		
		# Create a GDI+ bitmap from the raw pixels
		# pixels is an array of RGBQUAD (BGRA)
		gdip_bitmap = ctypes.c_void_p()
		# PixelFormat32bppARGB = 0x26200A
		res = gdiplus.GdipCreateBitmapFromScan0(width, height, width * 4, 0x26200A, ctypes.cast(pixels, ctypes.c_void_p), ctypes.byref(gdip_bitmap))
		if res != 0:
			log.error(f"GdipCreateBitmapFromScan0 failed: {res}")
			return None

		# Find JPEG encoder
		clsid = self._get_encoder_clsid("image/jpeg")
		if not clsid:
			log.error("Could not find JPEG encoder for GDI+")
			return None

		# Save to stream
		# GDI+ needs an IStream. We can use CreateStreamOnHGlobal.
		# But since we want to be simple, let's just save to a temp file or use a memory stream if possible.
		# For maximum compatibility with pure python without extra libs, let's use a temp file.
		import tempfile
		import os
		fd, path = tempfile.mkstemp(suffix=".jpg")
		os.close(fd)
		
		try:
			# GDI+ expects a wide string path
			res = gdiplus.GdipSaveImageToFile(gdip_bitmap, ctypes.c_wchar_p(path), ctypes.byref(clsid), None)
			if res != 0:
				log.error(f"GdipSaveImageToFile failed: {res}")
				return None
			
			with open(path, "rb") as f:
				data = f.read()
				return base64.b64encode(data).decode('utf-8')
		finally:
			if os.path.exists(path):
				os.remove(path)
			gdiplus.GdipDisposeImage(gdip_bitmap)

	def _get_encoder_clsid(self, mime_type):
		"""Helper to find the CLSID of a GDI+ encoder."""
		num = ctypes.c_uint()
		size = ctypes.c_uint()
		gdiplus.GdipGetImageEncodersSize(ctypes.byref(num), ctypes.byref(size))
		if size.value == 0:
			return None
		
		buf = ctypes.create_string_buffer(size.value)
		gdiplus.GdipGetImageEncoders(num, size, ctypes.cast(buf, ctypes.c_void_p))
		
		# ImageCodecInfo structure
		class ImageCodecInfo(ctypes.Structure):
			_fields_ = [
				("Clsid", winGDI.GUID),
				("FormatID", winGDI.GUID),
				("CodecName", ctypes.c_wchar_p),
				("DllName", ctypes.c_wchar_p),
				("FormatDescription", ctypes.c_wchar_p),
				("FilenameExtension", ctypes.c_wchar_p),
				("MimeType", ctypes.c_wchar_p),
				("Flags", ctypes.c_uint),
				("Version", ctypes.c_uint),
				("SigCount", ctypes.c_uint),
				("SigSize", ctypes.c_uint),
				("SigPattern", ctypes.c_void_p),
				("SigMask", ctypes.c_void_p),
			]
		
		encoders = ctypes.cast(buf, ctypes.POINTER(ImageCodecInfo))
		for i in range(num.value):
			if encoders[i].MimeType == mime_type:
				return encoders[i].Clsid
		return None

	def _send_to_local(self, image_data):
		"""Sends the image to a local Ollama instance."""
		url = f"{config.conf['IA']['localEndpoint']}/api/generate"
		model = config.conf["IA"]["localModel"]
		
		payload = {
			"model": model,
			"prompt": "Describe detalladamente esta captura de pantalla para una persona ciega. Sé preciso con el texto, iconos y la disposición de las ventanas.",
			"images": [image_data],
			"stream": False
		}
		
		try:
			response = requests.post(url, json=payload, timeout=30)
			response.raise_for_status()
			data = response.json()
			return data.get("response", "")
		except Exception as e:
			log.error(f"Ollama connection failed: {e}")
			return None

	def _send_to_gemini(self, image_data):
		"""Sends the image to Google Gemini API."""
		api_key = config.conf["IA"]["geminiKey"]
		if not api_key:
			return _("Error: Debes configurar tu API Key de Gemini en los ajustes.")
			
		url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
		
		payload = {
			"contents": [{
				"parts": [
					{"text": "Describe detalladamente esta captura de pantalla para una persona ciega. Sé preciso con el texto, iconos y la disposición de las ventanas."},
					{"inline_data": {
						"mime_type": "image/jpeg",
						"data": image_data
					}}
				]
			}]
		}
		
		try:
			response = requests.post(url, json=payload, timeout=30)
			response.raise_for_status()
			data = response.json()
			# Gemini 1.5 structure
			text = data['candidates'][0]['content']['parts'][0]['text']
			return text
		except Exception as e:
			log.error(f"Gemini API failed: {e}")
			return None

# Singleton instance
handler = IAHandler()
