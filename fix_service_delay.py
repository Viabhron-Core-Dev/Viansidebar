import re

with open('app/src/main/java/com/example/service/VianSideAccessibilityService.kt', 'r') as f:
    content = f.read()

old_code = """    private fun handleQRScan() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            Toast.makeText(this, "Scanning for QR Code...", Toast.LENGTH_SHORT).show()
            takeScreenshot(android.view.Display.DEFAULT_DISPLAY, mainExecutor, object : TakeScreenshotCallback {"""

new_code = """    private fun handleQRScan() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            Toast.makeText(this, "Scanning for QR Code...", Toast.LENGTH_SHORT).show()
            Handler(Looper.getMainLooper()).postDelayed({
                takeScreenshot(android.view.Display.DEFAULT_DISPLAY, mainExecutor, object : TakeScreenshotCallback {"""

content = content.replace(old_code, new_code)

old_code_2 = """                    }
                }

                override fun onFailure(errorCode: Int) {
                    Handler(Looper.getMainLooper()).post {
                        Toast.makeText(this@VianSideAccessibilityService, "Failed to take screenshot", Toast.LENGTH_SHORT).show()
                    }
                }
            })
        } else {
            Toast.makeText(this, "Screen QR Scanner requires Android 11+", Toast.LENGTH_LONG).show()
        }
    }"""

new_code_2 = """                    }
                }

                override fun onFailure(errorCode: Int) {
                    Handler(Looper.getMainLooper()).post {
                        Toast.makeText(this@VianSideAccessibilityService, "Failed to take screenshot", Toast.LENGTH_SHORT).show()
                    }
                }
            })
            }, 400) // Delay to let sidebar close
        } else {
            Toast.makeText(this, "Screen QR Scanner requires Android 11+", Toast.LENGTH_LONG).show()
        }
    }"""

content = content.replace(old_code_2, new_code_2)

with open('app/src/main/java/com/example/service/VianSideAccessibilityService.kt', 'w') as f:
    f.write(content)
