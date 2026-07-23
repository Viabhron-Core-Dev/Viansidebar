package com.example.service

import fi.iki.elonen.NanoHTTPD
import java.util.zip.ZipFile

class PwaServer(port: Int, private val zipFilePath: String) : NanoHTTPD(port) {
    private var zipFile: ZipFile? = null

    override fun start() {
        zipFile = ZipFile(zipFilePath)
        super.start(NanoHTTPD.SOCKET_READ_TIMEOUT, false)
    }

    override fun stop() {
        super.stop()
        try {
            zipFile?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    override fun serve(session: IHTTPSession): Response {
        var uri = session.uri
        if (uri == "/") uri = "/index.html"
        uri = uri.removePrefix("/")
        
        try {
            val entry = zipFile?.getEntry(uri)
            if (entry != null) {
                val mimeType = getMimeTypeForExt(uri)
                val inputStream = zipFile!!.getInputStream(entry)
                val bytes = inputStream.readBytes()
                inputStream.close()
                return newFixedLengthResponse(Response.Status.OK, mimeType, bytes.inputStream(), bytes.size.toLong())
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return newFixedLengthResponse(Response.Status.NOT_FOUND, NanoHTTPD.MIME_PLAINTEXT, "404 Not Found")
    }

    private fun getMimeTypeForExt(uri: String): String {
        return when {
            uri.endsWith(".html") -> "text/html"
            uri.endsWith(".js") -> "application/javascript"
            uri.endsWith(".mjs") -> "application/javascript"
            uri.endsWith(".css") -> "text/css"
            uri.endsWith(".json") -> "application/json"
            uri.endsWith(".png") -> "image/png"
            uri.endsWith(".jpg") || uri.endsWith(".jpeg") -> "image/jpeg"
            uri.endsWith(".svg") -> "image/svg+xml"
            uri.endsWith(".ico") -> "image/x-icon"
            uri.endsWith(".wasm") -> "application/wasm"
            else -> "application/octet-stream"
        }
    }
}
